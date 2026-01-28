# 🚀 Instalacja i Użycie

Prosty przewodnik instalacji i pierwszego uruchomienia Infrastructure Documentation Generator.

---

## 📦 Wymagania Wstępne

### System Operacyjny

- Windows 10/11
- Linux (Ubuntu 20.04+, Debian 11+)
- macOS 11+

### Oprogramowanie

- **Python 3.9 lub nowszy** - Sprawdź wersję:

    python --version

Jeśli nie masz Pythona, pobierz ze strony: https://www.python.org/downloads/

- **Git** (opcjonalnie) - do klonowania repozytorium

### Sieć

- Dostęp SSH do urządzeń sieciowych (port 22)
- Routing z komputera do urządzeń
- Credentials (username/password) do urządzeń

---

## 📥 Instalacja

### Krok 1: Pobierz Projekt

**Jeśli masz Git:**

    cd my-it-profile-hub/Automation-Scripts
    git pull

**Jeśli nie masz Git:**

Pobierz ZIP z GitHuba i rozpakuj do folderu `my-it-profile-hub/Automation-Scripts/Infrastructure-Docs-Generator`

### Krok 2: Przejdź do Folderu Projektu

**Windows:**

    cd C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator

**Linux/macOS:**

    cd ~/my-it-profile-hub/Automation-Scripts/Infrastructure-Docs-Generator

### Krok 3: Utwórz Virtual Environment

**Windows:**

    python -m venv venv
    venv\Scripts\activate

**Linux/macOS:**

    python3 -m venv venv
    source venv/bin/activate

Po aktywacji zobaczysz `(venv)` na początku linii w terminalu.

### Krok 4: Zainstaluj Zależności

    pip install -r requirements.txt

Instalacja zajmie 1-2 minuty. Zobaczysz listę instalowanych pakietów.

### Krok 5: Skonfiguruj Zmienne Środowiskowe

**Windows:**

    copy .env.example .env

**Linux/macOS:**

    cp .env.example .env

Edytuj plik `.env` w notatniku/VSC i uzupełnij:

    OPENAI_API_KEY=sk-proj-TWOJ-PRAWDZIWY-KLUCZ
    SWITCH_USERNAME=admin
    SWITCH_PASSWORD=TwojeHaslo123

### Krok 6: Skonfiguruj Urządzenia

Edytuj `config/devices.yml` i dodaj swoje urządzenia:

    - hostname: MojSwitch
      device_type: cisco_ios
      ip: 192.168.1.100
      username: ${SWITCH_USERNAME}
      password: ${SWITCH_PASSWORD}
      enabled: true

### Krok 7: Sprawdź Konfigurację (Test)

    python scripts/main.py --test

Jeśli zobaczysz:

    ✓ Załadowano X urządzeń
    ✓ Konfiguracja poprawna!

To wszystko działa!

---

## 🎮 Użycie

### Podstawowe Uruchomienie

Uruchom cały proces (zbieranie + generowanie dokumentacji):

    python scripts/main.py

Zobaczysz:

    ======================================================================
       Infrastructure Documentation Generator
    ======================================================================
    
    🚀 Uruchamiam pełny proces dokumentacji...
    
    KROK 1/2: Zbieranie konfiguracji z urządzeń
    ----------------------------------------------------------------------
    [INFO] Rozpoczynam zbieranie konfiguracji z 4 urządzeń...
    [INFO] Łączenie z Switch-L3-Core (10.10.10.1)...
    [INFO] ✓ Sukces: Switch-L3-Core
    ...
    
    KROK 2/2: Generowanie dokumentacji AI
    ----------------------------------------------------------------------
    [INFO] Generowanie dokumentacji dla: Switch-L3-Core...
    [INFO] ✓ Sukces: Switch-L3-Core
    ...
    
    ✓ PROCES ZAKOŃCZONY POMYŚLNIE!
    📁 Dokumentacja dostępna w: output/network-docs/

### Zaawansowane Opcje

**Tylko zbieranie konfiguracji (bez AI):**

    python scripts/main.py --collect-only

**Tylko generowanie dokumentacji (z istniejących plików):**

    python scripts/main.py --generate-only

**Test pojedynczego urządzenia:**

    python scripts/main.py --device 192.168.1.100

**Sprawdzenie konfiguracji (bez łączenia z urządzeniami):**

    python scripts/main.py --test

---

## 📂 Gdzie Znajdę Wygenerowane Pliki?

Po uruchomieniu, pliki znajdziesz w:

### Dokumentacja Markdown

    output/network-docs/
    ├── README.md                  # Przegląd wszystkich urządzeń
    ├── Switch-L3-Core.md          # Dokumentacja Switch
    ├── Router-WAN-Edge.md         # Dokumentacja Router
    └── ASA-Firewall-Primary.md    # Dokumentacja Firewall

Otwórz w Visual Studio Code z podglądem Markdown (Ctrl+Shift+V) lub w przeglądarce z rozszerzeniem Markdown Viewer.

### Backup Konfiguracji

    output/raw-configs/
    ├── Switch-L3-Core_2026-01-28_02-00-15.txt
    └── ...

### Logi

    output/logs/
    ├── collector.log
    └── generator.log

---

## ⏰ Automatyczne Uruchamianie

### Windows - Task Scheduler

Zobacz szczegółowy przewodnik: **WINDOWS_TASK_SCHEDULER.md**

Krótka wersja:

1. Win + R → `taskschd.msc`
2. Create Basic Task
3. Name: "Infrastructure Docs"
4. Trigger: Daily 2:00 AM
5. Action: `C:\...\venv\Scripts\python.exe scripts\main.py`

### Linux/macOS - Cron

Edytuj crontab:

    crontab -e

Dodaj linię:

    0 2 * * * cd /path/to/Infrastructure-Docs-Generator && ./venv/bin/python scripts/main.py

Zapisz i wyjdź. Skrypt będzie uruchamiany codziennie o 2:00.

---

## 🔧 Pierwsze Uruchomienie - Checklist

Przed pierwszym uruchomieniem, upewnij się że:

- [ ] Python 3.9+ jest zainstalowany
- [ ] Virtual environment jest utworzony i aktywowany
- [ ] Zależności są zainstalowane (`pip install -r requirements.txt`)
- [ ] Plik `.env` jest utworzony i zawiera OPENAI_API_KEY
- [ ] Plik `config/devices.yml` zawiera przynajmniej 1 urządzenie
- [ ] Możesz połączyć się SSH do urządzenia ręcznie (test: `ssh admin@192.168.1.100`)
- [ ] Test konfiguracji przeszedł (`python scripts/main.py --test`)

Jeśli wszystko OK, uruchom:

    python scripts/main.py

---

## 🆘 Problemy?

Jeśli coś nie działa, sprawdź:

1. **Logi** w `output/logs/`
2. **Dokument troubleshooting:** `TROUBLESHOOTING.md`
3. **Sprawdź czy urządzenie jest online:** `ping 192.168.1.100`
4. **Sprawdź czy SSH działa:** `ssh admin@192.168.1.100`

---

## 📚 Następne Kroki

Po pierwszym udanym uruchomieniu:

1. **Zaplanuj automatyczne uruchamianie** (Task Scheduler/Cron)
2. **Dodaj pozostałe urządzenia** do `config/devices.yml`
3. **Dostosuj ustawienia** w `config/settings.yml` (np. alerty email/Slack)
4. **Utwórz backup** folderu `output/raw-configs/` (na zewnętrzny dysk/NAS)

---

**Data aktualizacji:** 2026-01-28  
**Wersja:** 1.0
