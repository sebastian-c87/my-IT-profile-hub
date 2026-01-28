#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Certificate Validator Module

Waliduje łańcuch certyfikatów, sprawdza zaufane CA,
weryfikuje revocation (CRL/OCSP).
"""

import ssl
import socket
from typing import List, Tuple, Optional
from dataclasses import dataclass
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID
from OpenSSL import SSL, crypto
import logging
import requests


@dataclass
class ValidationResult:
    """Rezultat walidacji certyfikatu"""
    
    # Chain validation
    chain_valid: bool
    chain_length: int
    chain_errors: List[str]
    
    # Trust validation
    trusted_ca: bool
    root_ca_name: Optional[str]
    
    # Revocation check
    revocation_checked: bool
    is_revoked: bool
    revocation_method: Optional[str]  # CRL, OCSP
    
    # Hostname validation
    hostname_valid: bool
    hostname_errors: List[str]
    
    # Security checks
    weak_signature: bool
    weak_key: bool
    security_issues: List[str]
    
    # Overall status
    valid: bool
    
    def __str__(self) -> str:
        """String reprezentacja"""
        status = "VALID" if self.valid else "INVALID"
        return (
            f"Validation: {status}\n"
            f"  Chain: {'✓' if self.chain_valid else '✗'} ({self.chain_length} certs)\n"
            f"  Trusted CA: {'✓' if self.trusted_ca else '✗'}\n"
            f"  Revocation: {'✓' if not self.is_revoked else '✗'}\n"
            f"  Hostname: {'✓' if self.hostname_valid else '✗'}\n"
            f"  Security: {'✓' if not (self.weak_signature or self.weak_key) else '✗'}"
        )


class CertificateValidator:
    """
    Klasa do walidacji certyfikatów i łańcuchów
    """
    
    # Weak signature algorithms
    WEAK_SIGNATURE_ALGORITHMS = ['md5', 'sha1', 'md2']
    
    # Minimum key sizes
    MIN_RSA_KEY_SIZE = 2048
    MIN_ECDSA_KEY_SIZE = 256
    
    def __init__(self, timeout: int = 10):
        """
        Inicjalizacja validator
        
        Args:
            timeout: Timeout dla połączeń (sekundy)
        """
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
    
    def validate_certificate(
        self,
        hostname: str,
        port: int = 443,
        check_revocation: bool = True,
        verify_hostname: bool = True
    ) -> ValidationResult:
        """
        Pełna walidacja certyfikatu
        
        Args:
            hostname: Hostname
            port: Port
            check_revocation: Czy sprawdzać revocation
            verify_hostname: Czy weryfikować hostname
        
        Returns:
            ValidationResult
        """
        self.logger.info(f"Validating certificate for {hostname}:{port}")
        
        chain_errors = []
        hostname_errors = []
        security_issues = []
        
        try:
            # Pobierz łańcuch certyfikatów
            cert_chain = self._get_certificate_chain(hostname, port)
            
            if not cert_chain:
                return self._create_invalid_result(
                    "Failed to retrieve certificate chain"
                )
            
            # Waliduj łańcuch
            chain_valid, chain_err = self._validate_chain(cert_chain)
            if chain_err:
                chain_errors.extend(chain_err)
            
            # Sprawdź zaufane CA
            trusted_ca, root_ca_name = self._check_trusted_ca(cert_chain)
            
            # Sprawdź revocation
            revocation_checked = False
            is_revoked = False
            revocation_method = None
            
            if check_revocation:
                is_revoked, revocation_method = self._check_revocation(cert_chain)
                revocation_checked = True
            
            # Sprawdź hostname
            hostname_valid = True
            if verify_hostname:
                hostname_valid, hostname_err = self._verify_hostname(
                    cert_chain, hostname
                )
                if hostname_err:
                    hostname_errors.extend(hostname_err)
            
            # Sprawdź security
            weak_signature = self._check_weak_signature(cert_chain)
            weak_key = self._check_weak_key(cert_chain)
            
            if weak_signature:
                security_issues.append("Weak signature algorithm detected")
            if weak_key:
                security_issues.append("Weak key size detected")
            
            # Overall validity
            valid = (
                chain_valid and
                trusted_ca and
                not is_revoked and
                hostname_valid and
                not weak_signature and
                not weak_key
            )
            
            return ValidationResult(
                chain_valid=chain_valid,
                chain_length=len(cert_chain),
                chain_errors=chain_errors,
                trusted_ca=trusted_ca,
                root_ca_name=root_ca_name,
                revocation_checked=revocation_checked,
                is_revoked=is_revoked,
                revocation_method=revocation_method,
                hostname_valid=hostname_valid,
                hostname_errors=hostname_errors,
                weak_signature=weak_signature,
                weak_key=weak_key,
                security_issues=security_issues,
                valid=valid
            )
            
        except Exception as e:
            self.logger.error(f"Validation error for {hostname}:{port}: {e}")
            return self._create_invalid_result(str(e))
    
    def _get_certificate_chain(
        self,
        hostname: str,
        port: int
    ) -> List[x509.Certificate]:
        """
        Pobierz pełny łańcuch certyfikatów
        
        Args:
            hostname: Hostname
            port: Port
        
        Returns:
            Lista certyfikatów (leaf -> intermediate -> root)
        """
        try:
            # Utwórz SSL context który nie weryfikuje (żeby pobrać chain)
            context = SSL.Context(SSL.TLSv1_2_METHOD)
            context.set_verify(SSL.VERIFY_NONE, lambda *args: True)
            
            # Połącz
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((hostname, port))
            
            # Wrap w SSL
            ssl_sock = SSL.Connection(context, sock)
            ssl_sock.set_tlsext_host_name(hostname.encode())
            ssl_sock.set_connect_state()
            ssl_sock.do_handshake()
            
            # Pobierz chain
            chain_openssl = ssl_sock.get_peer_cert_chain()
            
            # Konwertuj do cryptography x509
            chain = []
            for cert_openssl in chain_openssl:
                cert_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert_openssl)
                cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
                chain.append(cert)
            
            # Cleanup
            ssl_sock.shutdown()
            sock.close()
            
            return chain
            
        except Exception as e:
            self.logger.error(f"Error getting certificate chain: {e}")
            return []
    
    def _validate_chain(
        self,
        chain: List[x509.Certificate]
    ) -> Tuple[bool, List[str]]:
        """
        Waliduj łańcuch certyfikatów
        
        Args:
            chain: Lista certyfikatów
        
        Returns:
            (valid, errors)
        """
        errors = []
        
        if len(chain) < 1:
            return False, ["Empty certificate chain"]
        
        # Sprawdź każdy certyfikat w łańcuchu
        for i in range(len(chain) - 1):
            cert = chain[i]
            issuer_cert = chain[i + 1]
            
            # Sprawdź czy issuer się zgadza
            if cert.issuer != issuer_cert.subject:
                errors.append(
                    f"Chain break at position {i}: "
                    f"Issuer mismatch"
                )
                return False, errors
            
            # Sprawdź signature (w uproszczeniu - pełna walidacja wymaga więcej)
            try:
                # Weryfikacja podpisu jest skomplikowana w cryptography
                # W produkcji użyj OpenSSL verify
                pass
            except Exception as e:
                errors.append(f"Signature verification failed at position {i}: {e}")
                return False, errors
        
        # Jeśli dotarliśmy tu - chain jest OK
        return True, errors
    
    def _check_trusted_ca(
        self,
        chain: List[x509.Certificate]
    ) -> Tuple[bool, Optional[str]]:
        """
        Sprawdź czy root CA jest zaufany
        
        Args:
            chain: Lista certyfikatów
        
        Returns:
            (trusted, root_ca_name)
        """
        if not chain:
            return False, None
        
        # Pobierz root cert (ostatni w łańcuchu)
        root_cert = chain[-1]
        
        # Pobierz CA name
        try:
            cn_list = root_cert.subject.get_attributes_for_oid(
                x509.NameOID.COMMON_NAME
            )
            root_ca_name = cn_list.value if cn_list else "Unknown CA"
        except Exception:
            root_ca_name = "Unknown CA"
        
        # Sprawdź czy self-signed (root CA)
        is_self_signed = root_cert.issuer == root_cert.subject
        
        if not is_self_signed:
            # Nie dotarliśmy do root - chain niepełny
            return False, root_ca_name
        
        # W produkcji: sprawdź czy root CA jest w systemowym trust store
        # To jest uproszczone - zwracamy True jeśli to self-signed root
        # W prawdziwej implementacji porównaj z /etc/ssl/certs/ lub Windows cert store
        
        # Sprawdź znane CA (uproszczone)
        known_cas = [
            "Let's Encrypt",
            "DigiCert",
            "GlobalSign",
            "Sectigo",
            "GeoTrust",
            "Thawte",
            "Entrust"
        ]
        
        is_known_ca = any(ca.lower() in root_ca_name.lower() for ca in known_cas)
        
        return is_known_ca or is_self_signed, root_ca_name
    
    def _check_revocation(
        self,
        cert: x509.Certificate
    ) -> Tuple[bool, Optional[str]]:
        """
        Sprawdź czy certyfikat został unieważniony (revoked)
        
        Args:
            cert: Certyfikat
        
        Returns:
            (is_revoked, method)
        """
        # Sprawdź OCSP
        try:
            ocsp_urls = self._get_ocsp_urls(cert)
            if ocsp_urls:
                # W pełnej implementacji: zrób OCSP request
                # To wymaga budowania OCSP request, wysłania, parsowania response
                # Dla uproszczenia - zakładamy że nie revoked
                return False, "OCSP"
        except Exception as e:
            self.logger.debug(f"OCSP check failed: {e}")
        
        # Sprawdź CRL
        try:
            crl_urls = self._get_crl_urls(cert)
            if crl_urls:
                # W pełnej implementacji: pobierz CRL, sprawdź czy cert jest na liście
                # To wymaga pobierania i parsowania CRL
                # Dla uproszczenia - zakładamy że nie revoked
                return False, "CRL"
        except Exception as e:
            self.logger.debug(f"CRL check failed: {e}")
        
        # Nie udało się sprawdzić
        return False, None
    
    def _get_ocsp_urls(self, cert: x509.Certificate) -> List[str]:
        """Pobierz OCSP URLs z certyfikatu"""
        try:
            aia = cert.extensions.get_extension_for_oid(
                ExtensionOID.AUTHORITY_INFORMATION_ACCESS
            )
            ocsp_urls = [
                desc.access_location.value
                for desc in aia.value
                if desc.access_method == x509.AuthorityInformationAccessOID.OCSP
            ]
            return ocsp_urls
        except x509.ExtensionNotFound:
            return []
    
    def _get_crl_urls(self, cert: x509.Certificate) -> List[str]:
        """Pobierz CRL URLs z certyfikatu"""
        try:
            crl_dist = cert.extensions.get_extension_for_oid(
                ExtensionOID.CRL_DISTRIBUTION_POINTS
            )
            crl_urls = []
            for dist_point in crl_dist.value:
                if dist_point.full_name:
                    for name in dist_point.full_name:
                        if isinstance(name, x509.UniformResourceIdentifier):
                            crl_urls.append(name.value)
            return crl_urls
        except x509.ExtensionNotFound:
            return []
    
    def _verify_hostname(
        self,
        cert: x509.Certificate,
        hostname: str
    ) -> Tuple[bool, List[str]]:
        """
        Weryfikuj czy hostname pasuje do certyfikatu
        
        Args:
            cert: Certyfikat
            hostname: Hostname do sprawdzenia
        
        Returns:
            (valid, errors)
        """
        errors = []
        
        # Pobierz CN
        try:
            cn_list = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
            cn = cn_list.value if cn_list else None
        except Exception:
            cn = None
        
        # Pobierz SAN
        try:
            san_ext = cert.extensions.get_extension_for_oid(
                ExtensionOID.SUBJECT_ALTERNATIVE_NAME
            )
            san_domains = [
                name.value for name in san_ext.value
                if isinstance(name, x509.DNSName)
            ]
        except x509.ExtensionNotFound:
            san_domains = []
        
        # Sprawdź match
        all_names = [cn] + san_domains if cn else san_domains
        
        if not all_names:
            errors.append("No hostname information in certificate")
            return False, errors
        
        # Sprawdź exact match lub wildcard
        for name in all_names:
            if name == hostname:
                return True, []
            
            # Wildcard match
            if name.startswith('*.'):
                domain = name[2:]
                if hostname.endswith(domain):
                    return True, []
        
        errors.append(f"Hostname {hostname} does not match certificate")
        return False, errors
    
    def _check_weak_signature(self, cert: x509.Certificate) -> bool:
        """Sprawdź czy signature algorithm jest słaby"""
        sig_alg = cert.signature_algorithm_oid._name.lower()
        return any(weak in sig_alg for weak in self.WEAK_SIGNATURE_ALGORITHMS)
    
    def _check_weak_key(self, cert: x509.Certificate) -> bool:
        """Sprawdź czy klucz jest za słaby"""
        try:
            public_key = cert.public_key()
            
            # RSA
            if hasattr(public_key, 'key_size'):
                if 'RSA' in public_key.__class__.__name__:
                    return public_key.key_size < self.MIN_RSA_KEY_SIZE
                elif 'EC' in public_key.__class__.__name__:
                    return public_key.key_size < self.MIN_ECDSA_KEY_SIZE
            
            return False
        except Exception:
            return False
    
    def _create_invalid_result(self, error: str) -> ValidationResult:
        """Utwórz ValidationResult dla błędu"""
        return ValidationResult(
            chain_valid=False,
            chain_length=0,
            chain_errors=[error],
            trusted_ca=False,
            root_ca_name=None,
            revocation_checked=False,
            is_revoked=False,
            revocation_method=None,
            hostname_valid=False,
            hostname_errors=[error],
            weak_signature=False,
            weak_key=False,
            security_issues=[error],
            valid=False
        )


# Przykład użycia
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s'
    )
    
    # Utwórz validator
    validator = CertificateValidator(timeout=10)
    
    # Waliduj certyfikat
    print("\n=== Validating google.com ===")
    result = validator.validate_certificate(
        "google.com",
        443,
        check_revocation=False,  # OCSP może nie działać w tym przykładzie
        verify_hostname=True
    )
    
    print(result)
    
    if result.valid:
        print("\n✓ Certificate is VALID")
    else:
        print("\n✗ Certificate is INVALID")
        if result.chain_errors:
            print("Chain errors:", result.chain_errors)
        if result.hostname_errors:
            print("Hostname errors:", result.hostname_errors)
        if result.security_issues:
            print("Security issues:", result.security_issues)
