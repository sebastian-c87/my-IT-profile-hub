#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Alerting Module

System alertów dla wygasających certyfikatów:
- Email alerts (SMTP)
- Slack notifications
- Microsoft Teams notifications
"""

import smtplib
import requests
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import logging
from jinja2 import Template

from cert_checker import CertificateInfo
from utils import ConfigLoader, FileUtils


class EmailAlerter:
    """Klasa do wysyłania alertów email przez SMTP"""
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        from_address: str,
        use_tls: bool = True
    ):
        """
        Inicjalizacja email alerter
        
        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            smtp_username: SMTP username
            smtp_password: SMTP password
            from_address: From email address
            use_tls: Czy używać TLS
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_address = from_address
        self.use_tls = use_tls
        self.logger = logging.getLogger(__name__)
    
    def send_alert(
        self,
        to_addresses: List[str],
        cert_info: CertificateInfo,
        template_path: Optional[Path] = None
    ) -> bool:
        """
        Wyślij alert email dla pojedynczego certyfikatu
        
        Args:
            to_addresses: Lista adresów email odbiorców
            cert_info: Informacje o certyfikacie
            template_path: Ścieżka do template HTML (opcjonalne)
        
        Returns:
            True jeśli sukces, False jeśli błąd
        """
        try:
            # Utwórz wiadomość
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self._create_subject(cert_info)
            msg['From'] = self.from_address
            msg['To'] = ', '.join(to_addresses)
            
            # Plain text version
            text_body = self._create_text_body(cert_info)
            msg.attach(MIMEText(text_body, 'plain'))
            
            # HTML version (jeśli template)
            if template_path and template_path.exists():
                html_body = self._create_html_body(cert_info, template_path)
                msg.attach(MIMEText(html_body, 'html'))
            
            # Wyślij
            self._send_email(msg, to_addresses)
            
            self.logger.info(
                f"Alert email sent for {cert_info.hostname}:{cert_info.port} "
                f"to {len(to_addresses)} recipients"
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
            return False
    
    def send_daily_report(
        self,
        to_addresses: List[str],
        certificates: List[CertificateInfo],
        template_path: Optional[Path] = None
    ) -> bool:
        """
        Wyślij dzienny raport ze wszystkimi certyfikatami
        
        Args:
            to_addresses: Lista odbiorców
            certificates: Lista certyfikatów
            template_path: Template HTML
        
        Returns:
            True jeśli sukces
        """
        try:
            # Utwórz wiadomość
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"[Daily Report] Certificate Status - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.from_address
            msg['To'] = ', '.join(to_addresses)
            
            # Plain text
            text_body = self._create_daily_report_text(certificates)
            msg.attach(MIMEText(text_body, 'plain'))
            
            # HTML (jeśli template)
            if template_path and template_path.exists():
                html_body = self._create_daily_report_html(certificates, template_path)
                msg.attach(MIMEText(html_body, 'html'))
            
            # Wyślij
            self._send_email(msg, to_addresses)
            
            self.logger.info(f"Daily report sent to {len(to_addresses)} recipients")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send daily report: {e}")
            return False
    
    def _send_email(self, msg: MIMEMultipart, to_addresses: List[str]) -> None:
        """Wyślij email przez SMTP"""
        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
            if self.use_tls:
                server.starttls()
            
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
    
    def _create_subject(self, cert_info: CertificateInfo) -> str:
        """Utwórz subject dla alertu"""
        if cert_info.alert_level == "EXPIRED":
            prefix = "[EXPIRED]"
        elif cert_info.alert_level == "CRITICAL":
            prefix = "[CRITICAL]"
        elif cert_info.alert_level == "WARNING":
            prefix = "[WARNING]"
        else:
            prefix = "[INFO]"
        
        return (
            f"{prefix} SSL Certificate Alert - "
            f"{cert_info.hostname}:{cert_info.port}"
        )
    
    def _create_text_body(self, cert_info: CertificateInfo) -> str:
        """Utwórz plain text body"""
        return f"""
Certificate Alert
=================

Host: {cert_info.hostname}:{cert_info.port}
Subject: {cert_info.common_name}
Issuer: {cert_info.issuer}

Valid From: {cert_info.valid_from.strftime('%Y-%m-%d %H:%M:%S')}
Valid Until: {cert_info.valid_until.strftime('%Y-%m-%d %H:%M:%S')}
Days Remaining: {cert_info.days_remaining}

Status: {cert_info.alert_level}

{"⚠ ACTION REQUIRED: Certificate expires soon!" if cert_info.days_remaining <= 7 else ""}
{"✗ URGENT: Certificate has EXPIRED!" if cert_info.is_expired else ""}

Please renew this certificate as soon as possible.

---
Certificate Expiry Monitor
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
    
    def _create_html_body(
        self,
        cert_info: CertificateInfo,
        template_path: Path
    ) -> str:
        """Utwórz HTML body z template"""
        template_content = FileUtils.read_file(template_path)
        template = Template(template_content)
        
        return template.render(
            cert=cert_info,
            now=datetime.now()
        )
    
    def _create_daily_report_text(self, certificates: List[CertificateInfo]) -> str:
        """Utwórz plain text daily report"""
        # Statystyki
        total = len(certificates)
        ok = sum(1 for c in certificates if c.alert_level == "OK")
        warning = sum(1 for c in certificates if c.alert_level == "WARNING")
        critical = sum(1 for c in certificates if c.alert_level == "CRITICAL")
        expired = sum(1 for c in certificates if c.alert_level == "EXPIRED")
        
        report = f"""
Daily Certificate Status Report
================================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
--------
Total Certificates: {total}
✓ OK: {ok}
⚠ Warning: {warning}
⚠ Critical: {critical}
✗ Expired: {expired}

Details:
--------
"""
        
        # Sortuj po days_remaining
        sorted_certs = sorted(certificates, key=lambda c: c.days_remaining)
        
        for cert in sorted_certs:
            status = "✓" if cert.alert_level == "OK" else "✗"
            report += f"\n{status} {cert.hostname}:{cert.port} - {cert.days_remaining} days - {cert.alert_level}"
        
        report += f"""

---
Certificate Expiry Monitor
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return report
    
    def _create_daily_report_html(
        self,
        certificates: List[CertificateInfo],
        template_path: Path
    ) -> str:
        """Utwórz HTML daily report z template"""
        template_content = FileUtils.read_file(template_path)
        template = Template(template_content)
        
        return template.render(
            certificates=certificates,
            now=datetime.now()
        )


class SlackAlerter:
    """Klasa do wysyłania alertów do Slack"""
    
    def __init__(self, webhook_url: str, channel: Optional[str] = None):
        """
        Inicjalizacja Slack alerter
        
        Args:
            webhook_url: Slack webhook URL
            channel: Kanał Slack (opcjonalnie)
        """
        self.webhook_url = webhook_url
        self.channel = channel
        self.logger = logging.getLogger(__name__)
    
    def send_alert(
        self,
        cert_info: CertificateInfo,
        mention: Optional[str] = None
    ) -> bool:
        """
        Wyślij alert do Slack
        
        Args:
            cert_info: Informacje o certyfikacie
            mention: Mention (@here, @channel, @username)
        
        Returns:
            True jeśli sukces
        """
        try:
            # Utwórz payload
            payload = self._create_alert_payload(cert_info, mention)
            
            # Wyślij
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"Slack alert sent for {cert_info.hostname}:{cert_info.port}")
                return True
            else:
                self.logger.error(f"Slack alert failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    def send_summary(
        self,
        certificates: List[CertificateInfo]
    ) -> bool:
        """
        Wyślij podsumowanie do Slack
        
        Args:
            certificates: Lista certyfikatów
        
        Returns:
            True jeśli sukces
        """
        try:
            payload = self._create_summary_payload(certificates)
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info("Slack summary sent")
                return True
            else:
                self.logger.error(f"Slack summary failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send Slack summary: {e}")
            return False
    
    def _create_alert_payload(
        self,
        cert_info: CertificateInfo,
        mention: Optional[str]
    ) -> dict:
        """Utwórz payload dla single alert"""
        # Kolor w zależności od alert level
        color_map = {
            "OK": "#36a64f",       # Zielony
            "WARNING": "#ffcc00",  # Żółty
            "CRITICAL": "#ff0000", # Czerwony
            "EXPIRED": "#8b0000"   # Ciemnoczerwony
        }
        color = color_map.get(cert_info.alert_level, "#cccccc")
        
        # Emoji
        emoji_map = {
            "OK": ":white_check_mark:",
            "WARNING": ":warning:",
            "CRITICAL": ":rotating_light:",
            "EXPIRED": ":x:"
        }
        emoji = emoji_map.get(cert_info.alert_level, ":question:")
        
        # Mention
        mention_text = f"{mention} " if mention else ""
        
        # Payload z Slack Block Kit
        payload = {
            "text": f"{mention_text}Certificate Alert: {cert_info.hostname}:{cert_info.port}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{emoji} SSL Certificate Alert"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Host:*\n{cert_info.hostname}:{cert_info.port}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Status:*\n{cert_info.alert_level}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Days Remaining:*\n{cert_info.days_remaining}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Expires:*\n{cert_info.valid_until.strftime('%Y-%m-%d')}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Subject:* {cert_info.common_name}\n*Issuer:* {cert_info.issuer}"
                    }
                }
            ],
            "attachments": [
                {
                    "color": color,
                    "fields": []
                }
            ]
        }
        
        if self.channel:
            payload["channel"] = self.channel
        
        return payload
    
    def _create_summary_payload(self, certificates: List[CertificateInfo]) -> dict:
        """Utwórz payload dla summary"""
        # Statystyki
        total = len(certificates)
        ok = sum(1 for c in certificates if c.alert_level == "OK")
        warning = sum(1 for c in certificates if c.alert_level == "WARNING")
        critical = sum(1 for c in certificates if c.alert_level == "CRITICAL")
        expired = sum(1 for c in certificates if c.alert_level == "EXPIRED")
        
        payload = {
            "text": "Certificate Status Summary",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📊 Certificate Status Summary"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Total:*\n{total}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*✓ OK:*\n{ok}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⚠ Warning:*\n{warning}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*⚠ Critical:*\n{critical}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*✗ Expired:*\n{expired}"
                        }
                    ]
                }
            ]
        }
        
        if self.channel:
            payload["channel"] = self.channel
        
        return payload


