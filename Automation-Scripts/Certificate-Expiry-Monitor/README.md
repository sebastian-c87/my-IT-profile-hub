# 🔒 Certificate Expiry Monitor

**Automatyczne monitorowanie i alertowanie wygasających certyfikatów SSL/TLS**


![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)


---

## 📋 Spis Treści

- [O Projekcie](#o-projekcie)
- [Funkcjonalności](#funkcjonalności)
- [Wymagania](#wymagania)
- [Szybki Start](#szybki-start)
- [Przykład Użycia](#przykład-użycia)
- [Scenariusze Użycia](#scenariusze-użycia)
- [Dokumentacja](#dokumentacja)
- [Testowanie](#testowanie)
- [Autor](#autor)

---

## 🎯 O Projekcie

**Certificate Expiry Monitor** to narzędzie do automatycznego monitorowania certyfikatów SSL/TLS w infrastrukturze sieciowej. Skrypt sprawdza certyfikaty na serwerach web, mail, proxy i innych usługach, alertując administratorów przed wygaśnięciem.

### Dlaczego Ten Projekt?

Wygasłe certyfikaty SSL prowadzą do:
- ❌ Przestojów w usługach (downtime)
- ❌ Ostrzeżeń bezpieczeństwa dla użytkowników
- ❌ Problemów z compliance i audytem
- ❌ Utraty zaufania klientów

**Rozwiązanie:** Automatyczne monitorowanie + alerty = Zero przestojów!

---

## ✨ Funkcjonalności

### 🔍 Monitorowanie

- ✅ **Multi-Protocol Support**
  - HTTPS (443) - Web servers
  - SMTPS (465/587) - Mail servers
  - IMAPS (993) - Mail servers
  - LDAPS (636) - Active Directory
  - FTPS (990) - FTP servers
  - Custom ports

- ✅ **Walidacja Certyfikatów**
  - Data wygaśnięcia
  - Łańcuch certyfikatów (chain validation)
  - Weryfikacja CA (Certificate Authority)
  - Sprawdzanie revocation (CRL/OCSP)
  - Support dla self-signed certificates

- ✅ **Typy Certyfikatów**
  - Public CA (Let's Encrypt, DigiCert)
  - Internal CA (Active Directory)
  - Self-signed (testowanie)
  - Wildcard certificates
  - Multi-domain (SAN)

### 🚨 System Alertów

- 📧 **Email Alerts** (SMTP)
  - WARNING - 30 dni przed wygaśnięciem
  - CRITICAL - 7 dni przed wygaśnięciem
  - EXPIRED - certyfikat już wygasł
  - HTML templates z szczegółami

- 💬 **Slack Integration**
  - Real-time notifications
  - Formatted blocks z przyciskami
  - Channel mentions (@here/@channel)

- 📱 **Microsoft Teams**
  - Adaptive Cards
  - Action buttons

### 📊 Raporty

- **Daily Reports** - Codzienny przegląd wszystkich certyfikatów
- **Alert History** - Historia wysłanych alertów
- **Expiry Calendar** - Kalendarz wygasających certyfikatów
- **Export Formats:**
  - HTML (interactive)
  - CSV (Excel)
  - JSON (API integration)
  - PDF (optional)

### 🔧 Automatyzacja

- ⏰ **Scheduled Checks**
  - Windows Task Scheduler
  - Linux/macOS Cron
  - Daemon mode (background service)

- 🐳 **Docker Test Environment**
  - Kompletny test setup
  - 5 różnych scenariuszy certyfikatów
  - Nginx, Apache, Postfix containers
  - Auto-generowane test certificates

---

## 📦 Wymagania

### System
- **Python:** 3.9 lub nowszy
- **OS:** Windows, Linux, macOS
- **Docker:** (opcjonalnie, do testowania)

### Sieć
- Dostęp do monitorowanych serwerów (port SSL/TLS)
- SMTP server (dla alertów email)
- Internet (dla Slack/Teams webhooks)

---

## 🚀 Szybki Start

### 1. Klonowanie Repozytorium

    git clone https://github.com/sebastian-c87/Certificate-Expiry-Monitor.git
    cd Certificate-Expiry-Monitor

### 2. Instalacja Zależności

    # Utwórz wirtualne środowisko
    python -m venv venv

    # Aktywuj środowisko
    # Windows:
    venv\Scripts\activate
    # Linux/macOS:
    source venv/bin/activate

    # Zainstaluj zależności
    pip install -r requirements.txt

### 3. Konfiguracja

    # Skopiuj przykładowe pliki konfiguracyjne
    copy .env.example .env
    copy .gitignore.example .gitignore

    # Edytuj .env i dodaj swoje dane
    notepad .env

**Minimalna konfiguracja `.env`:**

    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USERNAME=your-email@gmail.com
    SMTP_PASSWORD=your-app-password
    ALERT_EMAIL_TO=admin@company.com

### 4. Konfiguracja Domen

Edytuj `config/domains.yml`:

    public_domains:
      - name: Google
        host: google.com
        port: 443
        protocol: https
        alert_days: 30

### 5. Uruchomienie

    # Test pojedynczego hosta
    python scripts/main.py --test --host google.com

    # Sprawdź wszystkie skonfigurowane hosty
    python scripts/main.py --check-now

    # Wygeneruj raport
    python scripts/main.py --report

---

## 💡 Przykład Użycia

### Sprawdzanie Certyfikatu

    $ python scripts/main.py --test --host github.com

    Certificate Expiry Monitor v1.0
    ================================

    Checking: github.com:443

    ✓ Certificate Valid
      Subject: github.com
      Issuer: DigiCert TLS RSA SHA256 2020 CA1
      Valid From: 2025-12-15
      Valid Until: 2026-06-15
      Days Remaining: 138
      Status: OK

    Chain Validation: ✓ Valid
    OCSP Status: ✓ Good

### Pełne Skanowanie

    $ python scripts/main.py --check-now

    Certificate Expiry Monitor - Full Scan
    =======================================
    Scanning 15 hosts...

    ✓ google.com          89 days    OK
    ✓ github.com          127 days   OK
    ✓ mail.company.local  45 days    OK
    ⚠ vpn.company.local   12 days    WARNING
    ⚠ proxy.company.local 5 days     CRITICAL
    ✗ old.company.local   -10 days   EXPIRED

    Summary:
    --------
    Total: 15 hosts
    ✓ OK: 12
    ⚠ Warning: 2
    ✗ Critical/Expired: 1

    Alerts sent:
    - Email to admin@company.com (3 alerts)
    - Slack notification sent

    Report saved: output/reports/daily/2026-01-28.html

---

## 🎯 Scenariusze Użycia

### 1. Administrator Sieci Korporacyjnej

**Masz:**
- 20 serwerów web (IIS, Nginx, Apache)
- 3 mail servery (Exchange, Postfix)
- 5 load balancerów
- VPN gateway
- Proxy serwery

**Rozwiązanie:**

    # config/domains.yml
    internal_servers:
      - name: Main Web Server
        host: 192.168.1.100
        port: 443
        alert_days: 14
      
      - name: Mail Server SMTPS
        host: mail.company.local
        port: 465
        alert_days: 7

**Rezultat:**
- ✅ Codzienne sprawdzanie wszystkich serwerów (Task Scheduler)
- ✅ Alert 14 dni przed wygaśnięciem → czas na renewal
- ✅ Dashboard dla managementu z statusem certyfikatów
- ✅ Zero przestojów!

### 2. DevOps Engineer

**Masz:**
- Kubernetes cluster z 50 services
- Ingress controllers z certyfikatami
- Internal services z mTLS

**Rozwiązanie:**
- Automatyczne sprawdzanie cert-manager certificates
- Integration z cert-manager renewal
- Prometheus metrics export

### 3. Security Team

**Audyt compliance:**
- ✅ Wszystkie certyfikaty ważne
- ✅ Tylko zaufane CA
- ✅ Brak weak algorithms (MD5, SHA1)
- ✅ TLS 1.2+ only

---

## 📚 Dokumentacja

### Główna Dokumentacja

- 📖 [**Instalacja i Użycie**](docs/INSTALLATION_AND_USAGE.md) - Szczegółowa instrukcja setup
- 🐳 [**Docker Testing**](docs/DOCKER_TESTING.md) - Testowanie z Docker environment
- 🌐 [**Real World Scenarios**](docs/REAL_WORLD_SCENARIOS.md) - Praktyczne scenariusze użycia
- 🎓 [**SSL Certificates Training**](docs/SSL_CERTIFICATES_TRAINING.md) - Kompletne szkolenie SSL/TLS
- 🔧 [**Troubleshooting**](docs/TROUBLESHOOTING.md) - Rozwiązywanie problemów
- 📦 [**Packet Tracer Setup**](docs/PACKET_TRACER_SETUP.md) - Alternatywy dla PT (GNS3, EVE-NG)

### Szkolenie SSL/TLS

Projekt zawiera **kompletny przewodnik edukacyjny** po certyfikatach SSL/TLS:

📘 **[SSL_CERTIFICATES_TRAINING.md](docs/SSL_CERTIFICATES_TRAINING.md)**

**Zawartość:**
1. ✅ Podstawy kryptografii
2. ✅ Czym jest certyfikat SSL/TLS
3. ✅ Jak działa SSL handshake (krok po kroku)
4. ✅ Certificate Authority (CA) i łańcuch zaufania
5. ✅ Typy certyfikatów (DV, OV, EV, Wildcard, SAN)
6. ✅ Jak sprawdzać certyfikaty (OpenSSL, Python)
7. ✅ Jak generować certyfikaty (self-signed, Let's Encrypt, CA)
8. ✅ Jak odnowić certyfikaty
9. ✅ Troubleshooting (connection errors, chain issues)
10. ✅ Best practices
11. ✅ Narzędzia (OpenSSL, Certbot, TestSSL)
12. ✅ Praktyczne ćwiczenia
13. ✅ Real world examples
14. ✅ Zaawansowane tematy
15. ✅ Glossary (słowniczek terminów)

**To jest kompletny kurs SSL/TLS od podstaw do zaawansowanych!**

---

## 🧪 Testowanie

### Docker Test Environment

Projekt zawiera **kompletny Docker setup** do testowania:

    # Uruchom test environment
    cd docker
    docker-compose up -d

    # Zobaczysz 5 kontenerów z różnymi certyfikatami:
    # - nginx-valid (ważny 90 dni)
    # - nginx-expiring (wygasa za 7 dni)
    # - nginx-expired (wygasł)
    # - apache-selfsigned (self-signed)
    # - mail-server (SMTPS)

    # Testuj skrypt
    cd ..
    python scripts/main.py --check-now

**Rezultat:**

    ✓ localhost:8443 - Valid (89 days)
    ⚠ localhost:8444 - Expiring (7 days) - WARNING
    ✗ localhost:8445 - Expired (-5 days) - CRITICAL
    ⚠ localhost:8446 - Self-signed (not trusted)
    ✓ localhost:8465 - Valid (60 days)

### Unit Tests

    # Uruchom wszystkie testy
    pytest tests/

    # Tylko unit tests
    pytest tests/test_cert_checker.py

    # Integration tests (wymaga Docker)
    pytest tests/test_integration.py

---

## 📂 Struktura Projektu

    Certificate-Expiry-Monitor/
    ├── README.md                    # Ten plik
    ├── requirements.txt             # Zależności Python
    ├── .env.example                 # Przykładowa konfiguracja env
    ├── .gitignore.example           # Wzór .gitignore
    │
    ├── config/                      # Konfiguracja
    │   ├── domains.yml              # Lista hostów do monitorowania
    │   ├── settings.yml             # Ustawienia aplikacji
    │   └── certificate-types.yml   # Typy certyfikatów
    │
    ├── scripts/                     # Skrypty Python
    │   ├── main.py                  # Entry point
    │   ├── cert_checker.py          # Sprawdzanie certyfikatów
    │   ├── cert_validator.py        # Walidacja łańcucha
    │   ├── alerting.py              # System alertów
    │   ├── reporting.py             # Generowanie raportów
    │   └── utils.py                 # Utilities
    │
    ├── docker/                      # Docker test environment
    │   ├── docker-compose.yml       # Konfiguracja kontenerów
    │   ├── nginx/                   # Nginx z certyfikatami
    │   ├── apache/                  # Apache z certyfikatami
    │   └── scripts/                 # Generowanie cert testowych
    │
    ├── templates/                   # Szablony
    │   ├── email/                   # Email templates
    │   ├── slack/                   # Slack messages
    │   └── reports/                 # Report templates
    │
    ├── output/                      # Output (nie commitowane)
    │   ├── logs/                    # Logi aplikacji
    │   └── reports/                 # Wygenerowane raporty
    │
    └── docs/                        # Dokumentacja
        ├── INSTALLATION_AND_USAGE.md
        ├── DOCKER_TESTING.md
        ├── REAL_WORLD_SCENARIOS.md
        ├── SSL_CERTIFICATES_TRAINING.md
        ├── TROUBLESHOOTING.md
        └── PACKET_TRACER_SETUP.md

---

## 🛠️ Technologie

- **Python 3.9+**
- **cryptography** - X.509 certificate parsing
- **pyOpenSSL** - SSL/TLS operations
- **PyYAML** - Configuration files
- **Jinja2** - Templating
- **Docker** - Test environment

---

## 🤝 Jak Używać w Pracy

### Jako Network Administrator

1. **Setup** - Dodaj wszystkie serwery do `config/domains.yml`
2. **Automatyzacja** - Skonfiguruj Task Scheduler (codziennie o 3:00)
3. **Alerty** - Email na team mailbox
4. **Dashboard** - HTML report dla managementu
5. **Dokumentacja** - Pełna wiedza o SSL/TLS

### Integracja z Odnowieniem

    # W config/settings.yml
    auto_renewal:
      enabled: true
      method: certbot
      threshold_days: 30

    # Skrypt automatycznie uruchomi:
    # certbot renew --cert-name example.com

---

## 📝 Licencja

MIT License - Zobacz [LICENSE](LICENSE) dla szczegółów.

---

## 👤 Autor

**Sebastian C.**

- GitHub: [@sebastian-c87](https://github.com/sebastian-c87)
- Portfolio: [sebastian-c87.github.io/my-IT-profile-hub](https://sebastian-c87.github.io/my-IT-profile-hub)

---

## 🙏 Podziękowania

- **Let's Encrypt** - Za darmowe certyfikaty SSL
- **OpenSSL Community** - Za narzędzia kryptograficzne
- **Python Cryptography Team** - Za świetną bibliotekę

---

## 📈 Roadmap

- [ ] Prometheus metrics export
- [ ] Grafana dashboard
- [ ] Integration z cert-manager (Kubernetes)
- [ ] Mobile app (Android/iOS)
- [ ] Multi-tenant support
- [ ] API REST

---

## 🐛 Zgłaszanie Błędów

Znalazłeś bug? Otwórz [Issue na GitHubie](https://github.com/sebastian-c87/Certificate-Expiry-Monitor/issues)

---

## ⭐ Star History

Jeśli projekt Ci pomógł, zostaw ⭐ na GitHubie!

---

**Projekt stworzony jako część portfolio IT automation scripts.**

**Zero przestojów. Zero wygasłych certyfikatów. 100% automatyzacja.** 🚀
