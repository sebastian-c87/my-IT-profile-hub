# 📦 Instalacja i Użycie - Certificate Expiry Monitor

Szczegółowa instrukcja instalacji i konfiguracji projektu krok po kroku.

---

## 📋 Wymagania Systemowe

### Minimalne Wymagania

- **System operacyjny:** Windows 10/11, Linux (Ubuntu 20.04+), macOS 11+
- **Python:** 3.8 lub nowszy
- **RAM:** 512 MB
- **Dysk:** 100 MB wolnego miejsca
- **Połączenie internetowe:** Wymagane do sprawdzania certyfikatów zdalnych

### Opcjonalne (dla środowiska Docker)

- **Docker Desktop:** 20.10+ (Windows/Mac) lub Docker Engine (Linux)
- **Docker Compose:** 2.0+

---

## 🔧 Instalacja Krok Po Kroku

### Krok 1: Klonowanie Repozytorium

#### Metoda A: Git (Polecana)

    # Sklonuj repozytorium
    git clone https://github.com/sebastian-c87/my-IT-profile-hub.git

    # Przejdź do folderu projektu
    cd my-IT-profile-hub/Automation-Scripts/Certificate-Expiry-Monitor

#### Metoda B: Pobierz ZIP

1. Idź do: https://github.com/sebastian-c87/my-IT-profile-hub
2. Kliknij **Code** → **Download ZIP**
3. Rozpakuj archiwum
4. Otwórz folder `Automation-Scripts/Certificate-Expiry-Monitor`

---

### Krok 2: Instalacja Pythona

#### Windows

1. Pobierz Python z: https://www.python.org/downloads/
2. Uruchom instalator
3. **WAŻNE:** Zaznacz **"Add Python to PATH"**
4. Kliknij **Install Now**

**Weryfikacja:**

    python --version
    # Wynik: Python 3.11.x

#### Linux (Ubuntu/Debian)

    sudo apt update
    sudo apt install python3 python3-pip python3-venv

**Weryfikacja:**

    python3 --version

#### macOS

    # Zainstaluj Homebrew (jeśli nie masz)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Zainstaluj Python
    brew install python3

---

### Krok 3: Tworzenie Wirtualnego Środowiska (Zalecane)

Wirtualne środowisko izoluje zależności projektu od systemu.

#### Windows

    # Utwórz venv
    python -m venv venv

    # Aktywuj venv
    venv\Scripts\activate

Po aktywacji zobaczysz `(venv)` przed promptem.

#### Linux/macOS

    # Utwórz venv
    python3 -m venv venv

    # Aktywuj venv
    source venv/bin/activate

**Dezaktywacja venv:**

    deactivate

---

### Krok 4: Instalacja Zależności

Projekt wymaga bibliotek Python wymienionych w `requirements.txt`.

    # Upewnij się że venv jest aktywny (powinien być (venv) w promptu)
    pip install -r requirements.txt

**Co zostanie zainstalowane:**
- `cryptography` - Parsowanie certyfikatów X.509
- `pyOpenSSL` - Operacje SSL/TLS
- `PyYAML` - Parsowanie plików konfiguracyjnych
- `requests` - HTTP requests (dla webhooks)
- `jinja2` - Generowanie raportów HTML
- `python-dateutil` - Operacje na datach

**Weryfikacja instalacji:**

    pip list

Powinieneś zobaczyć wszystkie zainstalowane pakiety.

---

### Krok 5: Konfiguracja Projektu

#### 5.1. Plik Konfiguracyjny `.env`

Skopiuj przykładowy plik konfiguracji:

    # Windows
    copy .env.example .env

    # Linux/macOS
    cp .env.example .env

**Edytuj `.env`** w edytorze tekstu:

    # ============================================
    # Certificate Validation Settings
    # ============================================

    # Accept self-signed certificates (dla testów Docker)
    ALLOW_SELF_SIGNED=True

    # Verify certificate chain
    VERIFY_CHAIN=True

    # Check certificate revocation (CRL/OCSP)
    CHECK_REVOCATION=False

    # Minimum TLS version (1.2 lub 1.3)
    MIN_TLS_VERSION=1.2

    # ============================================
    # Alert Thresholds (dni)
    # ============================================

    # WARNING alert threshold
    ALERT_WARNING_DAYS=30

    # CRITICAL alert threshold
    ALERT_CRITICAL_DAYS=7

    # ============================================
    # Email Notifications (SMTP)
    # ============================================

    # SMTP Server
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USE_TLS=True

    # Authentication
    SMTP_USERNAME=twoj-email@gmail.com
    SMTP_PASSWORD=twoje-haslo-aplikacji

    # Sender and recipients
    EMAIL_FROM=twoj-email@gmail.com
    EMAIL_TO=admin@example.com,devops@example.com

    # ============================================
    # Slack Notifications
    # ============================================

    SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
    SLACK_ENABLED=False

    # ============================================
    # Microsoft Teams Notifications
    # ============================================

    TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/YOUR/WEBHOOK/URL
    TEAMS_ENABLED=False