class TeamsAlerter:
    """Klasa do wysyłania alertów do Microsoft Teams"""
    
    def __init__(self, webhook_url: str):
        """
        Inicjalizacja Teams alerter
        
        Args:
            webhook_url: Teams webhook URL
        """
        self.webhook_url = webhook_url
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, cert_info: CertificateInfo) -> bool:
        """
        Wyślij alert do Teams
        
        Args:
            cert_info: Informacje o certyfikacie
        
        Returns:
            True jeśli sukces
        """
        try:
            payload = self._create_alert_payload(cert_info)
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"Teams alert sent for {cert_info.hostname}:{cert_info.port}")
                return True
            else:
                self.logger.error(f"Teams alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send Teams alert: {e}")
            return False
    
    def _create_alert_payload(self, cert_info: CertificateInfo) -> dict:
        """Utwórz payload dla Teams (Adaptive Card)"""
        # Kolor
        color_map = {
            "OK": "good",
            "WARNING": "warning",
            "CRITICAL": "attention",
            "EXPIRED": "attention"
        }
        theme_color = color_map.get(cert_info.alert_level, "default")
        
        payload = {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": f"Certificate Alert: {cert_info.hostname}:{cert_info.port}",
            "themeColor": theme_color,
            "title": f"🔒 SSL Certificate Alert - {cert_info.alert_level}",
            "sections": [
                {
                    "activityTitle": f"{cert_info.hostname}:{cert_info.port}",
                    "activitySubtitle": f"Expires in {cert_info.days_remaining} days",
                    "facts": [
                        {
                            "name": "Subject:",
                            "value": cert_info.common_name
                        },
                        {
                            "name": "Issuer:",
                            "value": cert_info.issuer
                        },
                        {
                            "name": "Valid Until:",
                            "value": cert_info.valid_until.strftime('%Y-%m-%d %H:%M:%S')
                        },
                        {
                            "name": "Days Remaining:",
                            "value": str(cert_info.days_remaining)
                        },
                        {
                            "name": "Status:",
                            "value": cert_info.alert_level
                        }
                    ],
                    "markdown": True
                }
            ]
        }
        
        return payload


