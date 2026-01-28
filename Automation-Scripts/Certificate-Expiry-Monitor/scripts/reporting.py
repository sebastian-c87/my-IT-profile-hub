#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reporting Module

Generowanie raportów o certyfikatach:
- HTML reports (interactive)
- CSV reports (Excel)
- JSON reports (API integration)
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from jinja2 import Template
import logging

from cert_checker import CertificateInfo
from utils import FileUtils, DateFormatter


class ReportGenerator:
    """Klasa do generowania raportów"""
    
    def __init__(self, output_dir: Path):
        """
        Inicjalizacja report generator
        
        Args:
            output_dir: Folder do zapisywania raportów
        """
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        
        # Ensure directory exists
        FileUtils.ensure_directory(output_dir)
    
    def generate_html_report(
        self,
        certificates: List[CertificateInfo],
        template_path: Optional[Path] = None,
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generuj raport HTML
        
        Args:
            certificates: Lista certyfikatów
            template_path: Ścieżka do template (opcjonalne)
            output_filename: Nazwa pliku output (opcjonalne)
        
        Returns:
            Path do wygenerowanego pliku
        """
        try:
            # Default filename
            if output_filename is None:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                output_filename = f"certificate_report_{timestamp}.html"
            
            output_path = self.output_dir / output_filename
            
            # Jeśli template podany, użyj go
            if template_path and template_path.exists():
                html_content = self._render_template(certificates, template_path)
            else:
                # Użyj built-in template
                html_content = self._generate_builtin_html(certificates)
            
            # Zapisz
            FileUtils.write_file(output_path, html_content)
            
            self.logger.info(f"HTML report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
            raise
    
    def generate_csv_report(
        self,
        certificates: List[CertificateInfo],
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generuj raport CSV
        
        Args:
            certificates: Lista certyfikatów
            output_filename: Nazwa pliku output
        
        Returns:
            Path do wygenerowanego pliku
        """
        try:
            # Default filename
            if output_filename is None:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                output_filename = f"certificate_report_{timestamp}.csv"
            
            output_path = self.output_dir / output_filename
            
            # Zapisz CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([
                    'Hostname',
                    'Port',
                    'Protocol',
                    'Common Name',
                    'Issuer',
                    'Valid From',
                    'Valid Until',
                    'Days Remaining',
                    'Alert Level',
                    'Is Valid',
                    'Is Expired',
                    'Is Self-Signed',
                    'Key Size',
                    'Signature Algorithm'
                ])
                
                # Data rows
                for cert in certificates:
                    writer.writerow([
                        cert.hostname,
                        cert.port,
                        cert.protocol,
                        cert.common_name,
                        cert.issuer,
                        cert.valid_from.strftime('%Y-%m-%d %H:%M:%S'),
                        cert.valid_until.strftime('%Y-%m-%d %H:%M:%S'),
                        cert.days_remaining,
                        cert.alert_level,
                        cert.is_valid,
                        cert.is_expired,
                        cert.is_self_signed,
                        cert.key_size,
                        cert.signature_algorithm
                    ])
            
            self.logger.info(f"CSV report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate CSV report: {e}")
            raise
    
    def generate_json_report(
        self,
        certificates: List[CertificateInfo],
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generuj raport JSON
        
        Args:
            certificates: Lista certyfikatów
            output_filename: Nazwa pliku output
        
        Returns:
            Path do wygenerowanego pliku
        """
        try:
            # Default filename
            if output_filename is None:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                output_filename = f"certificate_report_{timestamp}.json"
            
            output_path = self.output_dir / output_filename
            
            # Konwertuj do dict
            data = {
                'generated_at': datetime.now().isoformat(),
                'total_certificates': len(certificates),
                'summary': self._generate_summary(certificates),
                'certificates': [cert.to_dict() for cert in certificates]
            }
            
            # Zapisz JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"JSON report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {e}")
            raise
    
    def _render_template(
        self,
        certificates: List[CertificateInfo],
        template_path: Path
    ) -> str:
        """Render HTML z Jinja2 template"""
        template_content = FileUtils.read_file(template_path)
        template = Template(template_content)
        
        return template.render(
            certificates=certificates,
            summary=self._generate_summary(certificates),
            generated_at=datetime.now(),
            formatter=DateFormatter()
        )
    
    def _generate_builtin_html(self, certificates: List[CertificateInfo]) -> str:
        """Generuj HTML używając built-in template"""
        summary = self._generate_summary(certificates)
        
        # Sort by days_remaining
        sorted_certs = sorted(certificates, key=lambda c: c.days_remaining)
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Certificate Status Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
        }}
        .summary-item {{
            text-align: center;
        }}
        .summary-value {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .summary-label {{
            color: #666;
            font-size: 14px;
        }}
        .ok {{ color: #4CAF50; }}
        .warning {{ color: #FF9800; }}
        .critical {{ color: #F44336; }}
        .expired {{ color: #B71C1C; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .status-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        .badge-ok {{
            background-color: #4CAF50;
            color: white;
        }}
        .badge-warning {{
            background-color: #FF9800;
            color: white;
        }}
        .badge-critical {{
            background-color: #F44336;
            color: white;
        }}
        .badge-expired {{
            background-color: #B71C1C;
            color: white;
        }}
        .footer {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Certificate Status Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="summary-item">
                <div class="summary-value">{summary['total']}</div>
                <div class="summary-label">Total</div>
            </div>
            <div class="summary-item">
                <div class="summary-value ok">{summary['ok']}</div>
                <div class="summary-label">OK</div>
            </div>
            <div class="summary-item">
                <div class="summary-value warning">{summary['warning']}</div>
                <div class="summary-label">Warning</div>
            </div>
            <div class="summary-item">
                <div class="summary-value critical">{summary['critical']}</div>
                <div class="summary-label">Critical</div>
            </div>
            <div class="summary-item">
                <div class="summary-value expired">{summary['expired']}</div>
                <div class="summary-label">Expired</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Host</th>
                    <th>Common Name</th>
                    <th>Issuer</th>
                    <th>Valid Until</th>
                    <th>Days Left</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for cert in sorted_certs:
            badge_class = f"badge-{cert.alert_level.lower()}"
            
            html += f"""
                <tr>
                    <td>{cert.hostname}:{cert.port}</td>
                    <td>{cert.common_name}</td>
                    <td>{cert.issuer[:50]}...</td>
                    <td>{cert.valid_until.strftime('%Y-%m-%d')}</td>
                    <td class="{cert.alert_level.lower()}">{cert.days_remaining}</td>
                    <td><span class="status-badge {badge_class}">{cert.alert_level}</span></td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <div class="footer">
            <p>Certificate Expiry Monitor</p>
            <p>This report was automatically generated.</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def _generate_summary(self, certificates: List[CertificateInfo]) -> Dict:
        """Generuj podsumowanie statystyk"""
        return {
            'total': len(certificates),
            'ok': sum(1 for c in certificates if c.alert_level == "OK"),
            'warning': sum(1 for c in certificates if c.alert_level == "WARNING"),
            'critical': sum(1 for c in certificates if c.alert_level == "CRITICAL"),
            'expired': sum(1 for c in certificates if c.alert_level == "EXPIRED"),
            'self_signed': sum(1 for c in certificates if c.is_self_signed)
        }


# Przykład użycia
if __name__ == "__main__":
    import logging
    from cert_checker import CertificateChecker
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s'
    )
    
    # Sprawdź kilka certyfikatów
    print("\n=== Checking certificates ===")
    checker = CertificateChecker(timeout=10, verify=False)
    
    hosts = [
        ("google.com", 443, "https"),
        ("github.com", 443, "https"),
        ("stackoverflow.com", 443, "https")
    ]
    
    results = checker.check_multiple_hosts(hosts, concurrent=3)
    certificates = list(results.values())
    
    # Generuj raporty
    output_dir = Path("output/reports/test")
    generator = ReportGenerator(output_dir)
    
    print("\n=== Generating reports ===")
    
    # HTML
    html_path = generator.generate_html_report(certificates)
    print(f"✓ HTML report: {html_path}")
    
    # CSV
    csv_path = generator.generate_csv_report(certificates)
    print(f"✓ CSV report: {csv_path}")
    
    # JSON
    json_path = generator.generate_json_report(certificates)
    print(f"✓ JSON report: {json_path}")
    
    print(f"\nReports saved to: {output_dir}")
