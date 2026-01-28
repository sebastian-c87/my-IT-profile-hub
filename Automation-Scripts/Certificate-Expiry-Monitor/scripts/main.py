#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Certificate Expiry Monitor - Main Entry Point

Główny skrypt orkiestrujący:
- Ładowanie konfiguracji
- Sprawdzanie certyfikatów
- Walidacja
- Wysyłanie alertów
- Generowanie raportów
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict
import logging

from cert_checker import CertificateChecker, CertificateInfo
from cert_validator import CertificateValidator
from alerting import EmailAlerter, SlackAlerter, TeamsAlerter
from reporting import ReportGenerator
from utils import ConfigLoader, ColorPrinter, LoggerSetup, FileUtils


class CertificateMonitor:
    """Główna klasa orchestrująca cały proces"""
    
    def __init__(self, config_loader: ConfigLoader):
        """
        Inicjalizacja monitora
        
        Args:
            config_loader: ConfigLoader instance
        """
        self.config_loader = config_loader
        self.project_root = config_loader.project_root
        
        # Załaduj konfigurację
        self.domains_config = config_loader.load_yaml("config/domains.yml")
        self.settings_config = config_loader.load_yaml("config/settings.yml")
        
        # Setup logger
        log_config = self.settings_config['logging']
        self.logger = LoggerSetup.setup_logger(
            name="certificate_monitor",
            log_file=str(self.project_root / log_config['file']),
            level=log_config['level'],
            console=log_config['console'],
            max_size_mb=log_config['max_size_mb'],
            backup_count=log_config['backup_count']
        )
        
        # Color printer
        self.printer = ColorPrinter()
        
        # Inicjalizuj komponenty
        self._init_checker()
        self._init_validator()
        self._init_alerters()
        self._init_reporter()
    
    def _init_checker(self):
        """Inicjalizuj certificate checker"""
        general_config = self.settings_config['general']
        
        self.checker = CertificateChecker(
            timeout=general_config['connection_timeout'],
            verify=self.settings_config['validation']['verify_chain']
        )
    
    def _init_validator(self):
        """Inicjalizuj certificate validator"""
        general_config = self.settings_config['general']
        
        self.validator = CertificateValidator(
            timeout=general_config['connection_timeout']
        )
    
    def _init_alerters(self):
        """Inicjalizuj alerters"""
        # Email
        smtp_config = self.settings_config['smtp']
        if smtp_config['enabled']:
            self.email_alerter = EmailAlerter(
                smtp_host=smtp_config['host'],
                smtp_port=smtp_config['port'],
                smtp_username=smtp_config['username'],
                smtp_password=smtp_config['password'],
                from_address=smtp_config['from_address'],
                use_tls=smtp_config['use_tls']
            )
        else:
            self.email_alerter = None
        
        # Slack
        slack_config = self.settings_config['slack']
        if slack_config['enabled']:
            self.slack_alerter = SlackAlerter(
                webhook_url=slack_config['webhook_url'],
                channel=slack_config.get('channel')
            )
        else:
            self.slack_alerter = None
        
        # Teams
        teams_config = self.settings_config['teams']
        if teams_config['enabled']:
            self.teams_alerter = TeamsAlerter(
                webhook_url=teams_config['webhook_url']
            )
        else:
            self.teams_alerter = None
    
    def _init_reporter(self):
        """Inicjalizuj report generator"""
        report_config = self.settings_config['reporting']
        output_path = self.project_root / report_config['output_path']
        
        self.reporter = ReportGenerator(output_path)
    
    def get_enabled_hosts(self) -> List[tuple]:
        """
        Pobierz listę aktywnych hostów do sprawdzenia

        Returns:
            Lista tuple (hostname, port, protocol)
        """
        hosts = []

        for group_name, group_hosts in self.domains_config.items():
            if isinstance(group_hosts, list):
                for host_config in group_hosts:
                    if host_config.get('enabled', False):
                        hostname = str(host_config['host'])
                        port = int(host_config['port'])
                        protocol = str(host_config['protocol'])

                        hosts.append((hostname, port, protocol))

        return hosts

    
    def check_all_certificates(self) -> Dict[str, CertificateInfo]:
        """
        Sprawdź wszystkie aktywne certyfikaty
        
        Returns:
            Dictionary {hostname:port -> CertificateInfo}
        """
        self.logger.info("Starting certificate check")
        self.printer.header("Certificate Expiry Monitor")
        
        # Pobierz hosty
        hosts = self.get_enabled_hosts()
        
        if not hosts:
            self.logger.warning("No enabled hosts found in configuration")
            self.printer.warning("No enabled hosts found!")
            return {}
        
        self.logger.info(f"Checking {len(hosts)} hosts")
        print(f"Checking {len(hosts)} hosts...\n")
        
        # Sprawdź certyfikaty
        general_config = self.settings_config['general']
        results = self.checker.check_multiple_hosts(
            hosts,
            concurrent=general_config['concurrent_checks']
        )
        
        # Wyświetl rezultaty
        print("\nResults:")
        print("-" * 60)

        for key, cert_info in sorted(results.items()):
            if cert_info.error:
                self.printer.error(f"{key} - ERROR: {cert_info.error}")
            else:
                self.printer.status_line(
                    key,
                    cert_info.days_remaining,
                    cert_info.alert_level
                )
        
        self.logger.info(f"Certificate check completed: {len(results)} hosts")
        return results
    
    def send_alerts(self, certificates: Dict[str, CertificateInfo]):
        """
        Wyślij alerty dla certyfikatów wymagających uwagi
        
        Args:
            certificates: Dictionary z certyfikatami
        """
        # Filtruj certyfikaty wymagające alertów
        alert_certs = {
            k: v for k, v in certificates.items()
            if v.alert_level in ['WARNING', 'CRITICAL', 'EXPIRED']
        }
        
        if not alert_certs:
            self.logger.info("No alerts to send - all certificates OK")
            print("\n✓ All certificates OK - no alerts needed")
            return
        
        self.logger.info(f"Sending alerts for {len(alert_certs)} certificates")
        print(f"\nSending alerts for {len(alert_certs)} certificates...")
        
        alerts_config = self.settings_config['alerts']
        smtp_config = self.settings_config['smtp']
        
        # Email alerts
        if self.email_alerter and alerts_config.get('alert_on_warning', True):
            to_addresses = smtp_config['to_addresses'].split(',')
            
            for cert_info in alert_certs.values():
                try:
                    self.email_alerter.send_alert(to_addresses, cert_info)
                    self.logger.info(f"Email alert sent for {cert_info.hostname}:{cert_info.port}")
                except Exception as e:
                    self.logger.error(f"Failed to send email alert: {e}")
        
        # Slack alerts
        if self.slack_alerter:
            for cert_info in alert_certs.values():
                try:
                    mention = None
                    if cert_info.alert_level == 'CRITICAL':
                        mention = self.settings_config['slack'].get('mention_on_critical')
                    
                    self.slack_alerter.send_alert(cert_info, mention)
                    self.logger.info(f"Slack alert sent for {cert_info.hostname}:{cert_info.port}")
                except Exception as e:
                    self.logger.error(f"Failed to send Slack alert: {e}")
        
        # Teams alerts
        if self.teams_alerter:
            for cert_info in alert_certs.values():
                try:
                    self.teams_alerter.send_alert(cert_info)
                    self.logger.info(f"Teams alert sent for {cert_info.hostname}:{cert_info.port}")
                except Exception as e:
                    self.logger.error(f"Failed to send Teams alert: {e}")
        
        print(f"✓ Alerts sent for {len(alert_certs)} certificates")
    
    def generate_reports(self, certificates: Dict[str, CertificateInfo]):
        """
        Generuj raporty
        
        Args:
            certificates: Dictionary z certyfikatami
        """
        if not certificates:
            self.logger.warning("No certificates to report")
            return
        
        self.logger.info("Generating reports")
        print("\nGenerating reports...")
        
        cert_list = list(certificates.values())
        report_config = self.settings_config['reporting']
        formats = report_config['formats']
        
        # HTML
        if formats.get('html', True):
            try:
                html_path = self.reporter.generate_html_report(cert_list)
                print(f"✓ HTML report: {html_path}")
            except Exception as e:
                self.logger.error(f"Failed to generate HTML report: {e}")
        
        # CSV
        if formats.get('csv', True):
            try:
                csv_path = self.reporter.generate_csv_report(cert_list)
                print(f"✓ CSV report: {csv_path}")
            except Exception as e:
                self.logger.error(f"Failed to generate CSV report: {e}")
        
        # JSON
        if formats.get('json', True):
            try:
                json_path = self.reporter.generate_json_report(cert_list)
                print(f"✓ JSON report: {json_path}")
            except Exception as e:
                self.logger.error(f"Failed to generate JSON report: {e}")
        
        self.logger.info("Reports generated successfully")
    
    def run_full_check(self):
        """Uruchom pełny check: sprawdź + alerty + raporty"""
        try:
            # Sprawdź certyfikaty
            certificates = self.check_all_certificates()
            
            if not certificates:
                return
            
            # Wyślij alerty
            self.send_alerts(certificates)
            
            # Wygeneruj raporty
            self.generate_reports(certificates)
            
            # Podsumowanie
            self._print_summary(certificates)
            
        except Exception as e:
            self.logger.error(f"Error during full check: {e}", exc_info=True)
            self.printer.error(f"Error: {e}")
            sys.exit(1)
    
    def _print_summary(self, certificates: Dict[str, CertificateInfo]):
        """Wydrukuj podsumowanie"""
        total = len(certificates)
        ok = sum(1 for c in certificates.values() if c.alert_level == "OK")
        warning = sum(1 for c in certificates.values() if c.alert_level == "WARNING")
        critical = sum(1 for c in certificates.values() if c.alert_level == "CRITICAL")
        expired = sum(1 for c in certificates.values() if c.alert_level == "EXPIRED")
        
        print("\n" + "=" * 60)
        print("Summary:")
        print("-" * 60)
        print(f"Total Certificates: {total}")
        self.printer.success(f"OK: {ok}")
        if warning > 0:
            self.printer.warning(f"Warning: {warning}")
        if critical > 0:
            self.printer.error(f"Critical: {critical}")
        if expired > 0:
            self.printer.error(f"Expired: {expired}")
        print("=" * 60)


