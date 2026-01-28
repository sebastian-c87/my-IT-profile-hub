# 📜 Scripts Directory

Folder zawierający wszystkie skrypty Python do monitorowania certyfikatów SSL/TLS.

---

## 📋 Spis Skryptów

| Plik | Linie | Opis |
|------|-------|------|
| `cert_checker.py` | ~500 | Sprawdzanie certyfikatów SSL/TLS, pobieranie informacji |
| `cert_validator.py` | ~550 | Walidacja łańcucha certyfikatów, revocation, security checks |
| `utils.py` | ~420 | Narzędzia pomocnicze (config, logging, formatting) |
| `alerting.py` | ~600 | System alertów (Email, Slack, Teams) |
| `reporting.py` | ~450 | Generowanie raportów (HTML, CSV, JSON) |
| `main.py` | ~450 | Główny entry point, CLI interface, orchestration |

**Łącznie:** ~3,000 linii kodu Python

---

## 🔍 Szczegóły Skryptów

### 1. cert_checker.py

**Cel:** Sprawdzanie certyfikatów SSL/TLS na zdalnych hostach.

**Główne klasy:**
- `CertificateInfo` - dataclass przechowująca wszystkie dane o certyfikacie
- `CertificateChecker` - klasa do sprawdzania certyfikatów

**Co robi:**
- Łączy się z serwerem przez SSL/TLS
- Pobiera certyfikat
- Ekstraktuje informacje (subject, issuer, dates, SAN, etc.)
- Oblicza dni do wygaśnięcia
- Określa poziom alertu (OK, WARNING, CRITICAL, EXPIRED)
- Obsługuje multiple hosts concurrently

**Przykład użycia:**

    from cert_checker import CertificateChecker
    
    checker = CertificateChecker(timeout=10, verify=False)
    cert_info = checker.check_certificate("google.com", 443, "https")
    
    print(f"Host: {cert_info.hostname}")
    print(f"Days remaining: {cert_info.days_remaining}")
    print(f"Alert level: {cert_info.alert_level}")

---

### 2. cert_validator.py

**Cel:** Zaawansowana walidacja certyfikatów i łańcuchów zaufania.

**Główne klasy:**
- `ValidationResult` - dataclass z wynikiem walidacji
- `CertificateValidator` - klasa do walidacji

**Co robi:**
- Pobiera i waliduje cały łańcuch certyfikatów (leaf → intermediate → root)
- Sprawdza czy root CA jest zaufany
- Weryfikuje revocation (CRL/OCSP)
- Sprawdza hostname match
- Wykrywa słabe algorytmy (MD5, SHA1)
- Wykrywa słabe klucze (< 2048 bit RSA)

**Przykład użycia:**

    from cert_validator import CertificateValidator
    
    validator = CertificateValidator(timeout=10)
    result = validator.validate_certificate("google.com", 443)
    
    print(result)  # Pretty-printed validation result
    print(f"Valid: {result.valid}")
    print(f"Chain length: {result.chain_length}")
    print(f"Trusted CA: {result.trusted_ca}")

---

### 3. utils.py

**Cel:** Funkcje pomocnicze używane przez inne moduły.

**Główne klasy:**
- `ConfigLoader` - ładowanie YAML i ENV
- `ColorPrinter` - kolorowany output w CLI
- `DateFormatter` - formatowanie dat
- `LoggerSetup` - konfiguracja logging
- `FileUtils` - operacje na plikach

**Co robi:**
- Ładuje konfigurację z YAML z podstawianiem zmiennych z .env
- Formatuje output w terminalu z kolorami
- Konfiguruje logger z rotacją plików
- Formatuje daty w różnych formatach

**Przykład użycia:**

    from utils import ConfigLoader, ColorPrinter, LoggerSetup
    
    # Config
    config_loader = ConfigLoader()
    domains = config_loader.load_yaml("config/domains.yml")
    
    # Printer
    printer = ColorPrinter()
    printer.success("Operation successful")
    printer.error("Something went wrong")
    
    # Logger
    logger = LoggerSetup.setup_logger(
        name="my_app",
        log_file="output/logs/app.log",
        level="INFO"
    )

---

### 4. alerting.py

**Cel:** Wysyłanie alertów przez różne kanały.

**Główne klasy:**
- `EmailAlerter` - alerty przez SMTP
- `SlackAlerter` - alerty do Slack
- `TeamsAlerter` - alerty do Microsoft Teams

