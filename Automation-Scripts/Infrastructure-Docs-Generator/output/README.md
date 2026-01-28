# 📁 Folder Output - Wygenerowane Pliki

Ten folder zawiera **wszystkie pliki wygenerowane automatycznie** przez Infrastructure Documentation Generator.

⚠️ **WAŻNE:** Ten folder NIE jest commitowany do Git (jest w .gitignore) ze względów bezpieczeństwa.

---

## 📂 Struktura Folderu Output

Po uruchomieniu skryptu (`python scripts/main.py`), folder output/ będzie zawierał:

    output/
    ├── network-docs/              # Dokumentacja Markdown (główny rezultat)
    │   ├── README.md              # Przegląd całej sieci
    │   ├── Switch-L3-Core.md      # Dokumentacja Switch Layer 3
    │   ├── Router-WAN-Edge.md     # Dokumentacja Router WAN
    │   └── ASA-Firewall-Primary.md # Dokumentacja Firewall
    │
    ├── raw-configs/               # Backup konfiguracji (raw)
    │   ├── Switch-L3-Core_2026-01-28_02-00-15.txt
    │   ├── Router-WAN-Edge_2026-01-28_02-00-23.txt
    │   └── ASA-Firewall-Primary_2026-01-28_02-00-31.txt
    │
    ├── logs/                      # Logi skryptu
    │   ├── collector.log          # Logi zbierania konfiguracji
    │   └── generator.log          # Logi generowania dokumentacji
    │
    └── temp/                      # Pliki tymczasowe (czyszczone automatycznie)

---

## 📝 Zawartość Poszczególnych Folderów

### 1. network-docs/

**Przeznaczenie:** Główna wygenerowana dokumentacja w formacie Markdown

**Zawiera:**
- `README.md` - Przegląd wszystkich urządzeń z linkami
- Osobny plik `.md` dla każdego urządzenia z sieci
- Dokumentacja generowana przez AI (GPT-5-nano)

**Format plików:** `{hostname}.md`