# Przykład użycia
if __name__ == "__main__":
    import logging
    from cert_checker import CertificateChecker
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s'
    )
    
    # Sprawdź certyfikat
    checker = CertificateChecker(timeout=10, verify=False)
    cert_info = checker.check_certificate("google.com", 443, "https")
    
    print("\n=== Email Alerter (Demo - wymaga konfiguracji SMTP) ===")
    print(f"Would send email alert for: {cert_info.hostname}:{cert_info.port}")
    print(f"Status: {cert_info.alert_level}, Days: {cert_info.days_remaining}")
    
    # Email demo (wyłączone - wymaga prawdziwych credentials)
    # email_alerter = EmailAlerter(
    #     smtp_host="smtp.gmail.com",
    #     smtp_port=587,
    #     smtp_username="your-email@gmail.com",
    #     smtp_password="your-app-password",
    #     from_address="cert-monitor@company.com"
    # )
    # email_alerter.send_alert(
    #     to_addresses=["admin@company.com"],
    #     cert_info=cert_info
    # )
    
    print("\n=== Slack Alerter (Demo - wymaga webhook URL) ===")
    print("Slack payload would be:")
    print(json.dumps({
        "text": f"Certificate Alert: {cert_info.hostname}:{cert_info.port}",
        "alert_level": cert_info.alert_level,
        "days_remaining": cert_info.days_remaining
    }, indent=2))
