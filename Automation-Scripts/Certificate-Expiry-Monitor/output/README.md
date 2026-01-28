# 📊 Output Folder - Raporty Monitorowania Certyfikatów

Ten folder zawiera **wygenerowane raporty** z monitorowania certyfikatów SSL/TLS.

Raporty są tworzone automatycznie przy każdym uruchomieniu skryptu `main.py` i zawierają szczegółowe informacje o stanie certyfikatów na monitorowanych hostach.

---

## 📂 Struktura Folderu

    output/
    ├── reports/                    # Folder z raportami
    │   ├── certificate_report_2026-01-28_23-03-47.html   # Raport HTML (interaktywny)
    │   ├── certificate_report_2026-01-28_23-03-47.csv    # Raport CSV (Excel)
    │   ├── certificate_report_2026-01-28_23-03-47.json   # Raport JSON (API/integracje)
    │   └── ...                     # Kolejne raporty (z timestampem)
    │
    ├── logs/                       # (Opcjonalnie) Logi aplikacji
    │   └── monitor.log
    │
    └── README.md                   # Ten plik

---

## 📋 Formaty Raportów

### 1. HTML Report (Główny Raport)

**Plik:** `certificate_report_YYYY-MM-DD_HH-MM-SS.html`

**Opis:** Interaktywny raport HTML z kolorowym oznaczeniem statusów:

- 🟢 **Zielony** - Certyfikat OK (30+ dni)
- 🟡 **Żółty** - Ostrzeżenie (7-30 dni)
- 🔴 **Czerwony** - Krytyczny (0-7 dni) lub wygasły

**Zawartość:**
- Podsumowanie wszystkich certyfikatów
- Tabela z szczegółami każdego certyfikatu:
  - Hostname i port
  - Data wygaśnięcia
  - Dni pozostałe
  - Wystawca (Issuer)
  - Numer seryjny
  - Status weryfikacji
- Timestamp wygenerowania raportu

**Jak otworzyć:**

    # Windows
    start output\reports\certificate_report_2026-01-28_23-03-47.html

    # Linux/Mac
    open output/reports/certificate_report_2026-01-28_23-03-47.html

---

### 2. CSV Report (Excel/Arkusze)

**Plik:** `certificate_report_YYYY-MM-DD_HH-MM-SS.csv`

**Opis:** Raport w formacie CSV, który można otworzyć w Excel, Google Sheets lub zaimportować do bazy danych.

**Kolumny:**

    Hostname, Port, Protocol, Common Name, Issuer, Valid From, Valid Until, Days Remaining, Status, Alert Level, Serial Number, Signature Algorithm, Key Size, Is Self-Signed, Error

**Przykład danych:**

    github.com,443,https,github.com,"DigiCert Inc",2025-11-22,2026-04-05,67,Valid,OK,...
    localhost,8443,https,valid.test.local,valid.test.local,2026-01-28,2026-04-28,89,Valid,OK,...
    localhost,8444,https,expiring.test.local,expiring.test.local,2026-01-28,2026-02-04,6,Valid,CRITICAL,...
    localhost,8445,https,expired.test.local,expired.test.local,2026-01-28,2026-01-29,0,Valid,CRITICAL,...

**Zastosowanie:**
- Analiza w Excel (filtry, wykresy, pivot tables)
- Import do Power BI / Tableau
- Integracja z systemami raportowania
- Archiwizacja danych

**Jak otworzyć:**

    # Excel
    excel output\reports\certificate_report_2026-01-28_23-03-47.csv

    # LibreOffice Calc
    libreoffice output/reports/certificate_report_2026-01-28_23-03-47.csv

---

### 3. JSON Report (API/Integracje)

**Plik:** `certificate_report_YYYY-MM-DD_HH-MM-SS.json`

**Opis:** Raport w formacie JSON do integracji z innymi systemami (API, monitoring tools, dashboards).

