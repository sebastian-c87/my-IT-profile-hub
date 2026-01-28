# 🌐 Infrastructure Documentation Generator

Automatyczne generowanie dokumentacji sieci na podstawie rzeczywistych konfiguracji urządzeń sieciowych, wykorzystujące AI (GPT-5-nano) do tworzenia czytelnych opisów w formacie Markdown.

## 📋 Spis Treści

- [O Projekcie](#o-projekcie)
- [Funkcje](#funkcje)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Użycie](#użycie)
- [Struktura Projektu](#struktura-projektu)
- [Harmonogram](#harmonogram)
- [Rozwiązywanie Problemów](#rozwiązywanie-problemów)
- [Licencja](#licencja)

## 🎯 O Projekcie

Ten projekt rozwiązuje problem **nieaktualnej lub nieistniejącej dokumentacji sieci**. Zamiast ręcznie opisywać konfiguracje setek urządzeń, skrypt:

1. Automatycznie łączy się SSH do wszystkich urządzeń (Cisco, Juniper, Arista)
2. Pobiera konfiguracje (show running-config)
3. Wykorzystuje AI do wygenerowania czytelnej dokumentacji
4. Zapisuje wszystko w formacie Markdown

**Rezultat:** Zawsze aktualna dokumentacja synchronizowana z rzeczywistym stanem sieci.

## ✨ Funkcje

- **Automatyczne zbieranie konfiguracji** - Netmiko łączy się SSH do urządzeń i pobiera config
- **Analiza AI** - GPT-5-nano generuje dokumentację na podstawie raw config
- **Multi-vendor support** - Cisco IOS/IOS-XE/IOS-XR, ASA, Juniper, Arista
- **Format Markdown** - Czytelna dokumentacja z tabelami, listami, nagłówkami
- **Backup konfiguracji** - Raw configs zapisywane z timestampem (wersjonowanie)
- **Schedulowanie** - Uruchamianie przez Cron (Linux/macOS) lub Task Scheduler (Windows)
- **Alerty** - Powiadomienia email/Slack gdy urządzenie jest niedostępne

## 📦 Wymagania

### System Operacyjny

- Windows 10/11 (testowane)
- Linux (Ubuntu 20.04+, Debian 11+)
- macOS 11+
- Windows Server 2016+ (produkcja)

### Oprogramowanie

- Python 3.9 lub nowszy
- Dostęp SSH do urządzeń sieciowych
- OpenAI API Key (dla GPT-5-nano)

### Sieć

- Urządzenia sieciowe muszą mieć włączony SSH
- Serwer z uruchomionym skryptem musi być w tej samej sieci lub mieć routing do urządzeń
- Firewall musi zezwalać na połączenia SSH (port 22) do urządzeń

## 🚀 Instalacja

### Krok 1: Przejdź do folderu projektu

    cd my-it-profile-hub/Automation-Scripts/Infrastructure-Docs-Generator

### Krok 2: Utwórz wirtualne środowisko Python

**Windows:**

    python -m venv venv
    venv\Scripts\activate

**Linux/macOS:**

    python3 -m venv venv
    source venv/bin/activate

### Krok 3: Zainstaluj zależności

    pip install -r requirements.txt

### Krok 4: Skonfiguruj zmienne środowiskowe

Skopiuj plik przykładowy i uzupełnij dane:

    copy .env.example .env

Edytuj plik .env w edytorze tekstu i uzupełnij:

- OPENAI_API_KEY - Twój klucz API OpenAI
- Hasła do urządzeń sieciowych

**UWAGA:** Plik .env zawiera wrażliwe dane i NIE MOŻE być commitowany do Git (jest w .gitignore).

## ⚙️ Konfiguracja

### Plik config/devices.yml

Zawiera listę urządzeń do monitorowania. Dodaj wszystkie swoje routery, switche, firewalle.

Przykład struktury jest zawarty w pliku. Każde urządzenie wymaga:

- hostname - Nazwa urządzenia (dla identyfikacji)
- device_type - Typ urządzenia (cisco_ios, cisco_asa, juniper_junos itp.)
- ip - Adres IP zarządzania
- username - Login SSH
- password - Hasło SSH (można użyć zmiennej z .env)

### Plik config/settings.yml

Zawiera globalne ustawienia projektu:

- Ścieżki do folderów output
- Ustawienia modelu AI (model, reasoning effort)
- Konfiguracja alertów (email, Slack)
- Poziom logowania

Szczegółowy opis każdego parametru znajduje się w komentarzach w pliku.

## 🎮 Użycie

### Podstawowe uruchomienie

Uruchom główny skrypt który wykona wszystkie kroki:

    python scripts/main.py

Skrypt automatycznie:
1. Zbierze konfiguracje ze wszystkich urządzeń
2. Wygeneruje dokumentację AI
3. Zapisze pliki Markdown w folderze output/

### Zaawansowane opcje

**Tylko zbieranie konfiguracji (bez AI):**

    python scripts/collect_configs.py

**Tylko generowanie dokumentacji (z istniejących raw configs):**

    python scripts/generate_docs.py

**Testowanie połączenia z jednym urządzeniem:**

    python scripts/main.py --test --device 10.10.10.1

### Gdzie znajdę dokumentację?

Po uruchomieniu skryptu, wygenerowana dokumentacja znajduje się w:

    output/network-docs/

Przykładowe pliki:
- README.md - Przegląd całej sieci
- Switch-L3.md - Dokumentacja konkretnego switcha
- Router0.md - Dokumentacja routera
- ASA-Firewall.md - Dokumentacja firewalla

Raw konfiguracje (backup) znajdują się w:

    output/raw-configs/

Format nazwy pliku: {hostname}_{data}_{czas}.txt

## 🗂️ Struktura Projektu

    Infrastructure-Docs-Generator/
    ├── README.md                    # Ten plik
    ├── requirements.txt             # Zależności Python
    ├── .env.example                 # Przykład zmiennych środowiskowych
    ├── .gitignore                   # Pliki ignorowane przez Git
    ├── config/                      # Pliki konfiguracyjne
    │   ├── devices.yml              # Lista urządzeń
    │   └── settings.yml             # Ustawienia globalne
    ├── scripts/                     # Główne skrypty
    │   ├── collect_configs.py       # Zbieranie konfiguracji
    │   ├── generate_docs.py         # Generowanie dokumentacji AI
    │   └── main.py                  # Główny skrypt (uruchamia wszystko)
    ├── templates/                   # Szablony dokumentacji
    │   ├── device_template.md       # Szablon dla urządzenia
    │   └── network_overview_template.md  # Szablon przeglądu
    ├── output/                      # Wygenerowane pliki (NIE W GIT!)
    │   └── README.md                # Opis zawartości folderu
    └── docs/                        # Dokumentacja projektu
        ├── INSTALLATION.md          # Szczegółowa instalacja
        ├── USAGE.md                 # Przewodnik użytkownika
        ├── WINDOWS_TASK_SCHEDULER.md # Harmonogram Windows
        └── TROUBLESHOOTING.md       # Rozwiązywanie problemów

## ⏰ Harmonogram

### Linux / macOS (Cron)

Edytuj crontab:

    crontab -e

Dodaj linię (uruchamianie codziennie o 2:00 AM):

    0 2 * * * cd /home/user/my-it-profile-hub/Automation-Scripts/Infrastructure-Docs-Generator && ./venv/bin/python scripts/main.py

### Windows (Task Scheduler)

Szczegółowa instrukcja znajduje się w pliku docs/WINDOWS_TASK_SCHEDULER.md

Krótka wersja:
1. Otwórz Task Scheduler (Win + R → taskschd.msc)
2. Create Basic Task
3. Name: Infrastructure Docs Generator
4. Trigger: Daily 2:00 AM
5. Action: Start a program
6. Program: C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator\venv\Scripts\python.exe
7. Arguments: scripts\main.py
8. Start in: C:\Users\YourUsername\my-it-profile-hub\Automation-Scripts\Infrastructure-Docs-Generator

## 🔧 Rozwiązywanie Problemów

Szczegółowy troubleshooting znajduje się w docs/TROUBLESHOOTING.md

### Najczęstsze problemy:

**Błąd: Authentication failed**
- Sprawdź czy username i password w devices.yml są poprawne
- Sprawdź czy urządzenie ma włączony SSH
- Sprawdź czy IP jest osiągalny (ping)

**Błąd: Connection timeout**
- Sprawdź routing (czy serwer ma dostęp do urządzenia)
- Sprawdź firewall (port 22 TCP)
- Sprawdź czy urządzenie jest online

**Błąd: OpenAI API Error**
- Sprawdź czy klucz API w .env jest poprawny
- Sprawdź saldo konta OpenAI
- Sprawdź połączenie internetowe

**Dokumentacja jest niekompletna**
- Sprawdź logi w output/logs/
- Uruchom z flagą --verbose dla szczegółowych logów
- Sprawdź czy raw config został pobrany poprawnie

## 📊 Logi

Logi zapisywane są w:

    output/logs/generator.log

Format logów:
- INFO - Normalne operacje
- WARNING - Potencjalne problemy
- ERROR - Błędy wymagające uwagi

## 🤝 Współpraca

Projekt jest częścią portfolio automatyzacji sieciowej. Sugestie i feedback są mile widziane.

## 📄 Licencja

MIT License - wolne użycie, modyfikacja, dystrybucja.

## 👤 Autor

Sebastian Ciborowski
GitHub: github.com/sebastian-c87/my-it-profile-hub