**UWAGA:** Dla Gmail musisz wygenerować **hasło aplikacji** (nie zwykłe hasło):
1. Idź do: https://myaccount.google.com/apppasswords
2. Utwórz hasło dla "Mail"
3. Skopiuj hasło do `SMTP_PASSWORD`

---

#### 5.2. Konfiguracja Domen do Monitorowania

Edytuj `config/domains.yml`:

    domains:
      # ===== PRODUKCJA =====
      
      - host: example.com
        port: 443
        name: "Strona Główna"
        enabled: true
        
      - host: api.example.com
        port: 443
        name: "API Backend"
        enabled: true
        
      - host: mail.example.com
        port: 993
        protocol: imaps
        name: "Email Server (IMAPS)"
        enabled: true
        
      # ===== ŚRODOWISKO TESTOWE DOCKER =====
      
      - host: localhost
        port: 8443
        name: "Docker Test: Valid Certificate"
        enabled: false  # Włącz gdy uruchomisz Docker
        
      - host: localhost
        port: 8444
        name: "Docker Test: Expiring Soon"
        enabled: false
        
      - host: localhost
        port: 8445
        name: "Docker Test: Expired"
        enabled: false

**Parametry domeny:**
- `host` - Hostname lub IP
- `port` - Port SSL/TLS (domyślnie 443)
- `protocol` - Protokół: `https`, `smtps`, `imaps`, `ldaps` (domyślnie `https`)
- `name` - Nazwa opisowa
- `enabled` - `true` = monitoruj, `false` = pomiń

---

#### 5.3. Konfiguracja Zaawansowana (Opcjonalna)

Edytuj `config/settings.yml`:

    # Thresholds (progi alertów)
    thresholds:
      warning_days: 30   # Wyślij WARNING gdy < 30 dni
      critical_days: 7   # Wyślij CRITICAL gdy < 7 dni

    # Timeouts
    timeouts:
      connection: 10     # Timeout połączenia (sekundy)
      handshake: 10      # Timeout SSL handshake

    # Reports
    reports:
      output_dir: output/reports
      formats:
        - html
        - csv
        - json
      retention_days: 30  # Usuń raporty starsze niż 30 dni

    # Concurrent checks
    concurrent:
      max_workers: 10    # Ile hostów sprawdzać jednocześnie

---

## 🚀 Pierwsze Uruchomienie

### Test 1: Sprawdź Pojedynczy Host

    python scripts/main.py --host google.com --port 443

**Oczekiwany wynik:**

    Certificate Expiry Monitor
    ==========================

    Checking 1 host...

    Results:
    ------------------------------------------------------------
    ✓ google.com:443                   67 days    OK

    Summary:
    ------------------------------------------------------------
    Total Certificates: 1
    ✓ OK: 1

---

### Test 2: Sprawdź Wszystkie Skonfigurowane Domeny

    python scripts/main.py --check-now

**Oczekiwany wynik:**

    Checking 5 hosts...

    Results:
    ------------------------------------------------------------
    ✓ example.com:443                  120 days   OK
    ✓ api.example.com:443              115 days   OK
    ⚠ mail.example.com:993              25 days   WARNING
    ✓ github.com:443                    67 days   OK
    ✓ google.com:443                    53 days   OK

    Summary:
    ------------------------------------------------------------
    Total Certificates: 5
    ✓ OK: 4
    ⚠ WARNING: 1

---

### Test 3: Generuj Raporty (Bez Alertów)

    python scripts/main.py --check-now --no-alerts

Raport zostanie zapisany w `output/reports/`.

**Otwórz raport HTML:**

    # Windows
    start output\reports\certificate_report_2026-01-28_23-03-47.html

    # Linux
    xdg-open output/reports/certificate_report_*.html

    # macOS
    open output/reports/certificate_report_*.html

---

## 📊 Parametry Uruchomienia (CLI)

### Podstawowe Użycie

    python scripts/main.py [OPCJE]

### Dostępne Opcje

| Opcja | Opis | Przykład |
|-------|------|----------|
| `--check-now` | Sprawdź wszystkie domeny | `python scripts/main.py --check-now` |
| `--host HOST` | Sprawdź konkretny host | `--host example.com` |
| `--port PORT` | Określ port | `--port 8443` |
| `--protocol PROTO` | Określ protokół | `--protocol smtps` |
| `--threshold DAYS` | Próg alertu (dni) | `--threshold 14` |
| `--no-alerts` | Wyłącz wysyłanie alertów | `--no-alerts` |
| `--formats FORMAT` | Formaty raportów | `--formats html,csv` |
| `--output DIR` | Folder wyjściowy | `--output /tmp/reports` |
| `--verbose` | Tryb szczegółowy (debug) | `--verbose` |
| `--quiet` | Tryb cichy (tylko błędy) | `--quiet` |
| `--help` | Pomoc | `--help` |