**Co robi:**
- Wysyła email alerts z plain text i HTML
- Wysyła Slack notifications z Block Kit formatting
- Wysyła Teams notifications z Adaptive Cards
- Obsługuje pojedyncze alerty i daily reports
- Retry mechanism przy błędach

**Przykład użycia:**

    from alerting import EmailAlerter
    from cert_checker import CertificateChecker
    
    # Sprawdź certyfikat
    checker = CertificateChecker()
    cert_info = checker.check_certificate("example.com", 443, "https")
    
    # Wyślij alert
    alerter = EmailAlerter(
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        smtp_username="your-email@gmail.com",
        smtp_password="your-app-password",
        from_address="monitor@company.com"
    )
    
    alerter.send_alert(
        to_addresses=["admin@company.com"],
        cert_info=cert_info
    )

---

### 5. reporting.py

**Cel:** Generowanie raportów w różnych formatach.

**Główne klasy:**
- `ReportGenerator` - generowanie raportów

**Co robi:**
- Generuje HTML reports z interaktywnym UI
- Generuje CSV reports (Excel-compatible)
- Generuje JSON reports (API integration)
- Built-in HTML template z CSS
- Możliwość użycia custom Jinja2 templates

**Przykład użycia:**

    from reporting import ReportGenerator
    from pathlib import Path
    
    generator = ReportGenerator(Path("output/reports"))
    
    # HTML report
    html_path = generator.generate_html_report(certificates)
    
    # CSV report
    csv_path = generator.generate_csv_report(certificates)
    
    # JSON report
    json_path = generator.generate_json_report(certificates)

---

### 6. main.py

**Cel:** Główny entry point aplikacji - orkiestracja całego procesu.

**Główne klasy:**
- `CertificateMonitor` - główna klasa orkiestrująca

**Co robi:**
- Ładuje konfigurację z YAML i .env
- Inicjalizuje wszystkie moduły (checker, validator, alerters, reporter)
- Pobiera enabled hosts z config/domains.yml
- Sprawdza wszystkie certyfikaty concurrently
- Wysyła alerty dla certyfikatów wymagających uwagi
- Generuje raporty w wybranych formatach
- CLI interface z argumentami

**Przykład użycia CLI:**

    # Pełny check
    python scripts/main.py --check-now
    
    # Test pojedynczego hosta
    python scripts/main.py --test --host google.com --port 443
    
    # Check bez alertów
    python scripts/main.py --check-now --no-alerts
    
    # Help
    python scripts/main.py --help

---

## 🚀 Jak Używać

### Wymagania

**Python 3.8+** i następujące biblioteki:

    pip install -r requirements.txt

Zawartość `requirements.txt`:

    cryptography>=41.0.0
    pyOpenSSL>=23.0.0
    python-dotenv>=1.0.0
    PyYAML>=6.0
    colorama>=0.4.6
    Jinja2>=3.1.2
    requests>=2.31.0

### Podstawowe Użycie

#### 1. Konfiguracja

Przed pierwszym uruchomieniem:

    # Skopiuj .env.example do .env
    cp .env.example .env
    
    # Edytuj .env (dodaj SMTP credentials, webhook URLs)
    nano .env
    
    # Edytuj config/domains.yml (włącz enabled: true dla swoich hostów)
    nano config/domains.yml

#### 2. Test Pojedynczego Hosta

    # Test google.com
    python scripts/main.py --test --host google.com
    
    # Test z custom portem
    python scripts/main.py --test --host example.com --port 8443

**Output:**

    === Test Mode: google.com:443 ===
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Certificate Info: google.com:443
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Subject: *.google.com
    Issuer: CN=GTS CA 1C3, O=Google Trust Services LLC, C=US
    Valid From: 2026-01-13 08:21:45
    Valid Until: 2026-04-07 08:21:44
    Days Remaining: 69
    Alert Level: OK
    Self-Signed: False

#### 3. Pełny Check Wszystkich Hostów

    python scripts/main.py --check-now

**Output:**

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Certificate Expiry Monitor
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Checking 5 hosts...
    
    Results:
    ------------------------------------------------------------
    ✓ google.com:443                     89 days    OK
    ✓ github.com:443                     67 days    OK
    ⚠ test.local:443                     12 days    WARNING
    ✗ old.local:443                      -5 days    EXPIRED
    ✓ stackoverflow.com:443              45 days    OK
    
    Sending alerts for 2 certificates...
    ✓ Alerts sent for 2 certificates
    
    Generating reports...
    ✓ HTML report: output/reports/certificate_report_2026-01-28_17-45-30.html
    ✓ CSV report: output/reports/certificate_report_2026-01-28_17-45-30.csv
    ✓ JSON report: output/reports/certificate_report_2026-01-28_17-45-30.json
    
    ============================================================
    Summary:
    ------------------------------------------------------------
    Total Certificates: 5
    ✓ OK: 3
    ⚠ Warning: 1
    ✗ Critical: 0
    ✗ Expired: 1
    ============================================================

