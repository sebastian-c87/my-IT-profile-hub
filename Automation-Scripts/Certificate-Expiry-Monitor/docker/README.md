# 🐳 Docker Test Environment - Certificate Expiry Monitor

## 📋 Cel Środowiska Testowego

Ten folder zawiera **kompletne środowisko Docker** do testowania skryptu `Certificate-Expiry-Monitor` bez potrzeby dostępu do rzeczywistych serwerów produkcyjnych.

Środowisko symuluje serwer Nginx z **wieloma wirtualnymi hostami**, z których każdy posiada certyfikat SSL/TLS w różnym stanie:

- ✅ **Certyfikat ważny** (90 dni do wygaśnięcia)
- ⚠️ **Certyfikat wygasający wkrótce** (7 dni do wygaśnięcia)
- ❌ **Certyfikat już wygasły** (wygasł wczoraj)

---

## 🏗️ Struktura Folderów

    docker/
    ├── README.md                       # ← Ten plik (instrukcja)
    ├── docker-compose.yml              # Definicja kontenera Nginx
    ├── nginx/                          # Konfiguracja serwera Nginx
    │   ├── Dockerfile                  # Obraz Docker dla Nginx
    │   └── nginx.conf                  # Konfiguracja wirtualnych hostów
    └── scripts/                        # Skrypty generujące certyfikaty
        ├── generate-valid-cert.sh      # Tworzy certyfikat ważny przez 90 dni
        ├── generate-expiring-cert.sh   # Tworzy certyfikat wygasający za 7 dni
        ├── generate-expired-cert.sh    # Tworzy certyfikat już wygasły
        └── README.md                   # Instrukcja użycia skryptów

---

## 🚀 Jak Uruchomić Środowisko Testowe?

### Krok 1: Generowanie Certyfikatów Testowych

**UWAGA:** Przed uruchomieniem Dockera musisz wygenerować certyfikaty testowe.

    cd docker/scripts
    chmod +x *.sh

    # Wygeneruj wszystkie 3 typy certyfikatów
    ./generate-valid-cert.sh
    ./generate-expiring-cert.sh
    ./generate-expired-cert.sh

**Co się dzieje?**

- Skrypty używają `openssl` do wygenerowania **samopodpisanych certyfikatów** (self-signed)
- Każdy certyfikat ma **inną datę ważności** (90 dni / 7 dni / już wygasły)
- Certyfikaty są zapisywane w folderze `docker/nginx/certs/` (folder powstanie automatycznie)

**Wynik:**

    docker/nginx/certs/
    ├── valid/
    │   ├── cert.pem
    │   └── key.pem
    ├── expiring/
    │   ├── cert.pem
    │   └── key.pem
    └── expired/
        ├── cert.pem
        └── key.pem

---

### Krok 2: Uruchomienie Kontenera Nginx

    cd docker
    docker-compose up -d

**Co się dzieje?**

- Docker buduje obraz Nginx z konfiguracją z pliku `nginx/nginx.conf`
- Uruchamia kontener w tle (`-d` = detached mode)
- Nginx nasłuchuje na **3 portach**:
    - `8443` → Certyfikat ważny (90 dni)
    - `8444` → Certyfikat wygasający (7 dni)
    - `8445` → Certyfikat wygasły

**Sprawdź status:**

    docker-compose ps

Powinieneś zobaczyć:

    NAME                COMMAND                  SERVICE   STATUS    PORTS
    cert-test-nginx     "nginx -g 'daemon of…"   nginx     Up        0.0.0.0:8443->8443/tcp, ...

---

### Krok 3: Testowanie Skryptu Monitorowania

Teraz możesz uruchomić skrypt `Certificate-Expiry-Monitor` i skierować go na testowe serwery.

#### A. Przygotuj plik `config/domains.yml`

Upewnij się, że plik zawiera testowe hosty:

    domains:
      - host: localhost
        port: 8443
        name: "Test: Valid Certificate (90 days)"
        
      - host: localhost
        port: 8444
        name: "Test: Expiring Soon (7 days)"
        
      - host: localhost
        port: 8445
        name: "Test: Already Expired"

#### B. Uruchom Skrypt Główny

    cd ..  # Wróć do głównego folderu projektu
    python scripts/main.py