### Przykłady Użycia

#### Sprawdź konkretny host:

    python scripts/main.py --host api.example.com --port 443

#### Sprawdź z niższym progiem alertu (14 dni):

    python scripts/main.py --check-now --threshold 14

#### Wygeneruj tylko CSV i JSON (bez HTML):

    python scripts/main.py --check-now --formats csv,json

#### Tryb debug (szczegółowe logi):

    python scripts/main.py --check-now --verbose

#### Sprawdź SMTP server:

    python scripts/main.py --host mail.example.com --port 587 --protocol smtps

---

## ⏰ Automatyzacja (Scheduler)

### Windows Task Scheduler

#### Krok 1: Otwórz Task Scheduler

1. Wciśnij **Win + R**
2. Wpisz `taskschd.msc`
3. Kliknij **OK**

#### Krok 2: Utwórz Zadanie

1. **Create Basic Task** (prawy panel)
2. **Name:** Certificate Monitor
3. **Trigger:** Daily (codziennie)
4. **Time:** 09:00 AM
5. **Action:** Start a program
6. **Program:** `C:\Python311\python.exe`
7. **Arguments:** `C:\path\to\project\scripts\main.py --check-now`
8. **Start in:** `C:\path\to\project`
9. **Finish**

---

### Linux Cron

#### Edytuj crontab:

    crontab -e

#### Dodaj linię (uruchom codziennie o 9:00):

    0 9 * * * cd /home/user/Certificate-Expiry-Monitor && /usr/bin/python3 scripts/main.py --check-now >> /var/log/cert-monitor.log 2>&1

**Wyjaśnienie:**
- `0 9 * * *` - Codziennie o 9:00
- `cd /home/user/...` - Przejdź do folderu projektu
- `python3 scripts/main.py` - Uruchom skrypt
- `>> /var/log/cert-monitor.log` - Zapisz output do logu
- `2>&1` - Przekieruj stderr do stdout

#### Inne przykłady harmonogramów:

    # Co 6 godzin
    0 */6 * * * cd /path/to/project && python3 scripts/main.py --check-now

    # W poniedziałki o 8:00
    0 8 * * 1 cd /path/to/project && python3 scripts/main.py --check-now

    # 1-go każdego miesiąca o 10:00
    0 10 1 * * cd /path/to/project && python3 scripts/main.py --check-now

---

### macOS Launchd

#### Utwórz plik `~/Library/LaunchAgents/com.cert-monitor.plist`:

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.cert-monitor</string>
        <key>ProgramArguments</key>
        <array>
            <string>/usr/local/bin/python3</string>
            <string>/path/to/project/scripts/main.py</string>
            <string>--check-now</string>
        </array>
        <key>StartCalendarInterval</key>
        <dict>
            <key>Hour</key>
            <integer>9</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <key>StandardOutPath</key>
        <string>/tmp/cert-monitor.log</string>
        <key>StandardErrorPath</key>
        <string>/tmp/cert-monitor-error.log</string>
    </dict>
    </plist>

#### Załaduj zadanie:

    launchctl load ~/Library/LaunchAgents/com.cert-monitor.plist

---

## 🧪 Weryfikacja Instalacji

### Checklist Instalacji

- [ ] Python 3.8+ zainstalowany (`python --version`)
- [ ] Repozytorium sklonowane
- [ ] Venv utworzony i aktywny
- [ ] Zależności zainstalowane (`pip list`)
- [ ] Plik `.env` skonfigurowany
- [ ] Plik `domains.yml` zawiera domeny
- [ ] Test uruchomienia działa (`python scripts/main.py --help`)
- [ ] Raport HTML został wygenerowany

### Test Pełnego Cyklu

    # 1. Sprawdź konfigurację
    python scripts/main.py --check-config

    # 2. Uruchom test
    python scripts/main.py --host google.com --port 443 --verbose

    # 3. Sprawdź raport
    ls -la output/reports/

---

## 📚 Dalsze Kroki

Po zakończeniu instalacji:

1. **[Konfiguracja Docker](DOCKER_TESTING.md)** - Uruchom środowisko testowe
2. **[Konfiguracja Alertów](ALERTS_CONFIGURATION.md)** - Skonfiguruj Email/Slack/Teams
3. **[Rozwiązywanie Problemów](TROUBLESHOOTING.md)** - Jeśli coś nie działa

---

**Sukces!** Projekt jest gotowy do użycia! 🎉
