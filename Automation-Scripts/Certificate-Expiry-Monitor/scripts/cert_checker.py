#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Certificate Checker Module

Sprawdza certyfikaty SSL/TLS na zdalnych hostach.
Pobiera informacje o certyfikacie, oblicza dni do wygaśnięcia,
i zwraca szczegółowe informacje.
"""

import ssl
import socket
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from OpenSSL import SSL
import logging


@dataclass
class CertificateInfo:
    """Klasa przechowująca informacje o certyfikacie"""
    
    # Podstawowe informacje
    hostname: str
    port: int
    protocol: str
    
    # Subject i Issuer
    subject: str
    issuer: str
    common_name: str
    organization: Optional[str]
    
    # Daty
    valid_from: datetime
    valid_until: datetime
    days_remaining: int
    
    # Status
    is_valid: bool
    is_expired: bool
    is_self_signed: bool
    
    # Szczegóły techniczne
    serial_number: str
    version: int
    signature_algorithm: str
    public_key_algorithm: str
    key_size: int
    
    # Extensions
    san_domains: list
    has_wildcard: bool
    
    # Chain info
    chain_valid: Optional[bool] = None
    chain_length: Optional[int] = None
    
    # Alert level
    alert_level: str = "OK"  # OK, WARNING, CRITICAL, EXPIRED
    
    # Error info
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Konwertuj do dictionary"""
        data = asdict(self)
        # Konwertuj datetime do string
        data['valid_from'] = self.valid_from.isoformat()
        data['valid_until'] = self.valid_until.isoformat()
        return data


