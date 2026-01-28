# 🔧 Troubleshooting - Rozwiązywanie Problemów

Kompleksowy przewodnik rozwiązywania problemów z Infrastructure Documentation Generator.

---

## 📋 Spis Treści

- [Kategorie Problemów](#kategorie-problemów)
- [Problemy z Połączeniem SSH](#problemy-z-połączeniem-ssh)
- [Problemy z Python i Zależnościami](#problemy-z-python-i-zależnościami)
- [Problemy z OpenAI API](#problemy-z-openai-api)
- [Problemy z Konfiguracją](#problemy-z-konfiguracją)
- [Problemy z Urządzeniami Cisco](#problemy-z-urządzeniami-cisco)
- [Problemy z Urządzeniami Juniper](#problemy-z-urządzeniami-juniper)
- [Problemy z Generowaniem Dokumentacji](#problemy-z-generowaniem-dokumentacji)
- [Problemy z Wydajnością](#problemy-z-wydajnością)
- [Problemy Specyficzne dla Windows](#problemy-specyficzne-dla-windows)
- [Problemy Specyficzne dla Linux/macOS](#problemy-specyficzne-dla-linuxmacos)
- [FAQ - Najczęściej Zadawane Pytania](#faq---najczęściej-zadawane-pytania)
- [Tryb Debug](#tryb-debug)
- [Gdzie Szukać Pomocy](#gdzie-szukać-pomocy)

---

## 📊 Kategorie Problemów

### Szybka Diagnoza

**Problem pojawia się podczas:**

| Moment | Kategoria | Zobacz sekcję |
|--------|-----------|---------------|
| Instalacji pakietów | Python/Pip | [Problemy z Python](#problemy-z-python-i-zależnościami) |
| Łączenia z urządzeniem | SSH/Network | [Problemy SSH](#problemy-z-połączeniem-ssh) |
| Pobierania konfiguracji | Device-specific | [Cisco](#problemy-z-urządzeniami-cisco) / [Juniper](#problemy-z-urządzeniami-juniper) |
| Generowania dokumentacji | OpenAI API | [OpenAI API](#problemy-z-openai-api) |
| Uruchamiania przez Task Scheduler | Windows | [Windows](#problemy-specyficzne-dla-windows) |

---

## 🔐 Problemy z Połączeniem SSH

### Problem 1: NetmikoTimeoutException

**Błąd:**

    [ERROR] ✗ Timeout: Switch-L3-Core - urządzenie niedostępne lub firewall blokuje
    netmiko.exceptions.NetmikoTimeoutException: Connection to device timed-out: cisco_ios 10.10.10.1:22

**Przyczyny:**

1. Urządzenie jest offline
2. Port SSH (22) jest zablokowany przez firewall
3. Niepoprawny adres IP
4. Timeout jest zbyt krótki

**Rozwiązanie Krok po Kroku:**

**Krok 1: Sprawdź czy urządzenie jest online**

    ping 10.10.10.1

Jeśli brak odpowiedzi → urządzenie offline lub routing nie działa

**Krok 2: Sprawdź czy port SSH jest otwarty**

Windows PowerShell:

    Test-NetConnection -ComputerName 10.10.10.1 -Port 22

Linux/macOS:

    nc -zv 10.10.10.1 22
    # lub
    telnet 10.10.10.1 22

Jeśli błąd "Connection refused" lub "No route to host" → SSH nie działa lub firewall blokuje

**Krok 3: Sprawdź routing z Twojego komputera**

    tracert 10.10.10.1    # Windows
    traceroute 10.10.10.1  # Linux/macOS

Czy pakiety docierają do urządzenia?

**Krok 4: Sprawdź czy SSH działa na urządzeniu**

Połącz się ręcznie:

    ssh admin@10.10.10.1

Jeśli połączenie się udaje → problem z konfiguracją skryptu  
Jeśli nie → problem z urządzeniem/siecią

**Krok 5: Zwiększ timeout w config/settings.yml**

    ssh:
      timeout: 60  # Zwiększ z 30 do 60 sekund

**Krok 6: Sprawdź firewall na Twoim komputerze**

Windows Firewall może blokować wychodzące połączenia SSH.

Windows Defender Firewall → Advanced Settings → Outbound Rules → Sprawdź reguły dla portu 22

**Dodatkowe Sprawdzenia:**

- Sprawdź czy urządzenie ma prawidłową konfigurację SSH (na konsoli urządzenia)
- Sprawdź czy ACL na urządzeniu nie blokuje Twojego IP
- Sprawdź czy VTY lines są dostępne (cisco: `line vty 0 15`)

---

### Problem 2: NetmikoAuthenticationException

**Błąd:**

    [ERROR] ✗ Błąd autentykacji: Router-WAN-Edge - sprawdź username/password
    netmiko.exceptions.NetmikoAuthenticationException: Authentication failed

**Przyczyny:**

1. Błędne hasło lub username
2. Brak zmiennych środowiskowych w .env
3. Konto zablokowane na urządzeniu
4. Wymagana autentykacja AAA (RADIUS/TACACS+)

**Rozwiązanie:**

**Krok 1: Sprawdź czy .env zawiera credentials**

Otwórz plik `.env`:

    SWITCH_USERNAME=admin
    SWITCH_PASSWORD=TwojeHaslo123

Czy zmienne są ustawione? Czy nie ma spacji na końcu?

**Krok 2: Sprawdź czy devices.yml używa zmiennych**

Otwórz `config/devices.yml`:

    username: ${SWITCH_USERNAME}
    password: ${SWITCH_PASSWORD}

Czy używa `${}` notacji?

**Krok 3: Test ręczny SSH**

    ssh admin@10.10.10.1

Podaj hasło ręcznie. Czy działa?

**Krok 4: Sprawdź czy hasło nie zawiera specjalnych znaków**

Niektóre znaki mogą powodować problemy w YAML:

    password: "Tw0je@Ha$lo!"  # Użyj cudzysłowów dla specjalnych znaków

**Krok 5: Sprawdź logi autoryzacji na urządzeniu**

Cisco IOS:

    show logging | include Authentication

Szukaj komunikatów typu "Authentication failed for user admin"

**Krok 6: Sprawdź czy konto nie jest zablokowane**

Cisco IOS:

    show users
    show users accounts

Jeśli konto zablokowane, odblokuj:

    configure terminal
    username admin privilege 15 secret NoweHaslo123

**Problem z AAA:**

Jeśli urządzenie używa AAA (RADIUS/TACACS+), upewnij się że:

1. Masz local fallback skonfigurowany:

    aaa authentication login default group tacacs+ local

2. Lub użyj lokalnego konta zamiast AAA

---

### Problem 3: "Authentication to device failed"

**Błąd:**

    paramiko.ssh_exception.AuthenticationException: Authentication failed.

**Przyczyna:** Problem z kluczami SSH lub metodami autentykacji

**Rozwiązanie:**

**Krok 1: Wymuś password authentication**

W `scripts/collect_configs.py` dodaj parametr:

    connection_params = {
        'device_type': device.get('device_type'),
        'host': ip,
        'username': device.get('username'),
        'password': device.get('password'),
        'port': device.get('port', 22),
        'timeout': self.config['ssh'].get('timeout', 30),
        'auth_timeout': 60,  # Dodaj timeout dla autentykacji
        'banner_timeout': 60,
        'allow_agent': False,  # Wyłącz SSH agent
        'look_for_keys': False  # Wyłącz szukanie kluczy
    }

**Krok 2: Sprawdź algorytmy SSH**

Niektóre stare urządzenia używają starszych algorytmów. Dodaj:

    connection_params['disabled_algorithms'] = {
        'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']
    }

---

### Problem 4: "Unable to automatically determine device_type"

**Błąd:**

    ValueError: Unable to automatically determine device_type

**Przyczyna:** Netmiko nie może rozpoznać typu urządzenia (jeśli `auto_detect=true`)

**Rozwiązanie:**

**Krok 1: Ręcznie określ device_type w devices.yml**

Zamiast:

    device_type: auto

Użyj konkretnego typu:

    device_type: cisco_ios

**Krok 2: Sprawdź listę wspieranych typów**

https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md

Popularne typy:
- `cisco_ios` - Cisco IOS, IOS-XE
- `cisco_asa` - Cisco ASA Firewall
- `cisco_nxos` - Cisco Nexus
- `cisco_xr` - Cisco IOS-XR
- `juniper_junos` - Juniper JunOS
- `arista_eos` - Arista EOS
- `hp_comware` - HP Comware

---

### Problem 5: Połączenie nagle się rozłącza

**Błąd:**

    [ERROR] Socket is closed

**Przyczyna:** VTY timeout lub max sessions limit

**Rozwiązanie (Cisco):**

Zwiększ timeout na VTY lines:

    line vty 0 15
     exec-timeout 30 0
     session-limit 10

---

## 🐍 Problemy z Python i Zależnościami

### Problem 1: "python: command not found"

**System:** Linux/macOS

**Przyczyna:** Python nie jest zainstalowany lub nie jest w PATH

**Rozwiązanie:**

**Krok 1: Sprawdź czy Python jest zainstalowany**

    python3 --version

Jeśli błąd → zainstaluj Python:

**Ubuntu/Debian:**

    sudo apt update
    sudo apt install python3 python3-pip python3-venv

**macOS (Homebrew):**

    brew install python3

**Krok 2: Użyj python3 zamiast python**

W skryptach i komendach zawsze używaj `python3`:

    python3 scripts/main.py

**Krok 3: Utwórz alias (opcjonalnie)**

Dodaj do `~/.bashrc` lub `~/.zshrc`:

    alias python=python3
    alias pip=pip3

---

### Problem 2: "No module named 'netmiko'"

**Błąd:**

    ModuleNotFoundError: No module named 'netmiko'

**Przyczyna:** Pakiety nie są zainstalowane lub virtual environment nie jest aktywowany

**Rozwiązanie:**

**Krok 1: Sprawdź czy venv jest aktywowany**

Powinieneś widzieć `(venv)` na początku linii w terminalu.

Jeśli nie, aktywuj:

**Windows:**

    venv\Scripts\activate

**Linux/macOS:**

    source venv/bin/activate

**Krok 2: Zainstaluj zależności**

    pip install -r requirements.txt

**Krok 3: Sprawdź czy pakiety są zainstalowane**

    pip list | grep netmiko

Powinieneś zobaczyć:

    netmiko    4.3.0

**Krok 4: Jeśli nadal błąd, reinstaluj wszystko**

    pip uninstall -r requirements.txt -y
    pip install -r requirements.txt

---

### Problem 3: "SSL: CERTIFICATE_VERIFY_FAILED"

**Błąd (podczas pip install):**

    SSL: CERTIFICATE_VERIFY_FAILED

**Przyczyna:** Proxy korporacyjny lub firewall blokuje HTTPS

**Rozwiązanie:**

**Opcja 1: Użyj HTTP mirror (tymczasowo)**

    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

**Opcja 2: Skonfiguruj proxy**

Windows:

    set HTTP_PROXY=http://proxy.firma.pl:8080
    set HTTPS_PROXY=http://proxy.firma.pl:8080
    pip install -r requirements.txt

Linux/macOS:

    export HTTP_PROXY=http://proxy.firma.pl:8080
    export HTTPS_PROXY=http://proxy.firma.pl:8080
    pip install -r requirements.txt

**Opcja 3: Zainstaluj certyfikat korporacyjny**

Skontaktuj się z IT Support o certyfikat root CA

---

### Problem 4: "Permission denied" podczas instalacji

**Błąd:**

    PermissionError: [Errno 13] Permission denied

**Przyczyna:** Próba instalacji poza virtual environment (systemowy Python)

**Rozwiązanie:**

**Nigdy nie używaj `sudo pip install`!**

Zawsze pracuj w virtual environment:

    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt

---

### Problem 5: Konflikt wersji pakietów

**Błąd:**

    ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
    This behaviour is the source of the following dependency conflicts.

**Rozwiązanie:**

**Krok 1: Utwórz nowy venv od zera**

    deactivate
    rm -rf venv  # Linux/macOS
    rmdir /s venv  # Windows
    
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

**Krok 2: Jeśli nadal problem, zaktualizuj requirements.txt**

Sprawdź najnowsze wersje:

    pip install --upgrade netmiko openai pyyaml python-dotenv jinja2

Wygeneruj nowy requirements.txt:

    pip freeze > requirements.txt

---

## 🤖 Problemy z OpenAI API

### Problem 1: "Incorrect API key provided"

**Błąd:**

    openai.AuthenticationError: Incorrect API key provided

**Przyczyny:**

1. Brak OPENAI_API_KEY w .env
2. Błędny klucz API
3. Spacje w kluczu

**Rozwiązanie:**

**Krok 1: Sprawdź plik .env**

    OPENAI_API_KEY=sk-proj-abcdefghijklmnop...

Czy klucz zaczyna się od `sk-proj-`?  
Czy nie ma spacji na początku/końcu?

**Krok 2: Wygeneruj nowy klucz**

1. Otwórz https://platform.openai.com/api-keys
2. Zaloguj się
3. "Create new secret key"
4. Skopiuj klucz (pojawi się tylko raz!)
5. Wklej do .env

**Krok 3: Test klucza**

Utwórz plik `test_openai.py`:

    import os
    from dotenv import load_dotenv
    from openai import OpenAI
    
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.models.list()
        print("✓ API Key działa!")
        print(f"Dostępne modele: {len(response.data)}")
    except Exception as e:
        print(f"✗ Błąd: {e}")

Uruchom:

    python test_openai.py

---

### Problem 2: "Model 'gpt-5-nano' does not exist"

**Błąd:**

    openai.NotFoundError: Error code: 404 - {'error': {'message': 'Model gpt-5-nano does not exist'}}

**Przyczyna:** Błąd w nazwie modelu lub brak dostępu

**Rozwiązanie:**

**Krok 1: Sprawdź dostępne modele**

    import openai
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    models = client.models.list()
    for model in models.data:
        print(model.id)

**Krok 2: Sprawdź czy masz dostęp do GPT-5-nano**

GPT-5-nano może wymagać:
- Płatnego planu
- Whitelist (early access)
- Specjalnej organizacji OpenAI

Sprawdź https://platform.openai.com/docs/models

**Krok 3: Tymczasowo użyj innego modelu**

W `config/settings.yml` zmień:

    openai:
      model: gpt-4-turbo  # Zamiast gpt-5-nano

---

### Problem 3: Rate Limit Error

**Błąd:**

    openai.RateLimitError: Error code: 429 - Rate limit exceeded

**Przyczyna:** Zbyt wiele zapytań w krótkim czasie

**Rozwiązanie:**

**Krok 1: Sprawdź swoje limity**

https://platform.openai.com/account/limits

**Krok 2: Dodaj retry logic**

W `scripts/generate_docs.py` dodaj retry:

    from tenacity import retry, wait_exponential, stop_after_attempt
    
    @retry(wait=wait_exponential(min=4, max=60), stop=stop_after_attempt(5))
    def _call_openai_api(self, prompt):
        response = self.openai_client.responses.create(
            model=self.config['openai']['model'],
            input=prompt
        )
        return response

**Krok 3: Zmniejsz concurrent requests**

W `config/settings.yml`:

    ssh:
      max_concurrent: 2  # Zmniejsz z 5 na 2

**Krok 4: Dodaj delay między zapytaniami**

    import time
    
    # W pętli generowania dokumentacji
    for device in devices:
        generate_doc(device)
        time.sleep(5)  # Czekaj 5 sekund między zapytaniami

---

### Problem 4: Timeout podczas generowania

**Błąd:**

    openai.APITimeoutError: Request timed out

**Przyczyna:** Generowanie dokumentacji trwa zbyt długo

**Rozwiązanie:**

**Krok 1: Zwiększ timeout w settings.yml**

    openai:
      timeout: 120  # Zwiększ z 60 do 120 sekund

**Krok 2: Zmniejsz reasoning effort**

    openai:
      reasoning:
        effort: minimal  # Zamiast high

**Krok 3: Zmniejsz verbosity**

    openai:
      text:
        verbosity: low  # Zamiast high

---

### Problem 5: Insufficient Quota

**Błąd:**

    openai.InsufficientQuotaError: You exceeded your current quota

**Przyczyna:** Wykorzystałeś cały credit lub limit konta

**Rozwiązanie:**

1. Sprawdź usage: https://platform.openai.com/usage
2. Dodaj metodę płatności: https://platform.openai.com/account/billing
3. Zwiększ limit wydatków (jeśli ustawiony zbyt nisko)

---

## ⚙️ Problemy z Konfiguracją

### Problem 1: "No such file or directory: 'config/devices.yml'"

**Błąd:**

    FileNotFoundError: [Errno 2] No such file or directory: 'config/devices.yml'

**Przyczyna:** Uruchamiasz skrypt z błędnego folderu

**Rozwiązanie:**

Zawsze uruchamiaj z głównego folderu projektu:

    cd C:\Users\...\Infrastructure-Docs-Generator
    python scripts\main.py

Nie uruchamiaj z:

    cd scripts
    python main.py  # ✗ BŁĄD

---

### Problem 2: Zmienne ${VARIABLE} nie są podstawiane

**Objaw:** W logach widzisz dosłowny tekst `${SWITCH_PASSWORD}` zamiast hasła

**Przyczyna:** Plik .env nie jest ładowany lub zmienne nie są eksportowane

**Rozwiązanie:**

**Krok 1: Sprawdź czy .env istnieje**

    ls .env  # Linux/macOS
    dir .env  # Windows

**Krok 2: Sprawdź czy dotenv jest zainstalowany**

    pip list | grep python-dotenv

**Krok 3: Upewnij się że load_dotenv() jest wywołany**

W `scripts/collect_configs.py` i `generate_docs.py` na początku:

    from dotenv import load_dotenv
    load_dotenv()  # Musi być przed użyciem os.getenv()

**Krok 4: Test ręczny**

    python
    >>> from dotenv import load_dotenv
    >>> import os
    >>> load_dotenv()
    >>> print(os.getenv('SWITCH_USERNAME'))
    admin  # Powinno wyświetlić wartość

---

### Problem 3: YAML Parsing Error

**Błąd:**

    yaml.scanner.ScannerError: mapping values are not allowed here

**Przyczyna:** Błąd składni w YAML (devices.yml lub settings.yml)

**Rozwiązanie:**

**Typowe błędy w YAML:**

**Błąd 1: Brak spacji po dwukropku**

    # ✗ ZŁE
    hostname:Switch-L3
    
    # ✓ DOBRE
    hostname: Switch-L3

**Błąd 2: Niepoprawna indentacja**

    # ✗ ZŁE (mix spacji i tabów)
    - hostname: Switch
        ip: 10.10.10.1  # Tab użyty zamiast spacji
    
    # ✓ DOBRE (tylko spacje)
    - hostname: Switch
      ip: 10.10.10.1

**Błąd 3: Specjalne znaki bez cudzysłowów**

    # ✗ ZŁE
    password: My@Pass:word!
    
    # ✓ DOBRE
    password: "My@Pass:word!"

**Weryfikacja YAML online:**

http://www.yamllint.com/ - wklej zawartość pliku i sprawdź błędy

---

## 🔧 Problemy z Urządzeniami Cisco

### Problem 1: "% Invalid input detected"

**Objaw:** Konfiguracja nie jest pobierana, w logach błąd komendy

**Przyczyna:** Niekompatybilna komenda dla danej wersji IOS

**Rozwiązanie:**

**Cisco IOS/IOS-XE:**

    show running-config

**Cisco ASA:**

    show running-config

**Cisco Nexus (NX-OS):**

    show running-config
    # lub
    show startup-config

Zmień w `scripts/collect_configs.py`:

    if 'nxos' in device['device_type']:
        config = connection.send_command('show running-config', read_timeout=120)

---

### Problem 2: Konfiguracja jest obcięta (incomplete)

**Objaw:** Plik konfiguracji jest niepełny, brakuje końca

**Przyczyna:** Timeout read jest zbyt krótki dla dużych konfigów

**Rozwiązanie:**

W `scripts/collect_configs.py` zwiększ `read_timeout`:

    config = connection.send_command('show running-config', read_timeout=180)

Dla bardzo dużych urządzeń (routery z BGP full table):

    config = connection.send_command('show running-config', read_timeout=300, max_loops=1000)

---

### Problem 3: Enable password required

**Błąd:**

    ValueError: Failed to enter enable mode

**Przyczyna:** Urządzenie wymaga enable password, ale nie jest skonfigurowany

**Rozwiązanie:**

W `config/devices.yml` dodaj `secret`:

    - hostname: Switch-L3-Core
      device_type: cisco_ios
      ip: 10.10.10.1
      username: ${SWITCH_USERNAME}
      password: ${SWITCH_PASSWORD}
      secret: ${SWITCH_ENABLE_PASSWORD}  # Dodaj to
      enabled: true

W `.env` dodaj:

    SWITCH_ENABLE_PASSWORD=EnableSecretHaslo123

---

### Problem 4: More prompts nie są obsługiwane

**Objaw:** Konfiguracja się przerywa na "--More--"

**Przyczyna:** Terminal paging nie jest wyłączony

**Rozwiązanie:**

Netmiko automatycznie wysyła `terminal length 0`, ale jeśli nie działa, wymuś:

W `scripts/collect_configs.py`:

    connection = ConnectHandler(**connection_params)
    connection.send_command('terminal length 0')  # Wyłącz paging
    config = connection.send_command('show running-config')

---

### Problem 5: AAA authentication blokuje dostęp

**Objaw:** Local user nie może się zalogować (AAA required)

**Rozwiązanie:**

Na urządzeniu skonfiguruj local fallback:

    configure terminal
    aaa authentication login default group tacacs+ local
    aaa authentication enable default group tacacs+ enable

Lub użyj konta AAA zamiast lokalnego.

---

## 🌐 Problemy z Urządzeniami Juniper

### Problem 1: "Permission denied" na Juniper

**Przyczyna:** User nie ma uprawnień do `show configuration`

**Rozwiązanie:**

Na urządzeniu Juniper, nadaj uprawnienia:

    set system login user automation class super-user

Lub utwórz custom class:

    set system login class automation permissions view-configuration
    set system login user automation class animation

---

### Problem 2: Konfiguracja w formacie XML zamiast text

**Objaw:** Otrzymujesz XML zamiast czytelnej konfiguracji

**Rozwiązanie:**

Użyj odpowiedniej komendy:

    # Text format (preferred)
    show configuration | display set
    
    # lub
    show configuration | no-more

W `scripts/collect_configs.py`:

    if 'juniper' in device['device_type']:
        config = connection.send_command('show configuration | display set', read_timeout=120)

---

### Problem 3: "error: configuration database modified"

**Przyczyna:** Ktoś inny edytuje konfigurację

**Rozwiązanie:**

Poczekaj aż inna sesja skończy edycję lub:

    request system configuration rescue save
    show configuration rescue

---

## 📝 Problemy z Generowaniem Dokumentacji

### Problem 1: Dokumentacja jest pusta lub bardzo krótka

**Przyczyna:** AI nie otrzymał odpowiednich danych lub prompt jest nieprawidłowy

**Rozwiązanie:**

**Krok 1: Sprawdź czy raw config jest poprawny**

Otwórz plik z `output/raw-configs/` i zweryfikuj czy zawiera pełną konfigurację.

**Krok 2: Zwiększ verbosity w settings.yml**

    openai:
      text:
        verbosity: high  # Zamiast low

**Krok 3: Zwiększ reasoning effort**

    openai:
      reasoning:
        effort: medium  # Lub high

**Krok 4: Sprawdź czy wszystkie sekcje są włączone**

W `config/settings.yml`:

    documentation:
      sections:
        device_info: true
        interfaces: true
        vlans: true
        routing: true
        acls: true
        security: true
        features: true

---

### Problem 2: AI wymyśla informacje (hallucination)

**Objaw:** Dokumentacja zawiera informacje których nie ma w konfiguracji

**Rozwiązanie:**

**Krok 1: Popraw prompt**

W `scripts/generate_docs.py` w funkcji `_generate_prompt()` dodaj:

    prompt += """
    WAŻNE:
    - Generuj TYLKO informacje które są RZECZYWIŚCIE w konfiguracji
    - Jeśli czegoś nie ma - napisz "Nie skonfigurowane"
    - NIE wymyślaj przykładowych danych
    - NIE zakładaj standardowych konfiguracji
    """

**Krok 2: Użyj niższy reasoning effort**

    openai:
      reasoning:
        effort: minimal  # Mniej "kreatywności"

---

### Problem 3: Dokumentacja w złym języku

**Objaw:** Dokumentacja jest po angielsku zamiast po polsku

**Rozwiązanie:**

W `scripts/generate_docs.py` w promptcie dodaj na początku:

    prompt = f"""Wygeneruj dokumentację PO POLSKU dla urządzenia sieciowego.
    
    JĘZYK: Polski
    
    Urządzenie: {hostname}
    ...
    """

---

## 🚀 Problemy z Wydajnością

### Problem 1: Skrypt działa bardzo wolno

**Objaw:** Generowanie dokumentacji dla 10 urządzeń trwa > 30 minut

**Przyczyny:**

1. Zbyt niski max_concurrent
2. Wysokie reasoning effort
3. Duże konfiguracje urządzeń
4. Wolne połączenie z OpenAI API

**Rozwiązanie:**

**Krok 1: Zwiększ concurrent connections**

W `config/settings.yml`:

    ssh:
      max_concurrent: 10  # Zwiększ z 5 na 10

**Krok 2: Zmniejsz reasoning effort**

    openai:
      reasoning:
        effort: minimal  # Zamiast high

**Krok 3: Zmniejsz verbosity**

    openai:
      text:
        verbosity: low  # Zamiast high

**Krok 4: Wyłącz nieużywane sekcje**

    documentation:
      sections:
        device_info: true
        interfaces: true
        vlans: false  # Wyłącz jeśli nie używasz
        routing: true
        acls: false   # Wyłącz jeśli nie używasz
        security: true
        features: false

---

### Problem 2: Wykorzystanie pamięci RAM rośnie

**Objaw:** Python.exe zużywa coraz więcej RAM

**Rozwiązanie:**

**Krok 1: Zmniejsz concurrent connections**

    ssh:
      max_concurrent: 3

**Krok 2: Dodaj garbage collection**

W `scripts/generate_docs.py`:

    import gc
    
    # Po każdym urządzeniu
    for device in devices:
        generate_doc(device)
        gc.collect()  # Wymuś garbage collection

---

## 💻 Problemy Specyficzne dla Windows

### Problem 1: "The system cannot find the path specified"

**Przyczyna:** Ścieżka zawiera spacje i nie jest w cudzysłowach

**Rozwiązanie:**

W Task Scheduler przy tworzeniu zadania:

    Program/script: "C:\Users\Jan Kowalski\...\venv\Scripts\python.exe"

Zawsze używaj cudzysłowów gdy ścieżka zawiera spacje.

---

### Problem 2: Encoding errors (krzaczki w logach)

**Błąd:**

    UnicodeEncodeError: 'charmap' codec can't encode character

**Rozwiązanie:**

Ustaw encoding na UTF-8 w PowerShell/CMD:

    chcp 65001

Lub w Python dodaj na początku skryptu:

    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

---

### Problem 3: Task Scheduler nie uruchamia skryptu

**Zobacz szczegóły:** `WINDOWS_TASK_SCHEDULER.md` sekcja Troubleshooting

---

## 🐧 Problemy Specyficzne dla Linux/macOS

### Problem 1: "Permission denied" na skryptach

**Rozwiązanie:**

Nadaj uprawnienia wykonywania:

    chmod +x scripts/*.py
    chmod +x run_generator.sh

---

### Problem 2: Cron nie uruchamia skryptu

**Sprawdź logi cron:**

    grep CRON /var/log/syslog

**Typowe problemy:**

1. Ścieżka do Python nie jest pełna
2. Virtual environment nie jest aktywowany
3. Brak zmiennych środowiskowych

**Poprawny wpis crontab:**

    0 2 * * * cd /home/user/Infrastructure-Docs-Generator && /home/user/Infrastructure-Docs-Generator/venv/bin/python scripts/main.py >> /home/user/Infrastructure-Docs-Generator/output/logs/cron.log 2>&1

---

## ❓ FAQ - Najczęściej Zadawane Pytania

### Q1: Czy mogę używać tego na Windows Server?

**A:** Tak, działa identycznie jak na Windows 10/11.

---

### Q2: Ile urządzeń mogę monitorować jednocześnie?

**A:** Teoretycznie nieograniczoną liczbę. Praktycznie:
- 1-50 urządzeń: Bez problemu
- 50-200 urządzeń: Zwiększ timeout i concurrent connections
- 200+: Rozważ segmentację (osobne zadania dla różnych lokacji)

---

### Q3: Czy muszę mieć dostęp do internetu?

**A:** Tak, wymagany dostęp do:
- OpenAI API (generowanie dokumentacji)
- Urządzeń sieciowych (SSH)
- PyPI (instalacja pakietów)

---

### Q4: Czy mogę używać na air-gapped sieci (bez internetu)?

**A:** Możesz zbierać konfiguracje (`--collect-only`), ale generowanie dokumentacji wymaga OpenAI API. Alternatywnie użyj lokalnego LLM (wymaga modyfikacji kodu).

---

### Q5: Jak często powinienem aktualizować dokumentację?

**A:** Zalecane:
- Produkcja: Codziennie w nocy
- Dev/Test: Co tydzień
- Po zmianach: Ręcznie

---

### Q6: Czy backup konfiguracji jest szyfrowany?

**A:** Nie, pliki są przechowywane w plain text. Zalecamy:
- Folder `output/` powinien być w .gitignore
- Backup na zaszyfrowanym dysku/NAS
- Uprawnienia 700 na Linux (tylko właściciel może czytać)

---

### Q7: Co zrobić gdy zmienię hasło na urządzeniu?

**A:** Zmień hasło w pliku `.env` i uruchom ponownie. Stare backupy pozostaną dostępne.

---

### Q8: Czy mogę używać z urządzeniami innych vendorów (HP, Arista)?

**A:** Tak, Netmiko wspiera 200+ typów urządzeń. Sprawdź listę:  
https://github.com/ktbyers/netmiko/blob/develop/PLATFORMS.md

---

## 🐛 Tryb Debug

### Włączenie Debug Mode

W `config/settings.yml`:

    advanced:
      debug_mode: true

Oraz w `logging`:

    logging:
      level: DEBUG  # Zamiast INFO

### Ręczny Debug Krok po Kroku

**Test 1: Python i zależności**

    python --version
    pip list

**Test 2: Połączenie SSH (ręczne)**

    ssh admin@10.10.10.1

**Test 3: Netmiko test**

Utwórz `test_netmiko.py`:

    from netmiko import ConnectHandler
    
    device = {
        'device_type': 'cisco_ios',
        'host': '10.10.10.1',
        'username': 'admin',
        'password': 'haslo123',
        'timeout': 30
    }
    
    try:
        connection = ConnectHandler(**device)
        print("✓ Połączenie OK")
        
        output = connection.send_command('show version')
        print(output)
        
        connection.disconnect()
    except Exception as e:
        print(f"✗ Błąd: {e}")

Uruchom:

    python test_netmiko.py

**Test 4: OpenAI API test**

(Zobacz sekcję "Problemy z OpenAI API" → Test klucza)

---

## 🆘 Gdzie Szukać Pomocy

### 1. Logi

**Zawsze najpierw sprawdź logi:**

    output/logs/collector.log
    output/logs/generator.log
    output/logs/scheduler.log

### 2. GitHub Issues

Projekt: https://github.com/sebastian-c87/my-it-profile-hub/issues

### 3. Dokumentacja Netmiko

https://github.com/ktbyers/netmiko

### 4. Dokumentacja OpenAI

https://platform.openai.com/docs

### 5. Stack Overflow

Tagi: `netmiko`, `python`, `openai-api`

---

## 📞 Kontakt

Jeśli żaden z powyższych sposobów nie pomógł:

1. Zbierz informacje:
   - Wersja Python: `python --version`
   - Wersje pakietów: `pip list`
   - Pełne logi błędów
   - Kroki reprodukcji problemu

2. Utwórz Issue na GitHubie z tagiem `bug`

3. Dołącz:
   - Opis problemu
   - Komunikaty błędów (bez wrażliwych danych!)
   - Wersje oprogramowania
   - System operacyjny

---

**Data aktualizacji:** 2026-01-28  
**Wersja:** 1.0  
**Status:** Kompletny przewodnik troubleshooting