#### 4. Check Bez Alertów (tylko sprawdzenie)

    python scripts/main.py --check-now --no-alerts

---

## 🧪 Testowanie Lokalne

### Test 1: Sprawdzenie Publicznych Domen

**Cel:** Przetestować podstawowe działanie bez konfiguracji SMTP.

**Kroki:**

1. Otwórz `config/domains.yml`
2. Włącz `public_domains`:

    public_domains:
      - name: Google
        host: google.com
        port: 443
        protocol: https
        alert_days: 30
        enabled: true  # ← Zmień na true
        tags:
          - public
          - test
    
      - name: GitHub
        host: github.com
        port: 443
        protocol: https
        alert_days: 30
        enabled: true  # ← Zmień na true

3. Uruchom check (bez alertów):

    python scripts/main.py --check-now --no-alerts

**Oczekiwany rezultat:**
- ✓ Połączenie z google.com i github.com
- ✓ Pobrane informacje o certyfikatach
- ✓ Wygenerowane raporty w `output/reports/`
- ✓ Logi w `output/logs/certificate_monitor.log`

---

### Test 2: Interaktywny Test Pojedynczego Hosta

**Cel:** Szybko sprawdzić dowolny host.

    # Twój GitHub Pages
    python scripts/main.py --test --host sebastian-c87.github.io
    
    # Dowolna inna domena
    python scripts/main.py --test --host stackoverflow.com
    python scripts/main.py --test --host twitter.com
    python scripts/main.py --test --host reddit.com

**Co sprawdzić:**
- Days remaining
- Alert level
- Issuer (CA name)
- Self-signed status

---

### Test 3: Email Alerts (wymaga SMTP)

**Cel:** Przetestować wysyłanie email alerts.

**Wymagania:**
- Gmail account z włączonym 2FA
- App Password wygenerowany w Google Account

**Kroki:**

1. Edytuj `.env`:

    # SMTP Configuration (Gmail example)
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USERNAME=twoj-email@gmail.com
    SMTP_PASSWORD=twoj-app-password  # 16-character app password
    
    # Alert Emails
    ALERT_EMAIL_FROM=cert-monitor@company.com
    ALERT_EMAIL_TO=twoj-email@gmail.com

2. Edytuj `config/domains.yml` - włącz host który wkrótce wygasa lub ustaw `alert_days: 365` dla google.com (żeby wymusić alert)

3. Uruchom:

    python scripts/main.py --check-now

4. Sprawdź skrzynkę email - powinieneś otrzymać alert.

---

### Test 4: Slack Alerts

**Cel:** Przetestować Slack notifications.

**Wymagania:**
- Slack workspace
- Incoming Webhook URL

**Kroki:**

1. Utwórz Slack webhook:
   - Idź do https://api.slack.com/apps
   - Create New App → From scratch
   - Enable Incoming Webhooks
   - Add New Webhook to Workspace
   - Skopiuj Webhook URL

2. Edytuj `.env`:

    # Slack Configuration
    SLACK_ENABLED=true
    SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
    SLACK_CHANNEL=#alerts

3. Uruchom:

    python scripts/main.py --check-now

4. Sprawdź kanał Slack - powinieneś zobaczyć notification.

---

### Test 5: Generowanie Raportów

**Cel:** Przetestować różne formaty raportów.

    # Sprawdź certyfikaty i wygeneruj raporty
    python scripts/main.py --check-now --no-alerts

**Sprawdź pliki:**

    # Lista wygenerowanych raportów
    ls -lh output/reports/
    
    # Otwórz HTML report w przeglądarce
    # Windows:
    start output/reports/certificate_report_*.html
    
    # Linux:
    xdg-open output/reports/certificate_report_*.html
    
    # macOS:
    open output/reports/certificate_report_*.html
    
    # Sprawdź CSV w Excel/LibreOffice
    libreoffice output/reports/certificate_report_*.csv
    
    # Sprawdź JSON
    cat output/reports/certificate_report_*.json | jq '.'

---

### Test 6: Testowanie z Docker (lokalne certyfikaty)

**Cel:** Przetestować z self-signed i expiring certificates.