**Oczekiwany wynik:**

- ✅ Port 8443 → **OK** (certyfikat ważny przez 90 dni)
- ⚠️ Port 8444 → **WARNING** (certyfikat wygasa za 7 dni - wysłany alert)
- ❌ Port 8445 → **CRITICAL** (certyfikat wygasły - wysłany alert krytyczny)

Sprawdź folder `output/logs/` i `output/reports/` aby zobaczyć wygenerowane logi i raporty.

---

## 🔄 Odświeżanie Certyfikatów (Symulacja Odnowienia)

Aby **symulować odnowienie certyfikatu** (np. po jego wygaśnięciu):

    cd docker/scripts

    # Wygeneruj nowy certyfikat dla "wygasającego" hosta
    ./generate-expiring-cert.sh

    # Restart Nginx, aby załadował nowy certyfikat
    cd ..
    docker-compose restart

**Scenariusz praktyczny:**

W rzeczywistym środowisku administrator otrzymuje alert "certyfikat wygasa za 7 dni". Następnie:

1. Odnawia certyfikat (np. przez Let's Encrypt lub CA firmowe)
2. Podmienia pliki `cert.pem` i `key.pem` na serwerze
3. Restartuje serwis (np. `systemctl restart nginx`)

W tym środowisku testowym **symulujemy ten proces**, ponownie generując certyfikat i restartując kontener.

---

## 🧪 Zaawansowane Testy

### Test 1: Certyfikat z Nieprawidłowym Łańcuchem

Aby przetestować walidację łańcucha certyfikatów (funkcja w `cert_validator.py`):

    openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout docker/nginx/certs/invalid/key.pem \
      -out docker/nginx/certs/invalid/cert.pem \
      -days 365 -subj "/CN=invalid.local"

Dodaj do `nginx.conf` nowy serwer wirtualny na porcie `8446` z tym certyfikatem.

### Test 2: Monitorowanie w Pętli (Cron Simulation)

Aby zasymulować codzienne sprawdzanie (jak w cron):

    watch -n 10 python scripts/main.py

---

## 🛑 Zatrzymanie i Czyszczenie

### Zatrzymanie Kontenera

    docker-compose down

### Pełne Wyczyszczenie (w tym certyfikaty)

    docker-compose down
    rm -rf nginx/certs/

---

## 🎓 Dlaczego To Jest Ważne dla Administratora?

1. **Bezpieczne Testowanie:** Nie ryzykujesz błędami w produkcji
2. **Zrozumienie Problemu:** Widzisz dokładnie, jak wygląda wygasający certyfikat
3. **Trening Reakcji:** Ćwiczysz procedurę odnowienia przed rzeczywistym alertem
4. **Dokumentacja:** Możesz pokazać zespołowi/przełożonemu, jak działa monitoring

---

## ❓ Troubleshooting

### Problem: `docker-compose: command not found`

**Rozwiązanie:**

    # Instalacja Docker Compose (Linux)
    sudo apt install docker-compose

    # Lub użyj Docker Compose V2
    docker compose up -d

### Problem: Porty 8443-8445 są zajęte

**Rozwiązanie:** Sprawdź, co używa portów:

    sudo lsof -i :8443

Zmień porty w `docker-compose.yml` (np. na 9443, 9444, 9445).

### Problem: Skrypt nie wykrywa wygasłych certyfikatów

**Diagnoza:**

    openssl s_client -connect localhost:8445 -showcerts 2>/dev/null | openssl x509 -noout -dates

Jeśli data wygaśnięcia jest w przyszłości, przegenruj certyfikat:

    cd scripts
    ./generate-expired-cert.sh

---

## 📚 Dokumentacja Zewnętrzna

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx SSL/TLS Configuration](https://nginx.org/en/docs/http/configuring_https_servers.html)
- [OpenSSL Certificate Management](https://www.openssl.org/docs/man1.1.1/man1/openssl-x509.html)

---

**Autor:** Sebastian Ciborowski  
**Projekt:** [my-IT-profile-hub/Automation-Scripts](https://github.com/sebastian-c87/my-IT-profile-hub)  
**Licencja:** MIT