class CertificateChecker:
    """
    Główna klasa do sprawdzania certyfikatów SSL/TLS
    """
    
    def __init__(self, timeout: int = 10, verify: bool = False):
        """
        Inicjalizacja checker
        
        Args:
            timeout: Timeout dla połączenia (sekundy)
            verify: Czy weryfikować certyfikat
        """
        self.timeout = timeout
        self.verify = verify
        self.logger = logging.getLogger(__name__)
    
    def check_certificate(
        self,
        hostname: str,
        port: int = 443,
        protocol: str = "https"
    ) -> CertificateInfo:
        if isinstance(hostname, (list, tuple)):
            hostname = str(hostname[0])
        else:
            hostname = str(hostname)
            
        port = int(port)
        protocol = str(protocol)
        # """
        # Sprawdź certyfikat na danym hoście
        
        # Args:
        #     hostname: Hostname lub IP
        #     port: Port SSL/TLS
        #     protocol: Protokół (https, smtps, imaps, ldaps)
        
        # Returns:
        #     CertificateInfo object z danymi certyfikatu
        # """
        self.logger.info(f"Checking certificate for {hostname}:{port}")
        
        try:
            # Pobierz certyfikat
            cert_pem = self._get_certificate_pem(hostname, port, protocol)
            
            # Parse certyfikat
            cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
            
            # Ekstraktuj informacje
            cert_info = self._extract_certificate_info(
                cert, hostname, port, protocol
            )
            
            self.logger.info(
                f"Certificate for {hostname}:{port} - "
                f"{cert_info.days_remaining} days remaining"
            )
            
            return cert_info
            
        except Exception as e:
            self.logger.error(f"Error checking {hostname}:{port}: {str(e)}")
            return self._create_error_info(hostname, port, protocol, str(e))
    
    def _get_certificate_pem(
        self,
        hostname: str,
        port: int,
        protocol: str
    ) -> bytes:
        """
        Pobierz certyfikat w formacie PEM
        
        Args:
            hostname: Hostname
            port: Port
            protocol: Protokół
        
        Returns:
            Certyfikat w formacie PEM (bytes)
        """
        # Utwórz SSL context
        context = ssl.create_default_context()
        
        if not self.verify or hostname in ['localhost', '127.0.0.1']:
            # Dla self-signed - wyłącz weryfikację
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        
        # Połącz z serwerem
        with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
            # Wrap w SSL
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Pobierz certyfikat w DER format
                cert_der = ssock.getpeercert(binary_form=True)
                
                # Konwertuj DER do PEM
                cert_pem = ssl.DER_cert_to_PEM_cert(cert_der).encode('utf-8')
                
                return cert_pem
    
    def _extract_certificate_info(
        self,
        cert: x509.Certificate,
        hostname: str,
        port: int,
        protocol: str
    ) -> CertificateInfo:
        """
        Ekstraktuj informacje z certyfikatu
        
        Args:
            cert: x509.Certificate object
            hostname: Hostname
            port: Port
            protocol: Protokół
        
        Returns:
            CertificateInfo object
        """
        # Subject
        subject = cert.subject
        subject_str = self._format_name(subject)
        common_name = self._get_common_name(subject)
        organization = self._get_organization(subject)
        
        # Issuer
        issuer = cert.issuer
        issuer_str = self._format_name(issuer)
        
        # Sprawdź czy self-signed
        is_self_signed = subject_str == issuer_str
        
        # Daty
        valid_from = cert.not_valid_before_utc
        valid_until = cert.not_valid_after_utc
        
        # Oblicz dni do wygaśnięcia
        now = datetime.now(timezone.utc)
        days_remaining = (valid_until - now).days
        
        # Status
        is_valid = valid_from <= now <= valid_until
        is_expired = now > valid_until
        
        # Szczegóły techniczne
        serial_number = format(cert.serial_number, 'x')
        version = cert.version.value
        signature_algorithm = cert.signature_algorithm_oid._name
        
        # Public key info
        public_key = cert.public_key()
        public_key_algorithm = public_key.__class__.__name__
        key_size = public_key.key_size if hasattr(public_key, 'key_size') else 0
        
        # SAN (Subject Alternative Names)
        san_domains = self._get_san_domains(cert)
        has_wildcard = any(domain.startswith('*.') for domain in san_domains)
        
        # Określ alert level
        alert_level = self._determine_alert_level(days_remaining, is_expired)
        
        return CertificateInfo(
            hostname=hostname,
            port=port,
            protocol=protocol,
            subject=subject_str,
            issuer=issuer_str,
            common_name=common_name,
            organization=organization,
            valid_from=valid_from,
            valid_until=valid_until,
            days_remaining=days_remaining,
            is_valid=is_valid,
            is_expired=is_expired,
            is_self_signed=is_self_signed,
            serial_number=serial_number,
            version=version,
            signature_algorithm=signature_algorithm,
            public_key_algorithm=public_key_algorithm,
            key_size=key_size,
            san_domains=san_domains,
            has_wildcard=has_wildcard,
            alert_level=alert_level
        )
    
    def _format_name(self, name: x509.Name) -> str:
        """Formatuj X509 Name do string"""
        parts = []
        for attr in name:
            parts.append(f"{attr.oid._name}={attr.value}")
        return ", ".join(parts)
    
    def _get_common_name(self, name: x509.Name) -> str:
        """Pobierz Common Name (CN) z Subject"""
        try:
            cn = name.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
            return cn.value if cn else "N/A"
        except Exception:
            return "N/A"
    
    def _get_organization(self, name: x509.Name) -> Optional[str]:
        """Pobierz Organization (O) z Subject"""
        try:
            org = name.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)
            return org.value if org else None
        except Exception:
            return None
    
    def _get_san_domains(self, cert: x509.Certificate) -> list:
        """
        Pobierz listę domen z SAN (Subject Alternative Name)
        
        Args:
            cert: x509.Certificate
        
        Returns:
            Lista domen
        """
        try:
            san_ext = cert.extensions.get_extension_for_oid(
                x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
            )
            san_domains = [
                name.value for name in san_ext.value
                if isinstance(name, x509.DNSName)
            ]
            return san_domains
        except x509.ExtensionNotFound:
            return []
        except Exception as e:
            self.logger.warning(f"Error extracting SAN: {e}")
            return []
    
    def _determine_alert_level(self, days_remaining: int, is_expired: bool) -> str:
        """
        Określ poziom alertu na podstawie dni do wygaśnięcia
        
        Args:
            days_remaining: Dni do wygaśnięcia
            is_expired: Czy certyfikat wygasł
        
        Returns:
            Alert level: OK, WARNING, CRITICAL, EXPIRED
        """
        if is_expired:
            return "EXPIRED"
        elif days_remaining <= 7:
            return "CRITICAL"
        elif days_remaining <= 30:
            return "WARNING"
        else:
            return "OK"
    
    def _create_error_info(
        self,
        hostname: str,
        port: int,
        protocol: str,
        error: str
    ) -> CertificateInfo:
        """
        Utwórz CertificateInfo z błędem
        
        Args:
            hostname: Hostname
            port: Port
            protocol: Protokół
            error: Opis błędu
        
        Returns:
            CertificateInfo z błędem
        """
        now = datetime.now(timezone.utc)
        
        return CertificateInfo(
            hostname=hostname,
            port=port,
            protocol=protocol,
            subject="ERROR",
            issuer="ERROR",
            common_name="ERROR",
            organization=None,
            valid_from=now,
            valid_until=now,
            days_remaining=0,
            is_valid=False,
            is_expired=False,
            is_self_signed=False,
            serial_number="N/A",
            version=0,
            signature_algorithm="N/A",
            public_key_algorithm="N/A",
            key_size=0,
            san_domains=[],
            has_wildcard=False,
            alert_level="ERROR",
            error=error
        )
    
    def check_multiple_hosts(
        self,
        hosts: list,
        concurrent: int = 10
    ) -> Dict[str, CertificateInfo]:
        """
        Sprawdź wiele hostów jednocześnie

        Args:
            hosts: Lista tuple (hostname, port, protocol)
            concurrent: Ile jednocześnie

        Returns:
            Dictionary {hostname:port -> CertificateInfo}
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
    
        results = {}
    
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            # Submit wszystkie zadania
            future_to_host = {}
            
            for host in hosts:
                hostname = host
                port = host[1]
                protocol = host[2]
                
                future = executor.submit(self.check_certificate, hostname, port, protocol)
                future_to_host[future] = host
            #     executor.submit(
            #         self.check_certificate,
            #         host,
            #         host[1],
            #         host[2]
            #     ): host for host in hosts
            # }

            # Zbierz rezultaty
            for future in as_completed(future_to_host):
                host = future_to_host[future]
                try:
                    cert_info = future.result()
                    # FIX: Użyj wartości z cert_info, nie z host tuple
                    key = f"{cert_info.hostname}:{cert_info.port}"
                    results[key] = cert_info

                    self.logger.debug(f"Successfully checked {key}")

                except Exception as e:
                    self.logger.error(f"Error processing {host[0]}:{host[1]}: {e}")

                    # FIX: Dodaj error cert_info do wyników
                    error_info = self._create_error_info(
                        hostname=host[0],
                        port=host[1],
                        protocol=host[2],
                        error=str(e)
                    )
                    key = f"{host[0]}:{host[1]}"
                    results[key] = error_info

        return results



# Przykład użycia
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s'
    )
    
    # Utwórz checker
    checker = CertificateChecker(timeout=10, verify=False)
    
    # Sprawdź pojedynczy host
    print("\n=== Checking google.com ===")
    cert_info = checker.check_certificate("google.com", 443, "https")
    
    print(f"Host: {cert_info.hostname}:{cert_info.port}")
    print(f"Subject: {cert_info.common_name}")
    print(f"Issuer: {cert_info.issuer}")
    print(f"Valid Until: {cert_info.valid_until}")
    print(f"Days Remaining: {cert_info.days_remaining}")
    print(f"Alert Level: {cert_info.alert_level}")
    print(f"Self-Signed: {cert_info.is_self_signed}")
    
    # Sprawdź wiele hostów
    print("\n=== Checking multiple hosts ===")
    hosts = [
        ("google.com", 443, "https"),
        ("github.com", 443, "https"),
        ("stackoverflow.com", 443, "https")
    ]
    
    results = checker.check_multiple_hosts(hosts, concurrent=3)
    
    for key, cert_info in results.items():
        status = "✓" if cert_info.is_valid else "✗"
        print(f"{status} {key} - {cert_info.days_remaining} days - {cert_info.alert_level}")