**Wymagania:** Docker i docker-compose

**Kroki:**

1. Przejdź do folderu docker:

    cd docker/test-certs

2. Uruchom test environment:

    docker-compose up -d

3. Sprawdź kontenery:

    docker ps

**Powinny być 5 kontenerów:**
- nginx-valid (port 8443) - valid cert
- nginx-expiring (port 8444) - expires soon
- nginx-expired (port 8445) - expired
- apache-self-signed (port 8446) - self-signed
- mail-server (port 8465) - mail cert

4. Edytuj `config/domains.yml` - włącz `docker_test`:

    docker_test:
      - name: Docker Nginx Valid
        host: localhost
        port: 8443
        protocol: https
        alert_days: 30
        enabled: true  # ← Zmień na true

5. Uruchom check:

    python scripts/main.py --check-now --no-alerts

**Oczekiwany rezultat:**
- ✓ localhost:8443 - OK (valid cert)
- ⚠ localhost:8444 - WARNING/CRITICAL (expiring)
- ✗ localhost:8445 - EXPIRED
- ⚠ localhost:8446 - WARNING (self-signed)
- ✓ localhost:8465 - OK (mail cert)

6. Stop environment:

    docker-compose down

---

### Test 7: Indywidualne Moduły

**Cel:** Przetestować poszczególne moduły niezależnie.

#### Test cert_checker.py:

    python scripts/cert_checker.py

**Output:**

    === Checking google.com ===
    Host: google.com:443
    Subject: *.google.com
    Issuer: CN=GTS CA 1C3...
    Days Remaining: 69
    Alert Level: OK
    Self-Signed: False
    
    === Checking multiple hosts ===
    ✓ google.com:443 - 69 days - OK
    ✓ github.com:443 - 67 days - OK
    ✓ stackoverflow.com:443 - 45 days - OK

#### Test cert_validator.py:

    python scripts/cert_validator.py

**Output:**

    === Validating google.com ===
    Validation: VALID
      Chain: ✓ (3 certs)
      Trusted CA: ✓
      Revocation: ✓
      Hostname: ✓
      Security: ✓

#### Test utils.py:

    python scripts/utils.py

**Output:**

    === Config Loader ===
    Loaded 10 domain groups
    
    === Color Printer ===
    ✓ Certificate is valid
    ⚠ Certificate expires soon
    ✗ Certificate has expired
    
    === Logger Setup ===
    [2026-01-28 17:45:30] [INFO] This is an info message

#### Test reporting.py:

    python scripts/reporting.py

**Output:**

    === Checking certificates ===
    === Generating reports ===
    ✓ HTML report: output/reports/test/certificate_report_*.html
    ✓ CSV report: output/reports/test/certificate_report_*.csv
    ✓ JSON report: output/reports/test/certificate_report_*.json

---

## 📊 Interpretacja Wyników

### Alert Levels

| Level | Dni | Kolor | Znaczenie |
|-------|-----|-------|-----------|
| **OK** | > 30 | 🟢 Zielony | Certyfikat OK |
| **WARNING** | 8-30 | 🟡 Żółty | Certyfikat wkrótce wygasa |
| **CRITICAL** | 1-7 | 🔴 Czerwony | Certyfikat wygasa bardzo wkrótce! |
| **EXPIRED** | < 0 | 🔴 Ciemnoczerwony | Certyfikat WYGASŁ! |

### HTML Report

Raport HTML zawiera:
- **Summary Cards** - statystyki (total, OK, warning, critical, expired)
- **Interactive Table** - wszystkie certyfikaty z sortowaniem
- **Color Coding** - wizualne oznaczenie statusu
- **Responsive Design** - działa na mobile

### CSV Report

Kolumny w CSV:
- Hostname, Port, Protocol
- Common Name, Issuer
- Valid From, Valid Until
- Days Remaining, Alert Level
- Is Valid, Is Expired, Is Self-Signed
- Key Size, Signature Algorithm

**Użycie:**
- Import do Excel/Google Sheets
- Analiza w Pandas
- Integracja z BI tools

### JSON Report

Struktura JSON:

    {
      "generated_at": "2026-01-28T17:45:30",
      "total_certificates": 5,
      "summary": {
        "total": 5,
        "ok": 3,
        "warning": 1,
        "critical": 0,
        "expired": 1
      },
      "certificates": [
        {
          "hostname": "google.com",
          "port": 443,
          "days_remaining": 69,
          "alert_level": "OK",
          ...
        }
      ]
    }