**Struktura:**

    {
      "timestamp": "2026-01-28T23:03:47.123456+01:00",
      "summary": {
        "total": 7,
        "ok": 5,
        "warning": 0,
        "critical": 2,
        "expired": 0,
        "errors": 0
      },
      "certificates": [
        {
          "hostname": "github.com",
          "port": 443,
          "protocol": "https",
          "common_name": "github.com",
          "organization": "GitHub, Inc.",
          "valid_from": "2025-11-22T00:00:00+00:00",
          "valid_until": "2026-04-05T23:59:59+00:00",
          "days_remaining": 67,
          "is_valid": true,
          "is_expired": false,
          "is_self_signed": false,
          "alert_level": "OK",
          "error": null
        },
        {
          "hostname": "localhost",
          "port": 8444,
          "protocol": "https",
          "common_name": "expiring.test.local",
          "valid_from": "2026-01-28T20:17:16+00:00",
          "valid_until": "2026-02-04T20:17:16+00:00",
          "days_remaining": 6,
          "is_self_signed": true,
          "alert_level": "CRITICAL"
        }
      ]
    }

**Zastosowanie:**
- RESTful API endpoints
- Webhook payloads
- Monitoring tools (Prometheus, Grafana, Datadog)
- Custom dashboards
- Automated workflows

**Przykład użycia w Python:**

    import json

    # Wczytaj raport
    with open('output/reports/certificate_report_2026-01-28_23-03-47.json', 'r') as f:
        report = json.load(f)

    # Wyświetl podsumowanie
    print(f"Total: {report['summary']['total']}")
    print(f"Critical: {report['summary']['critical']}")

    # Znajdź certyfikaty krytyczne
    critical_certs = [
        cert for cert in report['certificates']
        if cert['alert_level'] == 'CRITICAL'
    ]

    for cert in critical_certs:
        print(f"⚠️  {cert['hostname']}:{cert['port']} - {cert['days_remaining']} days")

**Przykład integracji z curl:**

    # Wyślij raport do API
    curl -X POST https://api.example.com/certificates \
         -H "Content-Type: application/json" \
         -d @output/reports/certificate_report_2026-01-28_23-03-47.json

---

## 📅 Nazewnictwo Plików

Wszystkie raporty używają tego samego schematu nazewnictwa:

    certificate_report_YYYY-MM-DD_HH-MM-SS.[format]

**Przykłady:**
- `certificate_report_2026-01-28_23-03-47.html`
- `certificate_report_2026-01-28_23-03-47.csv`
- `certificate_report_2026-01-28_23-03-47.json`

**Zalety:**
- Łatwe sortowanie chronologiczne
- Unikalne nazwy (brak konfliktów)
- Czytelny format daty i czasu
- Łatwa identyfikacja najnowszego raportu

---

## 🔍 Interpretacja Statusów

### Alert Levels (Poziomy Alertów)

| Level | Dni Pozostałe | Kolor | Znaczenie |
|-------|---------------|-------|-----------|
| **OK** | 30+ | 🟢 Zielony | Certyfikat w pełni ważny |
| **WARNING** | 7-30 | 🟡 Żółty | Należy zaplanować odnowienie |
| **CRITICAL** | 0-7 | 🔴 Czerwony | Pilnie wymagane odnowienie! |
| **EXPIRED** | < 0 | ⛔ Czarny | Certyfikat wygasł - BŁĄD! |
| **ERROR** | N/A | ❌ Czerwony | Błąd połączenia lub weryfikacji |

### Przykładowe Scenariusze

#### Scenariusz 1: Wszystko OK ✅

    Total Certificates: 5
    ✓ OK: 5
    ⚠ Warning: 0
    ✗ Critical: 0
    ❌ Expired: 0

**Akcja:** Brak. System działa prawidłowo.

---

#### Scenariusz 2: Ostrzeżenie ⚠️

    Total Certificates: 5
    ✓ OK: 3
    ⚠ Warning: 2
    ✗ Critical: 0
    ❌ Expired: 0

**Akcja:** Zaplanuj odnowienie certyfikatów w ciągu najbliższych 2 tygodni.

---