**Przykładowa zawartość:** Zobacz sekcję [Przykładowa Dokumentacja](#przykładowa-dokumentacja) poniżej

---

### 2. raw-configs/

**Przeznaczenie:** Backup oryginalnych konfiguracji pobranych z urządzeń

**Zawiera:**
- Raw output z `show running-config` (Cisco)
- Raw output z `show configuration` (Juniper)
- Timestamp w nazwie pliku

**Format plików:** `{hostname}_{YYYY-MM-DD}_{HH-MM-SS}.txt`

**Retencja:** Pliki starsze niż 90 dni są automatycznie usuwane (konfigurowane w settings.yml)

**Przykładowa zawartość:**

    # Konfiguracja urządzenia: Switch-L3-Core
    # IP: 10.10.10.1
    # Data pobrania: 2026-01-28 02:00:15
    # Device Type: cisco_ios
    # ======================================================================
    
    Building configuration...
    
    Current configuration : 4521 bytes
    !
    version 15.2
    service timestamps debug datetime msec
    service timestamps log datetime msec
    no service password-encryption
    !
    hostname Switch-L3-Core
    !
    (... pełna konfiguracja Cisco IOS ...)

---

### 3. logs/

**Przeznaczenie:** Logi diagnostyczne z uruchomienia skryptów

**Zawiera:**
- `collector.log` - Logi z collect_configs.py
- `generator.log` - Logi z generate_docs.py

**Format logów:**

    [2026-01-28 02:00:12] [INFO] Rozpoczynam zbieranie konfiguracji z 4 urządzeń...
    [2026-01-28 02:00:15] [INFO] Łączenie z Switch-L3-Core (10.10.10.1)...
    [2026-01-28 02:00:18] [INFO] Pobieranie konfiguracji z Switch-L3-Core...
    [2026-01-28 02:00:22] [INFO] ✓ Sukces: Switch-L3-Core - zapisano do Switch-L3-Core_2026-01-28_02-00-15.txt
    [2026-01-28 02:00:23] [INFO] Łączenie z Router-WAN-Edge (10.50.10.2)...
    [2026-01-28 02:00:45] [ERROR] ✗ Timeout: Router-WAN-Edge - urządzenie niedostępne lub firewall blokuje

**Użycie:** Sprawdź logi gdy coś nie działa poprawnie

---

### 4. temp/

**Przeznaczenie:** Pliki tymczasowe podczas przetwarzania

**Zawiera:**
- Częściowo przetworzone dane
- Cache (jeśli włączony)

**Czyszczenie:** Automatyczne po każdym uruchomieniu (konfigurowane w settings.yml)

---

## 📄 Przykładowa Dokumentacja

Poniżej znajdziesz **przykład wygenerowanej dokumentacji** dla urządzenia Switch Layer 3.

### Przykład: Switch-L3-Core.md

    # Dokumentacja: Switch-L3-Core
    
    **Data wygenerowania:** 2026-01-28 02:05:34
    
    ---
    
    ## Informacje Ogólne
    
    | Parametr | Wartość |
    |----------|---------|
    | Hostname | Switch-L3-Core |
    | Model | Cisco Catalyst 3560-24PS |
    | Wersja IOS | 15.2(4)E8 |
    | Serial Number | FDO1234X5YZ |
    | Uptime | 127 days, 14 hours, 23 minutes |
    | IP Management | 10.10.10.1 |
    
    ### Opis Urządzenia
    
    Switch L3 pełniący rolę core'a sieci. Odpowiedzialny za routing między VLANami oraz zarządzanie ruchem w sieci lokalnej. Urządzenie jest skonfigurowane z redundancją HSRP dla wysokiej dostępności.
    
    ---
    
    ## Interfejsy Sieciowe
    
    ### Interfejsy Fizyczne
    
    | Interfejs | Status | IP Address | Opis | Speed |
    |-----------|--------|------------|------|-------|
    | GigabitEthernet0/1 | up | - | Trunk do Core Switch 2 | 1000 Mbps |
    | GigabitEthernet0/2 | up | - | Trunk do Floor1 Switch | 1000 Mbps |
    | GigabitEthernet0/3 | up | - | Trunk do Floor2 Switch | 1000 Mbps |
    | GigabitEthernet0/24 | up | - | Uplink do Router WAN | 1000 Mbps |
    
    ### Interfejsy VLAN (SVI)
    
    | VLAN | IP Address | Subnet | Opis |
    |------|------------|--------|------|
    | VLAN 10 | 10.10.10.1 | 255.255.255.0 | Sprzedaz - Gateway |
    | VLAN 20 | 10.10.20.1 | 255.255.255.0 | Finanse - Gateway |
    | VLAN 30 | 10.10.30.1 | 255.255.255.0 | IT - Gateway |
    | VLAN 100 | 10.10.100.1 | 255.255.255.0 | Goscie - Gateway |
    
    ---
    
    ## VLANy
    
    ### Skonfigurowane VLANy
    
    | VLAN ID | Nazwa | Status | Liczba Portów |
    |---------|-------|--------|---------------|
    | 10 | Sprzedaz | active | 48 |
    | 20 | Finanse | active | 24 |
    | 30 | IT | active | 12 |
    | 100 | Goscie | active | 16 |
    | 999 | Native | active | 0 |
    
    ### Trunk Ports
    
    | Port | Dozwolone VLANy | Native VLAN | Status |
    |------|-----------------|-------------|--------|
    | Gi0/1 | 10,20,30,100 | 999 | trunking |
    | Gi0/2 | 10,20,30,100 | 999 | trunking |
    | Gi0/3 | 10,20,30,100 | 999 | trunking |
    | Gi0/24 | all | 1 | trunking |
    
    ---
    
    ## Routing
    
    ### Protokoły Routingu
    
    #### OSPF
    
    - **Process ID:** 1
    - **Router ID:** 10.10.10.1
    - **Area:** 0 (Backbone)
    - **Advertised Networks:**
    
    | Network | Area | Wildcard Mask |
    |---------|------|---------------|
    | 10.10.10.0 | 0 | 0.0.0.255 |
    | 10.10.20.0 | 0 | 0.0.0.255 |
    | 10.10.30.0 | 0 | 0.0.0.255 |
    | 10.10.100.0 | 0 | 0.0.0.255 |
    
    ### Static Routes
    
    | Destination | Next Hop | Interface | Administrative Distance |
    |-------------|----------|-----------|------------------------|
    | 0.0.0.0/0 | 10.50.10.2 | - | 1 |
    
    **Opis:** Default route kieruje cały ruch do internetu przez Router WAN (10.50.10.2).
    
    ---
    
    ## Access Listy (ACL)
    
    ### Standard ACLs
    
    #### ACL 10 - SSH_ACCESS
    
    | Seq | Action | Source | Wildcard |
    |-----|--------|--------|----------|
    | 10 | permit | 10.10.30.0 | 0.0.0.255 |
    | 20 | deny | any | - |
    
    **Zastosowanie:** Ogranicza dostęp SSH tylko do sieci IT (VLAN 30).
    
    ### Extended ACLs
    
    #### ACL 100 - GUEST_INTERNET_ONLY
    
    | Seq | Action | Protocol | Source | Destination | Ports |
    |-----|--------|----------|--------|-------------|-------|
    | 10 | permit | tcp | 10.10.100.0/24 | any | 80,443 |
    | 20 | permit | udp | 10.10.100.0/24 | any | 53 |
    | 30 | deny | ip | 10.10.100.0/24 | 10.0.0.0/8 | - |
    | 40 | permit | ip | 10.10.100.0/24 | any | - |
    
    **Zastosowanie:** VLAN Goscie (100) może tylko do internetu, blokuje dostęp do sieci wewnętrznej.
    
    ---
    
    ## Bezpieczeństwo
    
    ### Konfiguracja SSH
    
    - **Wersja SSH:** 2.0
    - **Timeout:** 60 sekund
    - **Max Sessions:** 5
    - **Dozwolone źródła:** ACL 10 (tylko VLAN IT)
    
    ### Password Policy
    
    - **Enable Secret:** Skonfigurowany (SHA-256)
    - **Line VTY Password:** Skonfigurowany
    - **Service Password Encryption:** Włączony
    
    ### Port Security
    
    | Port | Max MAC | Violation Action | Status |
    |------|---------|------------------|--------|
    | Fa0/1-24 | 2 | shutdown | enabled |
    
    **Opis:** Porty access (FastEthernet) mają włączony port security z limitem 2 adresy MAC.
    
    ---
    
    ## Dodatkowe Funkcje
    
    ### HSRP (Hot Standby Router Protocol)
    
    | VLAN | Group | Priority | Virtual IP | Preempt | Status |
    |------|-------|----------|------------|---------|--------|
    | 10 | 10 | 110 | 10.10.10.1 | Yes | Active |
    | 20 | 20 | 110 | 10.10.20.1 | Yes | Active |
    | 30 | 30 | 110 | 10.10.30.1 | Yes | Active |
    
    **Opis:** Switch jest aktywnym routerem HSRP dla wszystkich VLANów (priority 110). Backup switch ma priority 100.
    
    ### STP (Spanning Tree Protocol)
    
    - **Mode:** PVST+ (Per-VLAN Spanning Tree)
    - **Root Bridge:** Tak (dla wszystkich VLANów)
    - **Priority:** 4096
    - **PortFast:** Włączony na portach access
    - **BPDU Guard:** Włączony
    
    ### NTP (Network Time Protocol)
    
    - **Serwery NTP:** 
      - 10.50.10.2 (Router WAN - primary)
      - 193.5.216.14 (ntp.certum.pl - secondary)
    - **Timezone:** CET (UTC+1)
    - **Status:** Synchronized
    
    ---
    
    ## Zalecenia i Uwagi
    
    ### Zalecenia Bezpieczeństwa
    
    ✓ **Dobrze skonfigurowane:**
    - SSH v2 (bezpieczna wersja)
    - ACL ogranicza dostęp SSH
    - Port Security włączony
    - BPDU Guard zabezpiecza przed rogue switches
    
    ⚠ **Do poprawy:**
    - Brak AAA (RADIUS/TACACS+) - rozważ centralne zarządzanie użytkownikami
    - Native VLAN nie jest zmieniony na trunk portach (może być wykorzystany do VLAN hopping)
    - Brak DHCP Snooping - rozważ włączenie dla ochrony przed rogue DHCP servers
    
    ### Historia Zmian
    
    | Data | Zmiana | Autor |
    |------|--------|-------|
    | 2026-01-28 | Dokumentacja wygenerowana automatycznie | Infrastructure Docs Generator |
    | 2025-12-15 | Dodano VLAN 100 (Goscie) | Administrator IT |
    | 2025-11-20 | Upgrade IOS do 15.2(4)E8 | Administrator IT |
    
    ---
    
    **Wygenerowano automatycznie:** 2026-01-28 02:05:34  
    **Generator:** Infrastructure Documentation Generator v1.0  
    **GitHub:** https://github.com/sebastian-c87/my-it-profile-hub

---

## 📊 Przykład README.md (Przegląd Sieci)

W folderze `network-docs/` znajduje się również plik `README.md` który zawiera przegląd **wszystkich** urządzeń:

    # 🌐 Dokumentacja Infrastruktury Sieciowej
    
    **Data wygenerowania:** 2026-01-28 02:10:45  
    **Liczba urządzeń:** 4  
    **Status:** ✓ Wszystkie urządzenia online
    
    ---
    
    ## 📊 Podsumowanie
    
    | Kategoria | Liczba |
    |-----------|--------|
    | Routery | 1 |
    | Switche Layer 3 | 1 |
    | Switche Layer 2 | 0 |
    | Firewalle | 1 |
    | **RAZEM** | **4** |
    
    ---
    
    ## 📁 Lista Urządzeń
    
    | Hostname | IP | Typ | Status | Dokumentacja |
    |----------|----|----|--------|--------------|
    | Switch-L3-Core | 10.10.10.1 | Cisco L3 | ✓ OK | [Switch-L3-Core.md](./Switch-L3-Core.md) |
    | Router-WAN-Edge | 10.50.10.2 | Cisco Router | ✓ OK | [Router-WAN-Edge.md](./Router-WAN-Edge.md) |
    | ASA-Firewall-Primary | 10.30.40.2 | Cisco ASA | ✓ OK | [ASA-Firewall-Primary.md](./ASA-Firewall-Primary.md) |
    
    ---
    
    **Ostatnia aktualizacja:** 2026-01-28 02:10:45

---

## 🔍 Jak Przeglądać Dokumentację

### Opcja 1: GitHub (jeśli commitowane)

Jeśli zdecydujesz się commitować folder `network-docs/` do **prywatnego** repozytorium:

1. Otwórz repo na GitHubie
2. Przejdź do folderu `Automation-Scripts/Infrastructure-Docs-Generator/output/network-docs/`
3. GitHub automatycznie wyrenderuje pliki Markdown

### Opcja 2: Visual Studio Code

1. Otwórz folder projektu w VSC
2. Przejdź do `output/network-docs/`
3. Kliknij prawym na plik `.md` → **Open Preview**

### Opcja 3: Markdown Viewer (przeglądarka)

Zainstaluj rozszerzenie do przeglądarki:
- **Chrome/Edge:** Markdown Viewer
- **Firefox:** Markdown Viewer Webext

Następnie otwórz plik `.md` bezpośrednio w przeglądarce.

### Opcja 4: Konwersja do HTML/PDF

Użyj narzędzi takich jak:
- `pandoc` - konwersja Markdown → HTML/PDF
- `grip` - serwer HTTP dla Markdown (wygląd jak GitHub)

Przykład z pandoc:

    pandoc Switch-L3-Core.md -o Switch-L3-Core.pdf

---

## 🔒 Bezpieczeństwo

### Co znajduje się w tym folderze?

⚠️ **WRAŻLIWE DANE:**
- Raw konfiguracje urządzeń (adresy IP, hostnamy, topologia)
- Informacje o ACL i bezpieczeństwie
- Potencjalnie hasła (jeśli nie są zaszyfrowane w config)

### Zalecenia:

✅ **Zawsze:**
- Folder `output/` jest w `.gitignore` (NIE commituj do publicznego repo)
- Przechowuj dokumentację lokalnie lub w prywatnym repo
- Regularnie rób backup folderu `output/`

❌ **Nigdy:**
- Nie udostępniaj publicznie
- Nie wysyłaj emailem bez szyfrowania
- Nie wrzucaj na publiczne dyski (Google Drive, Dropbox bez szyfrowania)

---

## 📞 FAQ

**Q: Czy mogę edytować wygenerowane pliki .md?**  
A: Tak, ale zmiany zostaną nadpisane przy kolejnym uruchomieniu skryptu. Jeśli chcesz dodać własne notatki, utwórz osobne pliki (np. `Switch-L3-Core_NOTES.md`).

**Q: Jak często aktualizować dokumentację?**  
A: Zalecane: codziennie (przez Task Scheduler/Cron). Dokumentacja będzie zawsze aktualna.

**Q: Co zrobić jeśli urządzenie ma błąd?**  
A: Sprawdź logi w `output/logs/collector.log`. Najczęstsze przyczyny: błędne hasło, timeout SSH, urządzenie offline.

**Q: Czy mogę zmienić format plików (np. HTML zamiast Markdown)?**  
A: Tak, zmodyfikuj `scripts/generate_docs.py` lub użyj narzędzia `pandoc` do konwersji.

---

**Data stworzenia:** 2026-01-28  
**Wersja:** 1.0  
**Projekt:** Infrastructure Documentation Generator
