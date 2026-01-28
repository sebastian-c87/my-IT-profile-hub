# 🛠️ Skrypty Generujące Certyfikaty Testowe

Ten folder zawiera skrypty Bash, które automatycznie generują certyfikaty SSL/TLS w różnych stanach dla środowiska testowego Docker.

---

## 📂 Zawartość Folderu

- `generate-valid-cert.sh` - Generuje certyfikat ważny przez 90 dni
- `generate-expiring-cert.sh` - Generuje certyfikat wygasający za 7 dni
- `generate-expired-cert.sh` - Generuje certyfikat już wygasły (lub wygasający za 1 dzień)
- `README.md` - Ten plik (instrukcja użycia)

---

## 🚀 Jak Uruchomić Skrypty?

### Metoda 1: Bezpośrednio w Linux/macOS

Jeśli pracujesz na systemie Unix-like:

    cd docker/scripts
    chmod +x *.sh
    
    ./generate-valid-cert.sh
    ./generate-expiring-cert.sh
    ./generate-expired-cert.sh

### Metoda 2: Przez Docker (Windows/Linux/macOS)

Jeśli pracujesz na Windows lub nie masz Bash:

    cd docker
    docker run --rm -v "%cd%":/workspace -w /workspace/scripts alpine:latest sh -c "apk add --no-cache openssl bash && chmod +x *.sh && ./generate-valid-cert.sh && ./generate-expiring-cert.sh && ./generate-expired-cert.sh"

**Wyjaśnienie komendy:**
- `docker run --rm` - Uruchom kontener i usuń go po zakończeniu
- `-v "%cd%":/workspace` - Zamontuj bieżący folder (Windows CMD syntax)
- `-w /workspace/scripts` - Ustaw katalog roboczy wewnątrz kontenera
- `alpine:latest` - Lekki obraz Linux (5MB)
- `apk add openssl bash` - Zainstaluj OpenSSL i Bash
- `chmod +x *.sh` - Nadaj uprawnienia wykonania skryptom
- `./generate-*.sh` - Uruchom wszystkie skrypty

### Metoda 3: Jeden skrypt do wszystkich (Wygodne)

Możesz utworzyć pomocniczy skrypt `generate-all.sh`:

    #!/bin/bash
    echo "Generowanie wszystkich certyfikatów testowych..."
    ./generate-valid-cert.sh
    ./generate-expiring-cert.sh
    ./generate-expired-cert.sh
    echo ""
    echo "✅ Wszystkie certyfikaty wygenerowane!"

---

## 📊 Wynik Działania

Po uruchomieniu skryptów powstanie struktura:

    docker/nginx/certs/
    ├── valid/
    │   ├── cert.pem       # Certyfikat publiczny (90 dni)
    │   └── key.pem        # Klucz prywatny
    ├── expiring/
    │   ├── cert.pem       # Certyfikat publiczny (7 dni)
    │   └── key.pem        # Klucz prywatny
    └── expired/
        ├── cert.pem       # Certyfikat publiczny (wygasły)
        └── key.pem        # Klucz prywatny

---

## 🔍 Weryfikacja Certyfikatów

### Sprawdź daty ważności:

    openssl x509 -in ../nginx/certs/valid/cert.pem -noout -dates
    openssl x509 -in ../nginx/certs/expiring/cert.pem -noout -dates
    openssl x509 -in ../nginx/certs/expired/cert.pem -noout -dates

### Sprawdź szczegóły certyfikatu:

    openssl x509 -in ../nginx/certs/valid/cert.pem -noout -text

### Oblicz ile dni do wygaśnięcia:

    # Linux/macOS
    echo $(( ($(date -d "$(openssl x509 -in ../nginx/certs/valid/cert.pem -noout -enddate | cut -d= -f2)" +%s) - $(date +%s)) / 86400 ))

---

## ⚠️ Ważne Uwagi

### Bezpieczeństwo Kluczy Prywatnych

- Pliki `key.pem` zawierają **klucze prywatne** - w produkcji MUSZĄ być chronione!
- Uprawnienia pliku: `chmod 600 key.pem` (tylko właściciel może czytać)
- **NIGDY** nie commituj kluczy prywatnych do repozytorium Git!
- W `.gitignore` dodaj: `*.pem`

### Certyfikaty Self-Signed

- Wszystkie generowane certyfikaty są **self-signed** (samopodpisane)
- Przeglądarki będą wyświetlać ostrzeżenie (to normalne!)
- W produkcji używaj certyfikatów od zaufanych CA (Let's Encrypt, DigiCert)

### Problem z Wygasłymi Certyfikatami

- OpenSSL nie pozwala łatwo wygenerować certyfikatu z przeszłą datą
- Skrypt `generate-expired-cert.sh` tworzy certyfikat na 1 dzień
- Możesz poczekać 24h lub użyć narzędzia `faketime` (Linux)

---

## 🔄 Odnawianie Certyfikatów (Symulacja)

W rzeczywistym środowisku administrator odnawia certyfikaty przed wygaśnięciem.

**Symulacja odnowienia:**

    # Usuń stary certyfikat
    rm -rf ../nginx/certs/expiring/*
    
    # Wygeneruj nowy
    ./generate-expiring-cert.sh
    
    # Restart Nginx
    cd ..
    docker-compose restart

---

## 📚 Dodatkowe Zasoby

- [OpenSSL Command Cheatsheet](https://www.sslshopper.com/article-most-common-openssl-commands.html)
- [Let's Encrypt - Darmowe Certyfikaty CA](https://letsencrypt.org/)
- [SSL Labs - Test Konfiguracji SSL](https://www.ssllabs.com/ssltest/)

---

**Autor:** Sebastian Ciborowski  
**Projekt:** Certificate-Expiry-Monitor