**Użycie:**
- API integration
- Dashboard data source
- Monitoring systems (Grafana, etc.)

---

## 🔧 Troubleshooting

### Problem 1: ModuleNotFoundError

**Error:**

    ModuleNotFoundError: No module named 'cryptography'

**Rozwiązanie:**

    pip install -r requirements.txt

---

### Problem 2: SSL Connection Failed

**Error:**

    Error checking host: [SSL: CERTIFICATE_VERIFY_FAILED]

**Rozwiązanie:**
- Dla self-signed certs: ustaw `VERIFY_CHAIN=false` w .env
- Sprawdź firewall/network connectivity
- Sprawdź czy port jest otwarty: `telnet hostname port`

---

### Problem 3: SMTP Authentication Failed

**Error:**

    SMTPAuthenticationError: Username and Password not accepted

**Rozwiązanie:**
- Gmail: Włącz 2FA i wygeneruj App Password
- Sprawdź czy SMTP_USERNAME i SMTP_PASSWORD są poprawne
- Sprawdź czy SMTP_HOST i SMTP_PORT są poprawne

---

### Problem 4: Permission Denied (logs/reports)

**Error:**

    PermissionError: [Errno 13] Permission denied: 'output/logs/'

**Rozwiązanie:**

    # Linux/macOS
    chmod -R 755 output/
    
    # Lub utwórz ręcznie
    mkdir -p output/logs output/reports

---

### Problem 5: Config File Not Found

**Error:**

    FileNotFoundError: Config file not found: config/domains.yml

**Rozwiązanie:**
- Sprawdź czy jesteś w głównym folderze projektu
- Sprawdź czy struktura folderów jest poprawna
- Uruchom skrypt z poziomu root projektu:

    cd /path/to/certificate-expiry-monitor
    python scripts/main.py --check-now

---

## 📚 Dodatkowe Zasoby

### Dokumentacja Python Libraries

- **cryptography**: https://cryptography.io/
- **pyOpenSSL**: https://www.pyopenssl.org/
- **Jinja2**: https://jinja.palletsprojects.com/
- **requests**: https://requests.readthedocs.io/

### SSL/TLS Resources

- **SSL Labs**: https://www.ssllabs.com/
- **Let's Encrypt**: https://letsencrypt.org/
- **Mozilla SSL Config**: https://ssl-config.mozilla.org/

### Monitoring Integration

- **Grafana**: Użyj JSON reports jako data source
- **Prometheus**: Implementacja w `config/settings.yml`
- **Zabbix**: External script integration

---

## ✅ Quick Start Checklist

- [ ] Zainstaluj Python 3.8+
- [ ] Zainstaluj dependencies: `pip install -r requirements.txt`
- [ ] Skopiuj `.env.example` do `.env`
- [ ] Edytuj `.env` (opcjonalnie SMTP/Slack)
- [ ] Edytuj `config/domains.yml` (włącz `public_domains`)
- [ ] Uruchom test: `python scripts/main.py --test --host google.com`
- [ ] Uruchom full check: `python scripts/main.py --check-now --no-alerts`
- [ ] Sprawdź raporty w `output/reports/`
- [ ] Sprawdź logi w `output/logs/`
- [ ] Gotowe! 🎉

---

## 💡 Pro Tips

1. **Scheduled Checks**: Użyj cron (Linux) lub Task Scheduler (Windows) do automatycznego uruchamiania

    # Cron example (codziennie o 3:00)
    0 3 * * * cd /path/to/project && python scripts/main.py --check-now

2. **Email Filtering**: Dodaj reguły w Gmail/Outlook dla alertów certyfikatów

3. **Report Retention**: Automatyczne usuwanie starych raportów (ustawienie w config)

4. **Custom Templates**: Stwórz własne Jinja2 templates dla raportów

5. **API Integration**: Użyj JSON reports jako data source dla dashboards

---

## 🎓 Następne Kroki

Po opanowaniu podstaw:

1. **Docker Setup** - uruchom test environment (`docker/test-certs/`)
2. **Custom Templates** - stwórz własne email/report templates
3. **Auto-Renewal** - skonfiguruj automatyczne odnawianie (Certbot/ACME.sh)
4. **Database Integration** - włącz SQLite/PostgreSQL dla historii
5. **Prometheus Metrics** - expose metrics dla Grafana

---

**Autor:** Sebastian (sebastian-c87)  
**Projekt:** Certificate Expiry Monitor  
**Wersja:** 1.0.0  
**Data:** 2026-01-28
