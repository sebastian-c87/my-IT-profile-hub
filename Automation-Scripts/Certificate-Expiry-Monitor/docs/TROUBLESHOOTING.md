# 🔧 Troubleshooting Guide - Certificate Expiry Monitor

Kompletny przewodnik rozwiązywania problemów z szczegółowymi diagnozami i rozwiązaniami.

---

## 📋 Spis Treści

- [Problemy z Instalacją](#problemy-z-instalacją)
- [Problemy z Konfiguracją](#problemy-z-konfiguracją)
- [Problemy z Połączeniem SSL/TLS](#problemy-z-połączeniem-ssltls)
- [Problemy z Alertami](#problemy-z-alertami)
- [Problemy z Docker](#problemy-z-docker)
- [Problemy z Raportami](#problemy-z-raportami)
- [Problemy Wydajnościowe](#problemy-wydajnościowe)
- [Błędy Python](#błędy-python)
- [FAQ - Najczęstsze Pytania](#faq---najczęstsze-pytania)

---

## 🚨 Problemy z Instalacją

### Problem 1.1: `python: command not found`

**Objawy:**
```
bash: python: command not found
```

**Przyczyna:** Python nie jest zainstalowany lub nie w PATH.

**Diagnoza:**
```bash
# Sprawdź czy Python3 jest dostępny
python3 --version

# Sprawdź lokalizację Python
which python3

# Windows - sprawdź PATH
echo %PATH%
```

**Rozwiązanie:**

#### Windows
1. Pobierz Python z: https://www.python.org/downloads/
2. Uruchom instalator
3. **ZAZNACZ "Add Python to PATH"**
4. Restart CMD
5. Weryfikacja: `python --version`

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### macOS
```bash
brew install python3
```

**Alternatywnie:** Użyj `python3` zamiast `python`:
```bash
python3 scripts/main.py
```

---

### Problem 1.2: `pip: command not found`

**Objawy:**
```
bash: pip: command not found
```

**Rozwiązanie:**

#### Metoda 1: Zainstaluj pip
```bash
# Linux
sudo apt install python3-pip

# macOS
brew install python3  # pip jest wbudowany

# Windows
python -m ensurepip --upgrade
```

#### Metoda 2: Użyj `python -m pip`
```bash
python -m pip install -r requirements.txt
```

---

### Problem 1.3: `ModuleNotFoundError: No module named 'cryptography'`

**Objawy:**
```python
Traceback (most recent call last):
  File "scripts/main.py", line 21, in <module>
    from cryptography import x509
ModuleNotFoundError: No module named 'cryptography'
```

**Przyczyna:** Biblioteki nie zostały zainstalowane.

**Rozwiązanie:**
```bash
# Upewnij się że venv jest aktywny
# (powinien być (venv) w promptu)

pip install -r requirements.txt
```

**Jeśli nadal błąd:**
```bash
# Zainstaluj ręcznie
pip install cryptography pyOpenSSL PyYAML requests jinja2 python-dateutil
```

**Weryfikacja:**
```bash
pip list | grep cryptography
# Powinno pokazać: cryptography X.X.X
```

---

### Problem 1.4: `Permission denied` podczas instalacji

**Objawy:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Przyczyna:** Próba instalacji globalnie bez uprawnień sudo.

**Rozwiązanie A: Użyj venv (ZALECANE)**
```bash
# Utwórz venv
python3 -m venv venv

# Aktywuj
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Zainstaluj
pip install -r requirements.txt
```

**Rozwiązanie B: Instalacja dla użytkownika**
```bash
pip install --user -r requirements.txt
```

**Rozwiązanie C: Sudo (NIE ZALECANE)**
```bash
sudo pip install -r requirements.txt
```

---

### Problem 1.5: `SSL: CERTIFICATE_VERIFY_FAILED` podczas `pip install`

**Objawy:**
```
Could not fetch URL https://pypi.org/simple/cryptography/: There was a problem confirming the ssl certificate
```

**Przyczyna:** Firewall korporacyjny, proxy, lub problem z certyfikatami CA.

**Rozwiązanie A: Użyj HTTP (tymczasowo)**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**Rozwiązanie B: Skonfiguruj proxy**
```bash
# Ustaw zmienne środowiskowe
export HTTP_PROXY=http://proxy.firma.pl:8080
export HTTPS_PROXY=http://proxy.firma.pl:8080

pip install -r requirements.txt
```

**Rozwiązanie C: Zaktualizuj certyfikaty CA**
```bash
# Linux
sudo apt install ca-certificates
sudo update-ca-certificates

# macOS
/Applications/Python\ 3.11/Install\ Certificates.command
```

---

## ⚙️ Problemy z Konfiguracją

### Problem 2.1: `FileNotFoundError: [Errno 2] No such file or directory: 'config/domains.yml'`

**Objawy:**
```python
FileNotFoundError: [Errno 2] No such file or directory: 'config/domains.yml'
```

**Przyczyna:** Uruchamiasz skrypt z niewłaściwego folderu.

**Rozwiązanie:**
```bash
# Sprawdź gdzie jesteś
pwd  # Linux/Mac
cd   # Windows

# Przejdź do głównego folderu projektu
cd /path/to/Certificate-Expiry-Monitor

# Sprawdź strukturę
ls -la config/

# Uruchom
python scripts/main.py
```

**Alternatywnie:** Podaj pełną ścieżkę
```bash
python /full/path/to/scripts/main.py
```

---

### Problem 2.2: `yaml.scanner.ScannerError: while scanning` w domains.yml

**Objawy:**
```
yaml.scanner.ScannerError: while scanning for the next token
found character '\t' that cannot start any token
  in "config/domains.yml", line 12, column 1
```

**Przyczyna:** Błąd składni YAML (TAB zamiast spacji, zły indent).

**Diagnoza:**
```bash
# Sprawdź plik pod kątem TAB
cat -A config/domains.yml | grep "^I"
```

**Rozwiązanie:**

#### Zasady YAML:
- **Używaj SPACJI, nie TAB**
- **Zachowaj jednolity indent (2 lub 4 spacje)**
- **Dwukropek musi mieć spację po sobie: `key: value`**

**Przykład DOBRY:**
```yaml
domains:
  - host: example.com    # ← 2 spacje indent
    port: 443            # ← 2 spacje indent
    name: "Example"
    enabled: true
```

**Przykład ZŁY:**
```yaml
domains:
	- host: example.com     # ← TAB (źle!)
  - host:example.com        # ← Brak spacji po dwukropku (źle!)
   - host: example.com      # ← Nieparzysty indent (źle!)
```

**Narzędzie do walidacji:**
```bash
# Online: http://www.yamllint.com/

# CLI (jeśli zainstalowany)
yamllint config/domains.yml
```

---

### Problem 2.3: Zmienne środowiskowe z `.env` nie są wczytywane

**Objawy:**
```
Using default value for SMTP_HOST: localhost
```

**Przyczyna:** Plik `.env` nie istnieje lub jest w złym miejscu.

**Diagnoza:**
```bash
# Sprawdź czy plik istnieje
ls -la .env

# Sprawdź zawartość
cat .env
```

**Rozwiązanie:**
```bash
# Skopiuj przykładowy plik
cp .env.example .env

# Edytuj wartości
nano .env  # Linux/Mac
notepad .env  # Windows
```

**Format pliku `.env`:**
```env
# NIE UŻYWAJ spacji wokół =
SMTP_HOST=smtp.gmail.com  # ✅ DOBRZE
SMTP_HOST = smtp.gmail.com  # ❌ ŹLE (spacje)

# NIE UŻYWAJ cudzysłowów (chyba że wartość zawiera spacje)
SMTP_USERNAME=user@gmail.com  # ✅ DOBRZE
SMTP_USERNAME="user@gmail.com"  # ❌ NIEPOTRZEBNE

# Cudzysłowy tylko gdy potrzebne
EMAIL_TO=admin@example.com,devops@example.com  # ✅ DOBRZE
```

---

### Problem 2.4: `YAML Merge Key Not Supported` w settings.yml

**Objawy:**
```
yaml.constructor.ConstructorError: could not determine a constructor for the tag 'tag:yaml.org,2002:merge'
```

**Przyczyna:** Używasz YAML merge keys (`<<:`) które nie są wspierane przez PyYAML domyślnie.

**Rozwiązanie:** Nie używaj merge keys, zduplikuj wartości.

**Zamiast:**
```yaml
defaults: &defaults
  timeout: 10
  verify: true

production:
  <<: *defaults
  host: prod.example.com
```

**Użyj:**
```yaml
production:
  timeout: 10
  verify: true
  host: prod.example.com
```

---

## 🔒 Problemy z Połączeniem SSL/TLS

### Problem 3.1: `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate`

**Objawy:**
```
Error checking localhost:8443: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1028)
```

**Przyczyna:** Skrypt weryfikuje certyfikaty i odrzuca self-signed (dla localhost/Docker).

**Rozwiązanie A: Zmień `.env`**
```env
ALLOW_SELF_SIGNED=True
```

**Rozwiązanie B: Popraw `cert_checker.py`**

Znajdź linię ~125 w `scripts/cert_checker.py`:
```python
# Było:
if not self.verify:
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

# Zmień na:
if not self.verify or hostname in ['localhost', '127.0.0.1', '::1']:
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
```

**Rozwiązanie C: Wyłącz weryfikację globalnie (tylko testy!)**

Na początku `cert_checker.py` dodaj:
```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

⚠️ **UWAGA:** To wyłącza weryfikację dla WSZYSTKICH połączeń! Tylko dla testów!

---

### Problem 3.2: `[Errno 111] Connection refused`

**Objawy:**
```
Error checking example.com:443: [Errno 111] Connection refused
```

**Przyczyna:** Serwer nie odpowiada na tym porcie lub jest wyłączony.

**Diagnoza:**
```bash
# Test połączenia
telnet example.com 443

# Alternatywnie (curl)
curl -v https://example.com

# Sprawdź ping
ping example.com
```

**Możliwe przyczyny:**
1. **Serwer jest wyłączony** - Skontaktuj się z adminem
2. **Firewall blokuje** - Sprawdź reguły firewall
3. **Zły port** - Sprawdź czy to rzeczywiście 443
4. **DNS nie działa** - Sprawdź `nslookup example.com`

**Rozwiązanie:**
```bash
# Sprawdź czy port jest otwarty (Linux)
nmap -p 443 example.com

# Sprawdź czy port jest otwarty (Windows)
Test-NetConnection -ComputerName example.com -Port 443
```

---

### Problem 3.3: `[Errno 10060] A connection attempt failed` (Windows)

**Objawy:**
```
Error checking example.com:443: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time
```

**Przyczyna:** Timeout połączenia (10 sekund domyślnie).

**Rozwiązanie A: Zwiększ timeout**

Edytuj `config/settings.yml`:
```yaml
timeouts:
  connection: 30  # Zwiększ z 10 do 30 sekund
  handshake: 30
```

**Rozwiązanie B: Sprawdź proxy**
```bash
# Windows
netsh winhttp show proxy

# Jeśli używasz proxy, skonfiguruj:
set HTTP_PROXY=http://proxy.firma.pl:8080
set HTTPS_PROXY=http://proxy.firma.pl:8080
```

---

### Problem 3.4: `[WinError 10053] An established connection was aborted by the software in your host machine`

**Objawy:**
```
Error checking localhost:8443: [WinError 10053] Nawiązane połączenie zostało przerwane przez oprogramowanie
```

**Przyczyna:** Windows Firewall lub Antywirus blokuje połączenie.

**Diagnoza:**
```bash
# Test curl
curl -k https://localhost:8443
```

**Rozwiązanie A: Dodaj wyjątek w Windows Firewall**

PowerShell (jako Administrator):
```powershell
New-NetFirewallRule -DisplayName "Cert Monitor Docker" -Direction Inbound -Protocol TCP -LocalPort 8443,8444,8445 -Action Allow
```

**Rozwiązanie B: Tymczasowo wyłącz Firewall (test)**
1. Win + R → `firewall.cpl`
2. "Wyłącz Zaporę Windows" (sieć prywatna)
3. Test: `python scripts/main.py`
4. **Włącz ponownie Firewall!**

**Rozwiązanie C: Wyłącz SSL Scanning w Antywirus**

Kaspersky/Avast/Norton często skanują ruch SSL i przerywają połączenie:
- Otwórz Antywirus
- Ustawienia → Sieć
- Wyłącz "HTTPS Scanning" / "SSL Filtering"

---

### Problem 3.5: `[SSL] unknown protocol` lub `wrong version number`

**Objawy:**
```
Error checking example.com:80: [SSL] unknown protocol (_ssl.c:1000)
```

**Przyczyna:** Próbujesz połączyć SSL do portu HTTP (80 zamiast 443).

**Rozwiązanie:**

Popraw `domains.yml`:
```yaml
# ŹLE:
- host: example.com
  port: 80  # ← HTTP, nie HTTPS!
  protocol: https

# DOBRZE:
- host: example.com
  port: 443  # ← HTTPS
  protocol: https
```

---

### Problem 3.6: `certificate has expired` (ale certyfikat jest ważny!)

**Objawy:**
```
Error checking example.com:443: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired
```

**Przyczyna:** Zegar systemowy jest źle ustawiony.

**Diagnoza:**
```bash
# Sprawdź datę i czas
date  # Linux/Mac
echo %date% %time%  # Windows
```

**Rozwiązanie:**

#### Windows
1. Win + R → `timedate.cpl`
2. "Change date and time"
3. Ustaw prawidłową datę i czas
4. Włącz "Set time automatically"

#### Linux
```bash
# Synchronizuj czas przez NTP
sudo timedatectl set-ntp true

# Weryfikacja
timedatectl status
```

#### macOS
```bash
# System Preferences → Date & Time
# Zaznacz "Set date and time automatically"
```

---

## 📧 Problemy z Alertami

### Problem 4.1: `(535, b'5.7.8 Username and Password not accepted')` - Gmail

**Objawy:**
```
Failed to send email alert: (535, b'5.7.8 Username and Password not accepted. For more information, go to https://support.google.com/mail/?p=BadCredentials')
```

**Przyczyna:** Gmail wymaga **hasła aplikacji**, nie zwykłego hasła.

**Rozwiązanie:**

#### Krok 1: Włącz 2FA (jeśli nie masz)
1. Idź do: https://myaccount.google.com/security
2. "2-Step Verification" → Włącz

#### Krok 2: Wygeneruj Hasło Aplikacji
1. Idź do: https://myaccount.google.com/apppasswords
2. "Select app" → **Mail**
3. "Select device" → **Other (Custom name)** → "Cert Monitor"
4. Kliknij **Generate**
5. **Skopiuj 16-znakowe hasło** (np. `abcd efgh ijkl mnop`)

#### Krok 3: Zaktualizuj `.env`
```env
SMTP_USERNAME=twoj-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop  # ← 16-znakowe hasło (bez spacji!)
```

#### Krok 4: Test
```bash
python scripts/main.py --host google.com --threshold 1000
# Powinien wysłać alert (bo threshold = 1000 dni)
```

---

### Problem 4.2: `Slack alert failed: 404 - no_team`

**Objawy:**
```
Slack alert failed: 404 - no_team
```

**Przyczyna:** Zły Slack Webhook URL lub webhook został usunięty.

**Rozwiązanie:**

#### Krok 1: Utwórz Nowy Incoming Webhook
1. Idź do: https://api.slack.com/messaging/webhooks
2. Kliknij **"Create your Slack app"**
3. **"From scratch"** → Nazwa: "Cert Monitor" → Workspace
4. **"Incoming Webhooks"** → Włącz
5. **"Add New Webhook to Workspace"** → Wybierz kanał (np. #devops)
6. **Skopiuj Webhook URL** (np. `https://hooks.slack.com/services/T00/B00/XXX`)

#### Krok 2: Zaktualizuj `.env`
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00/B00/XXX
SLACK_ENABLED=True
```

#### Krok 3: Test
```bash
# Test webhook przez curl
curl -X POST https://hooks.slack.com/services/T00/B00/XXX \
     -H 'Content-Type: application/json' \
     -d '{"text":"Test from Cert Monitor"}'
```

Powinieneś zobaczyć wiadomość na Slack!

---

### Problem 4.3: Teams Alert nie działa (brak błędu)

**Objawy:**
```
[INFO] Teams alert sent for localhost:8444
```
Ale na Teams nic nie przychodzi.

**Przyczyna:** Zły format Webhook URL lub webhook wygasł.

**Rozwiązanie:**

#### Krok 1: Utwórz Nowy Incoming Webhook w Teams
1. Otwórz **Microsoft Teams**
2. Przejdź do kanału (np. "DevOps")
3. Kliknij **"..." (More options)** → **"Connectors"**
4. Znajdź **"Incoming Webhook"** → **Configure**
5. Nazwa: "Cert Monitor" → Upload Image (opcjonalne)
6. **Skopiuj URL** (np. `https://outlook.office.com/webhook/abc.../IncomingWebhook/...`)

#### Krok 2: Zaktualizuj `.env`
```env
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/.../IncomingWebhook/...
TEAMS_ENABLED=True
```

#### Krok 3: Test przez curl
```bash
curl -X POST https://outlook.office.com/webhook/.../IncomingWebhook/... \
     -H 'Content-Type: application/json' \
     -d '{"text":"Test from Cert Monitor"}'
```

---

### Problem 4.4: Alerty nie są wysyłane mimo `--check-now`

**Objawy:**
```
✓ All certificates OK - no alerts needed
```
Ale certyfikat wygasa za 5 dni (powinien być CRITICAL).

**Przyczyna:** Używasz `--no-alerts` LUB progi alertów są źle skonfigurowane.

**Diagnoza:**
```bash
# Sprawdź czy używasz --no-alerts
python scripts/main.py --help

# Sprawdź progi w settings.yml
cat config/settings.yml | grep -A 5 thresholds
```

**Rozwiązanie:**

#### Opcja A: Usuń `--no-alerts`
```bash
# Zamiast:
python scripts/main.py --check-now --no-alerts

# Użyj:
python scripts/main.py --check-now
```

#### Opcja B: Zmień progi w `settings.yml`
```yaml
thresholds:
  warning_days: 30  # Domyślnie 30
  critical_days: 7   # Domyślnie 7
```

#### Opcja C: Użyj CLI `--threshold`
```bash
python scripts/main.py --check-now --threshold 14
# Wyśle alert gdy certyfikat < 14 dni
```

---

## 🐳 Problemy z Docker

### Problem 5.1: `docker: command not found`

**Objawy:**
```bash
bash: docker: command not found
```

**Przyczyna:** Docker nie jest zainstalowany.

**Rozwiązanie:** Zobacz [DOCKER_TESTING.md](DOCKER_TESTING.md#instalacja-docker)

---

### Problem 5.2: `Cannot connect to the Docker daemon`

**Objawy:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

**Rozwiązanie:**

#### Windows/Mac
- Uruchom **Docker Desktop**
- Poczekaj aż ikona Docker będzie zielona (dolny prawy róg)

#### Linux
```bash
# Sprawdź status
sudo systemctl status docker

# Uruchom Docker
sudo systemctl start docker

# Włącz autostart
sudo systemctl enable docker

# Dodaj użytkownika do grupy docker (bez sudo)
sudo usermod -aG docker $USER

# WYLOGUJ SIĘ i zaloguj ponownie!
```

---

### Problem 5.3: `Container keeps restarting` (status: Restarting)

**Objawy:**
```bash
docker ps
# STATUS: Restarting (1) 3 seconds ago
```

**Przyczyna:** Nginx crashuje przy starcie (błąd konfiguracji).

**Diagnoza:**
```bash
docker logs cert-test-nginx
```

**Najczęstsze błędy:**

#### Błąd A: `nginx: [emerg] cannot load certificate`
```
nginx: [emerg] cannot load certificate "/etc/nginx/certs/expired/cert.pem": BIO_new_file() failed
```

**Rozwiązanie:** Brak certyfikatu - wygeneruj ponownie:
```bash
cd docker
docker run --rm -v "%cd%\nginx\certs\expired":/certs -w /certs alpine:latest sh -c "apk add --no-cache openssl && openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 1 -subj '/CN=expired.test.local'"

docker-compose restart
```

#### Błąd B: `SSL_CTX_use_PrivateKey failed: key values mismatch`
```
nginx: [emerg] SSL_CTX_use_PrivateKey("/etc/nginx/certs/expired/key.pem") failed (SSL: error:05800074:x509 certificate routines::key values mismatch)
```

**Rozwiązanie:** Certyfikat i klucz nie pasują - usuń i wygeneruj ponownie:
```bash
cd docker/nginx/certs/expired
rm cert.pem key.pem

# Wygeneruj przez Docker (Windows)
docker run --rm -v "%cd%":/certs -w /certs alpine:latest sh -c "apk add --no-cache openssl && openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 1 -subj '/CN=expired.test.local'"

cd ../../..
docker-compose restart
```

#### Błąd C: `unknown directive "﻿#"` (BOM w pliku)
```
nginx: [emerg] unknown directive "﻿#" in /etc/nginx/nginx.conf:12
```

**Rozwiązanie:** Plik `nginx.conf` ma BOM (Byte Order Mark):
1. Otwórz `docker/nginx/nginx.conf` w VS Code
2. Prawy dolny róg: "UTF-8 with BOM"
3. Kliknij → "Save with Encoding" → "UTF-8" (bez BOM)
4. Zapisz (Ctrl+S)
5. `docker-compose restart`

---

### Problem 5.4: `Port 8443 already in use`

**Objawy:**
```
Error starting userland proxy: listen tcp 0.0.0.0:8443: bind: address already in use
```

**Przyczyna:** Inny proces używa portu 8443.

**Diagnoza:**
```bash
# Windows
netstat -ano | findstr :8443

# Linux/Mac
lsof -i :8443
```

**Rozwiązanie A:** Zabij proces
```bash
# Windows
taskkill /PID 1234 /F

# Linux/Mac
kill -9 1234
```

**Rozwiązanie B:** Zmień port w `docker-compose.yml`
```yaml
ports:
  - "9443:8443"  # ← Zmień 8443 (host) na 9443
```

---

## 📊 Problemy z Raportami

### Problem 6.1: Raport HTML nie jest generowany

**Objawy:**
```
ls output/reports/
# Pusty folder
```

**Diagnoza:**
```bash
# Sprawdź logi
python scripts/main.py --check-now --verbose
```

**Możliwe przyczyny:**

#### Przyczyna A: Brak uprawnień zapisu
```bash
# Sprawdź uprawnienia
ls -la output/reports/

# Nadaj uprawnienia
chmod 755 output/reports/  # Linux/Mac
```

#### Przyczyna B: Błąd w szablonie Jinja2
```
jinja2.exceptions.TemplateNotFound: report_template.html
```

**Rozwiązanie:** Sprawdź czy folder `templates/` istnieje:
```bash
ls -la templates/
# Powinien zawierać: report_template.html
```

#### Przyczyna C: Brak biblioteki Jinja2
```bash
pip install jinja2
```

---

### Problem 6.2: Raport CSV ma złe kodowanie (krzaczki)

**Objawy:**
```
Otwierasz CSV w Excel i widzisz: "Ä™Å›Ä‡Ä…Å¼Å¼Ã³Å‚"
```

**Przyczyna:** Excel domyślnie używa Windows-1250, a CSV jest w UTF-8.

**Rozwiązanie A: Otwórz CSV poprawnie w Excel**
1. Excel → **Data** → **From Text/CSV**
2. Wybierz plik CSV
3. **File Origin:** `65001: Unicode (UTF-8)`
4. **Delimiter:** Comma
5. **Load**

**Rozwiązanie B: Zmień encoding w `settings.yml`**
```yaml
reports:
  csv_encoding: windows-1250  # Zamiast UTF-8
```

---

### Problem 6.3: JSON raport jest za duży (>10MB)

**Objawy:**
```
output/reports/certificate_report_*.json: 15 MB
```

**Przyczyna:** Bardzo dużo certyfikatów (200+) z pełnymi szczegółami.

**Rozwiązanie A: Włącz kompresję**
```yaml
reports:
  compress_json: true  # Generuj .json.gz
```

**Rozwiązanie B: Ogranicz szczegóły**
```yaml
reports:
  json_minimal: true  # Tylko najważniejsze pola
```

**Rozwiązanie C: Split na wiele plików**
```bash
python scripts/main.py --check-now --split-reports 50
# Generuj osobny plik co 50 certyfikatów
```

---

## ⚡ Problemy Wydajnościowe

### Problem 7.1: Skrypt działa bardzo wolno (>10 minut)

**Objawy:**
```
Checking 200 hosts...
[10 minutes later...]
Still checking...
```

**Przyczyna:** Zbyt mało workerów concurrent lub timeout jest za długi.

**Rozwiązanie A: Zwiększ liczbę workerów**

Edytuj `config/settings.yml`:
```yaml
concurrent:
  max_workers: 20  # Zwiększ z 10 do 20
```

**Rozwiązanie B: Zmniejsz timeout**
```yaml
timeouts:
  connection: 5   # Zmniejsz z 10 do 5 sekund
  handshake: 5
```

**Rozwiązanie C: Wyłącz powolne hosty tymczasowo**
```yaml
domains:
  - host: very-slow-server.com
    enabled: false  # ← Wyłącz tymczasowo
```

---

### Problem 7.2: Skrypt zużywa 100% CPU

**Objawy:**
```bash
top
# python3: 100% CPU
```

**Przyczyna:** Zbyt wiele workerów concurrent lub pętla nieskończona.

**Rozwiązanie:**
```yaml
concurrent:
  max_workers: 5  # Zmniejsz z 20 do 5
```

---

### Problem 7.3: Timeout przy sprawdzaniu niektórych hostów

**Objawy:**
```
Error checking slow-server.com:443: [Errno 110] Connection timed out
```

**Rozwiązanie:**

Dla konkretnego hosta ustaw dłuższy timeout w `domains.yml`:
```yaml
- host: slow-server.com
  port: 443
  timeout: 30  # ← Custom timeout (domyślnie 10s)
  enabled: true
```

---

## 🐍 Błędy Python

### Problem 8.1: `AttributeError: 'NoneType' object has no attribute 'get_attributes_for_oid'`

**Objawy:**
```python
AttributeError: 'NoneType' object has no attribute 'get_attributes_for_oid'
  File "scripts/cert_checker.py", line 180, in _get_common_name
```

**Przyczyna:** Certyfikat nie ma pola Common Name (CN).

**Rozwiązanie:** To jest obsłużone w kodzie (zwraca "N/A"). Jeśli widzisz ten błąd, zaktualizuj `cert_checker.py`:
```python
def _get_common_name(self, name: x509.Name) -> str:
    try:
        cn = name.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
        return cn.value if cn else "N/A"  # ← Dodaj 
    except Exception:
        return "N/A"
```

---

### Problem 8.2: `TypeError: 'tuple' object is not callable`

**Objawy:**
```python
TypeError: 'tuple' object is not callable
  File "scripts/cert_checker.py", line 75, in check_certificate
```

**Przyczyna:** Błąd w kodzie - próbujesz wywołać tuple jak funkcję.

**Rozwiązanie:** Sprawdź `cert_checker.py` linia 75. Prawdopodobnie masz:
```python
# ŹLE:
hostname = hostname()

# DOBRZE:
hostname = str(hostname)
```

---

### Problem 8.3: `KeyError: 'hostname'` przy parsowaniu JSON

**Objawy:**
```python
KeyError: 'hostname'
  File "scripts/report_generator.py", line 120
```

**Przyczyna:** JSON z poprzedniej wersji (stary format).

**Rozwiązanie:** Usuń stare raporty:
```bash
rm output/reports/*
python scripts/main.py --check-now
```

---

## ❓ FAQ - Najczęstsze Pytania

### Q1: Jak często uruchamiać skrypt?

**Rekomendacja:**
- **Produkcja:** Raz dziennie (o 9:00)
- **Staging:** Raz na tydzień
- **Docker testy:** Ręcznie

---

### Q2: Czy skrypt może odnowić certyfikaty automatycznie?

**NIE.** Skrypt **tylko monitoruje** i **wysyła alerty**. Odnowienie certyfikatów musisz zrobić ręcznie lub przez:
- **Let's Encrypt:** `certbot renew`
- **cert-manager (K8s):** Automatyczne
- **ACM (AWS):** Automatyczne

---

### Q3: Czy mogę monitorować certyfikaty wewnętrzne (self-signed)?

**TAK.** Ustaw w `.env`:
```env
ALLOW_SELF_SIGNED=True
```

---

### Q4: Czy skrypt działa na Windows Server 2012?

**TAK**, jeśli:
- Python 3.8+ jest zainstalowany
- OpenSSL jest dostępny (wbudowany w Python)

---

### Q5: Czy mogę sprawdzać certyfikaty w intranetcie (bez internetu)?

**TAK.** Skrypt działa w sieci lokalnej. Sprawdzi dowolny host dostępny przez sieć (LAN, VPN).

---

### Q6: Jak długo działają logi?

**Domyślnie 30 dni.** Zmień w `settings.yml`:
```yaml
reports:
  retention_days: 90  # Zachowaj 90 dni
```

---

### Q7: Czy mogę integrować z Prometheus?

**TAK.** Użyj JSON raportów jako źródło dla custom exporter:
```bash
python scripts/prometheus_exporter.py --input output/reports/certificate_report_latest.json --port 9090
```

---

### Q8: Skrypt nie wykrywa że certyfikat wygasł wczoraj. Dlaczego?

**Sprawdź zegar systemowy:**
```bash
date
```

Jeśli zegar jest źle ustawiony, zaktualizuj czas (NTP).

---

### Q9: Czy mogę monitorować certyfikaty klienckie (mTLS)?

**NIE bezpośrednio.** Skrypt sprawdza tylko certyfikaty serwerowe. Dla mTLS potrzebny jest custom script.

---

### Q10: Błąd `ImportError: cannot import name 'x509'`. Co robić?

**Rozwiązanie:**
```bash
pip uninstall cryptography pyOpenSSL
pip install --upgrade cryptography pyOpenSSL
```

---

## 📞 Dalsze Wsparcie

### Jeśli Nadal Masz Problem:

1. **Sprawdź logi szczegółowe:**
   ```bash
   python scripts/main.py --check-now --verbose > debug.log 2>&1
   ```

2. **Zgłoś issue na GitHub:**
   https://github.com/sebastian-c87/my-IT-profile-hub/issues

3. **Dołącz:**
   - Output z `--verbose`
   - Wersję Python (`python --version`)
   - System operacyjny
   - Plik `domains.yml` (bez wrażliwych danych!)

---

**To wszystko!** Masz rozwiązania na 99% problemów! 🎉