def main():
    """Main entry point"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Certificate Expiry Monitor - Monitor SSL/TLS certificates"
    )
    parser.add_argument(
        '--check-now',
        action='store_true',
        help='Run certificate check now'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode - check single host'
    )
    parser.add_argument(
        '--host',
        type=str,
        help='Hostname to check (for test mode)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=443,
        help='Port (default: 443)'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Generate reports only (skip checking)'
    )
    parser.add_argument(
        '--no-alerts',
        action='store_true',
        help='Skip sending alerts'
    )
    
    args = parser.parse_args()
    
    # Config loader
    config_loader = ConfigLoader()
    
    # Test mode
    if args.test:
        if not args.host:
            print("Error: --host required for test mode")
            sys.exit(1)
        
        print(f"\n=== Test Mode: {args.host}:{args.port} ===\n")
        
        checker = CertificateChecker(timeout=10, verify=False)
        cert_info = checker.check_certificate(args.host, args.port, "https")
        
        printer = ColorPrinter()
        printer.header(f"Certificate Info: {args.host}:{args.port}")
        
        print(f"Subject: {cert_info.common_name}")
        print(f"Issuer: {cert_info.issuer}")
        print(f"Valid From: {cert_info.valid_from}")
        print(f"Valid Until: {cert_info.valid_until}")
        print(f"Days Remaining: {cert_info.days_remaining}")
        print(f"Alert Level: {cert_info.alert_level}")
        print(f"Self-Signed: {cert_info.is_self_signed}")
        
        if cert_info.error:
            printer.error(f"Error: {cert_info.error}")
        
        sys.exit(0)
    
    # Utwórz monitor
    monitor = CertificateMonitor(config_loader)
    
    # Run check
    if args.check_now:
        monitor.run_full_check()
    else:
        parser.print_help()


if __name__ == "__main__":
    import sys
    
    # Jeśli uruchomiono bez argumentów - użyj domyślnych
    if len(sys.argv) == 1:
        print("🚀 Running with default arguments: --check-now --no-alerts\n")
        sys.argv = ['main.py', '--check-now', '--no-alerts']
        
    main()