#### Scenariusz 3: Stan Krytyczny 🚨

    Total Certificates: 5
    ✓ OK: 2
    ⚠ Warning: 1
    ✗ Critical: 2
    ❌ Expired: 0

**Akcja:** PILNE! Odnów certyfikaty w ciągu 24-48h!

---

#### Scenariusz 4: Certyfikat Wygasł ⛔

    Total Certificates: 5
    ✓ OK: 2
    ⚠ Warning: 1
    ✗ Critical: 1
    ❌ Expired: 1

**Akcja:** NATYCHMIASTOWA INTERWENCJA! Serwis może nie działać!

---

## 📈 Przykładowe Raporty (Demo)

### Raport z Testowego Środowiska Docker

**Data:** 2026-01-28 23:03:47

**Podsumowanie:**
- Total: 7 certyfikatów
- OK: 5 (71%)
- Critical: 2 (29%)

**Szczegóły:**

| Host | Port | CN | Days | Status |
|------|------|----|----|--------|
| github.com | 443 | github.com | 67 | 🟢 OK |
| google.com | 443 | *.google.com | 53 | 🟢 OK |
| localhost | 8443 | valid.test.local | 89 | 🟢 OK |
| localhost | 8444 | expiring.test.local | 6 | 🔴 CRITICAL |
| localhost | 8445 | expired.test.local | 0 | 🔴 CRITICAL |
| sebastian-c87.github.io | 443 | *.github.io | 38 | 🟢 OK |
| stackoverflow.com | 443 | *.stackoverflow.com | 52 | 🟢 OK |

---

## 🗂️ Zarządzanie Raportami

### Automatyczne Czyszczenie Starych Raportów

Aby uniknąć zapełnienia dysku, możesz skonfigurować automatyczne usuwanie starych raportów:

**W pliku `config/settings.yml`:**

    reports:
      retention_days: 30  # Usuń raporty starsze niż 30 dni
      auto_cleanup: true

**Ręczne czyszczenie (Windows):**

    # Usuń raporty starsze niż 30 dni
    forfiles /P output\reports /S /M *.* /D -30 /C "cmd /c del @path"

**Ręczne czyszczenie (Linux/Mac):**

    # Usuń raporty starsze niż 30 dni
    find output/reports -name "certificate_report_*" -mtime +30 -delete

---

## 🔗 Integracje

### Power BI / Tableau

1. Import CSV do Power BI/Tableau
2. Utwórz dashboard z wizualizacjami:
   - Wykres słupkowy: Liczba certyfikatów według statusu
   - Timeline: Daty wygaśnięcia certyfikatów
   - Tabela: Lista krytycznych certyfikatów
   - Gauge: Procent certyfikatów OK

### Prometheus / Grafana

Użyj JSON report jako źródło danych dla custom exporter:

    # Przykładowy Prometheus exporter
    python scripts/prometheus_exporter.py \
      --input output/reports/certificate_report_latest.json \
      --port 9090

### Webhook Notifications

Skrypt automatycznie może wysyłać raporty JSON do webhooków:

    # config/settings.yml
    webhooks:
      - url: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
        on_alert: true
      - url: https://your-api.com/certificates
        on_every_run: true

---

## 📞 Pomoc i Wsparcie

### Problemy z Raportami?

**Problem:** Raport nie został wygenerowany

**Rozwiązanie:** Sprawdź logi w `output/logs/monitor.log`

**Problem:** CSV nie otwiera się w Excel

**Rozwiązanie:** Zmień encoding na Windows-1250 w `config/settings.yml`

**Problem:** JSON jest za duży (>10MB)

**Rozwiązanie:** Włącz kompresję gzip w konfiguracji

---

## 📚 Dodatkowe Zasoby

- [Główny README projektu](../README.md)
- [Konfiguracja monitorowania](../config/README.md)
- [Dokumentacja Docker](../docker/README.md)
- [Skrypty generujące certyfikaty](../docker/scripts/README.md)

---

**Autor:** Sebastian Ciborowski  
**Projekt:** Certificate-Expiry-Monitor  
**GitHub:** https://github.com/sebastian-c87/my-IT-profile-hub
