# 🔒 SSL/TLS Certificate Guide - Kompletne Szkolenie

Profesjonalny przewodnik po certyfikatach SSL/TLS - od podstaw do zaawansowanych zastosowań.

---

## 📋 Spis Treści

### Część I: Podstawy
- [Czym są certyfikaty SSL/TLS?](#czym-są-certyfikaty-ssltls)
- [Jak działa szyfrowanie SSL/TLS?](#jak-działa-szyfrowanie-ssltls)
- [Historia i ewolucja protokołów](#historia-i-ewolucja-protokołów)
- [Dlaczego certyfikaty są ważne?](#dlaczego-certyfikaty-są-ważne)

### Część II: Architektura i Komponenty
- [Anatomia certyfikatu X.509](#anatomia-certyfikatu-x509)
- [Łańcuch zaufania (Chain of Trust)](#łańcuch-zaufania-chain-of-trust)
- [Public Key Infrastructure (PKI)](#public-key-infrastructure-pki)
- [Rodzaje certyfikatów](#rodzaje-certyfikatów)

### Część III: Praktyka
- [Jak uzyskać certyfikat SSL/TLS?](#jak-uzyskać-certyfikat-ssltls)
- [Instalacja certyfikatu na serwerze](#instalacja-certyfikatu-na-serwerze)
- [Konfiguracja Apache, Nginx, IIS](#konfiguracja-serwerów-web)
- [Odnowienie certyfikatów](#odnowienie-certyfikatów)

### Część IV: Bezpieczeństwo
- [Typowe zagrożenia i ataki](#typowe-zagrożenia-i-ataki)
- [Best practices bezpieczeństwa](#best-practices-bezpieczeństwa)
- [Compliance i standardy](#compliance-i-standardy)

### Część V: Troubleshooting
- [Diagnostyka problemów](#diagnostyka-problemów)
- [Narzędzia do debugowania](#narzędzia-do-debugowania)
- [Najczęstsze błędy](#najczęstsze-błędy)

---

# Część I: Podstawy

## Czym są Certyfikaty SSL/TLS?

### Definicja

**SSL/TLS certyfikat** to cyfrowy dokument, który:
- ✅ **Potwierdza tożsamość** serwera (np. google.com jest rzeczywiście Google)
- ✅ **Szyfruje komunikację** między klientem (przeglądarka) a serwerem
- ✅ **Zapewnia integralność danych** (dane nie zostały zmienione w transicie)

### Analogia ze Świata Rzeczywistego

Wyobraź sobie certyfikat SSL/TLS jako **paszport** lub **dowód osobisty** w internecie:

**Paszport (świat rzeczywisty):**
- Zdjęcie + dane osobowe
- Podpis urzędu (np. MSZ)
- Hologram zabezpieczający
- Data ważności

**Certyfikat SSL (świat cyfrowy):**
- Nazwa domeny (np. google.com)
- Podpis CA (Certificate Authority)
- Klucz publiczny
- Data wygaśnięcia

### Skróty: SSL vs TLS

| Skrót | Pełna Nazwa | Status |
|-------|-------------|--------|
| **SSL** | Secure Sockets Layer | ❌ **Przestarzały** (ostatnia wersja: SSL 3.0 z 1996) |
| **TLS** | Transport Layer Security | ✅ **Aktualny** (TLS 1.2 i 1.3) |

**UWAGA:** Dzisiaj mówimy "SSL", ale faktycznie używamy **TLS**. To jak mówienie "Kleenex" na chusteczki - nazwa się przyjęła, choć technicznie nieprecyzyjna.

---

## Jak Działa Szyfrowanie SSL/TLS?

### Proces Nawiązania Połączenia (TLS Handshake)

Gdy wpisujesz `https://google.com` w przeglądarce, dzieje się to:

#### Krok 1: Client Hello (Klient → Serwer)

Przeglądarka mówi:

    Cześć google.com!
    - Obsługuję TLS 1.2 i 1.3
    - Preferuję szyfrowanie: AES-256-GCM, ChaCha20-Poly1305
    - Oto mój losowy numer (Client Random): abc123...

#### Krok 2: Server Hello (Serwer → Klient)

Serwer odpowiada:

    Cześć przeglądarko!
    - Używamy TLS 1.3
    - Wybrałem szyfrowanie: AES-256-GCM
    - Mój losowy numer (Server Random): xyz789...
    - Mój certyfikat SSL (z kluczem publicznym):
      [CERTYFIKAT X.509]

#### Krok 3: Weryfikacja Certyfikatu (Klient)

Przeglądarka sprawdza:

    1. Czy certyfikat jest podpisany przez zaufane CA? ✅
    2. Czy nazwa domeny się zgadza (google.com)? ✅
    3. Czy certyfikat nie wygasł? ✅
    4. Czy certyfikat nie został odwołany (CRL/OCSP)? ✅

Jeśli wszystko OK → **kłódka zielona** 🔒

#### Krok 4: Pre-Master Secret

Przeglądarka:

    Generuję losowy klucz (Pre-Master Secret): qwerty456...
    Szyfruję go kluczem PUBLICZNYM z certyfikatu serwera
    Wysyłam do serwera: [ZASZYFROWANY KLUCZ]

**Serwer** deszyfruje kluczem **PRYWATNYM** (tylko on go ma!).

#### Krok 5: Session Keys

Zarówno klient jak i serwer obliczają **Session Keys**:

    Session Key = funkcja(
        Client Random,
        Server Random,
        Pre-Master Secret
    )

Teraz **obie strony** mają ten sam **symetryczny klucz** do szyfrowania!

#### Krok 6: Szyfrowana Komunikacja

Wszystkie dalsze dane są szyfrowane **Session Key** (szybkie, symetryczne).

**Przykład:**

    Przeglądarka → Serwer (zaszyfrowane):
    GET /search?q=ssl+certificates HTTP/1.1
    
    Serwer → Przeglądarka (zaszyfrowane):
    HTTP/1.1 200 OK
    <html>...</html>

---

### Szyfrowanie: Asymetryczne vs Symetryczne

#### Szyfrowanie Asymetryczne (Powolne, Bezpieczne)

**Używane w:** TLS Handshake (tylko na początku)

**Jak działa:**
- **2 klucze:** Publiczny (wszyscy znają) + Prywatny (tylko serwer)
- **Zaszyfrowane kluczem PUBLICZNYM** → tylko klucz PRYWATNY może odszyfrować
- **Analogia:** Skrzynka pocztowa z szczeliną (każdy może wrzucić list), ale tylko listonosz ma klucz

**Przykład (RSA 2048-bit):**

    Klucz Publiczny (w certyfikacie):
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
    -----END PUBLIC KEY-----
    
    Klucz Prywatny (na serwerze, TAJNY!):
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEA...
    -----END PRIVATE KEY-----

---

#### Szyfrowanie Symetryczne (Szybkie)

**Używane w:** Cała reszta komunikacji (po handshake)

**Jak działa:**
- **1 klucz** używany do szyfrowania i deszyfrowania
- **100x szybsze** niż asymetryczne
- **Analogia:** Sejf z kodem - ten sam kod otwiera i zamyka

**Przykład (AES-256):**

    Session Key (256 bitów):
    a1b2c3d4e5f6...7890abcdef1234567890abcdef12345

---

## Historia i Ewolucja Protokołów

### Timeline SSL/TLS

| Rok | Protokół | Status | Kluczowe Cechy |
|-----|----------|--------|----------------|
| **1995** | SSL 2.0 | ❌ Przestarzały | Pierwszy publicznie dostępny, wiele dziur bezpieczeństwa |
| **1996** | SSL 3.0 | ❌ Przestarzały | Poprawki SSL 2.0, ale nadal podatny (POODLE attack) |
| **1999** | TLS 1.0 | ⚠️ Przestarzały (2020) | Ewolucja SSL 3.0, RFC 2246 |
| **2006** | TLS 1.1 | ⚠️ Przestarzały (2020) | Ochrona przed CBC attacks |
| **2008** | TLS 1.2 | ✅ **Aktualny** | AES-GCM, SHA-256, używany do dziś |
| **2018** | TLS 1.3 | ✅ **Najnowszy** | Szybszy handshake, silniejsze szyfrowanie |

### Dlaczego TLS 1.3 jest Lepszy?

**TLS 1.2 Handshake:** 2 rundy (2-RTT)

    Klient → Serwer: Client Hello
    Klient ← Serwer: Server Hello, Certificate, Key Exchange
    Klient → Serwer: Key Exchange, Finished
    Klient ← Serwer: Finished
    [Dopiero teraz można wysyłać dane]

**TLS 1.3 Handshake:** 1 runda (1-RTT)

    Klient → Serwer: Client Hello + Key Share
    Klient ← Serwer: Server Hello + Key Share + Certificate + Finished
    [Od razu można wysyłać dane!]

**Rezultat:** TLS 1.3 jest **2x szybszy** przy nawiązywaniu połączenia!

---

## Dlaczego Certyfikaty Są Ważne?

### 1. Bezpieczeństwo (Security)

**Bez certyfikatu (HTTP):**

    Ty → Router WiFi → ISP → Serwer
         ↑ Ktoś podsłuchuje (plaintext!)
    
    Twoje hasło: "password123"
    Widoczne dla: kawiarni WiFi, ISP, atakujących

**Z certyfikatem (HTTPS):**

    Ty → Router WiFi → ISP → Serwer
         ↑ Ktoś podsłuchuje (ale widzi tylko śmieci!)
    
    Twoje hasło: "8x#j2@Pk9!mZ" (zaszyfrowane)
    Widoczne dla: NIKOGO (tylko ty i serwer)

---

### 2. Autentykacja (Kto to naprawdę?)

**Scenariusz:** Chcesz zalogować się do banku.

**Bez certyfikatu:**

    Wpisujesz: bank.com
    Ładuje się strona - ale czy to prawdziwy bank?
    ❌ Może to phishing (bank-com.evil.com)!

**Z certyfikatem:**

    Przeglądarka sprawdza:
    1. Domena: bank.com ✅
    2. Certyfikat podpisany przez DigiCert ✅
    3. Nazwa organizacji: "Bank Example SA" ✅
    
    Pewność: To PRAWDZIWY bank.com!

---

### 3. SEO i Zaufanie Użytkowników

**Google ranking (od 2014):**
- HTTPS = **boost w rankingu** 🚀
- HTTP = **penalty** (niższe pozycje)

**Przeglądarki (Chrome, Firefox):**
- HTTPS: 🔒 **Bezpieczne**
- HTTP: ⚠️ **"Niezabezpieczone"** (straszak dla użytkowników!)

**Statystyki:**
- 95% użytkowników **nie kliknie** strony z ostrzeżeniem SSL
- Strony HTTPS mają **średnio +20% konwersji**

---

### 4. Compliance (Wymogi Prawne)

**PCI-DSS** (płatności kartą):
- Wymóg: TLS 1.2+ dla wszystkich transakcji
- Brak SSL = **nie możesz przyjmować płatności**

**RODO (GDPR):**
- Art. 32: "Odpowiednie środki techniczne" = szyfrowanie
- Brak HTTPS przy przetwarzaniu danych osobowych = **kara do 20M EUR**

**HIPAA** (ochrona zdrowia, USA):
- Dane medyczne muszą być szyfrowane
- TLS wymagany dla API medycznych

---

# Część II: Architektura i Komponenty

## Anatomia Certyfikatu X.509

### Czym Jest X.509?

**X.509** to standard definiujący format certyfikatów cyfrowych (RFC 5280).

### Struktura Certyfikatu

Każdy certyfikat SSL/TLS zawiera:

#### 1. Version (Wersja)

    Version: 3 (0x2)

Prawie wszystkie certyfikaty dzisiaj to **v3** (wspiera rozszerzenia).

---

#### 2. Serial Number (Numer Seryjny)

    Serial Number:
        03:e7:00:00:00:01:68:d0:89:b7:4a

**Unikalny identyfikator** certyfikatu (jak PESEL). Używany przy:
- Odwoływaniu certyfikatu (CRL)
- Identyfikacji w logach

---

#### 3. Signature Algorithm (Algorytm Podpisu)

    Signature Algorithm: sha256WithRSAEncryption

**Jak CA podpisał certyfikat:**
- `sha256` = algorytm hashowania (SHA-256)
- `RSAEncryption` = algorytm kryptograficzny (RSA)

**Inne przykłady:**
- `ecdsa-with-SHA384` (ECDSA)
- `sha1WithRSAEncryption` (❌ przestarzały!)

---

#### 4. Issuer (Wystawca = CA)

    Issuer: C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA

**Kto podpisał certyfikat:**
- `C` = Country (Kraj)
- `O` = Organization (Organizacja)
- `CN` = Common Name (Nazwa CA)

---

#### 5. Validity (Okres Ważności)

    Validity
        Not Before: Jan  1 00:00:00 2026 GMT
        Not After : Apr  1 23:59:59 2026 GMT

**Daty ważności:**
- **Not Before:** Od kiedy certyfikat jest ważny
- **Not After:** Do kiedy certyfikat jest ważny

**UWAGA:** Maksymalny okres ważności (od 2020):
- **398 dni** dla certyfikatów publicznych
- Wcześniej było 2-3 lata!

---

#### 6. Subject (Podmiot = Właściciel)

    Subject: C=PL, ST=Mazovia, L=Warsaw, O=Example Corp, CN=www.example.com

**Dla kogo wystawiono certyfikat:**
- `C` = Country (Kraj)
- `ST` = State/Province (Województwo)
- `L` = Locality (Miasto)
- `O` = Organization (Firma)
- `CN` = Common Name (Domena) ← **NAJWAŻNIEJSZE!**

---

#### 7. Subject Public Key Info (Klucz Publiczny)

    Subject Public Key Info:
        Public Key Algorithm: rsaEncryption
            RSA Public-Key: (2048 bit)
            Modulus:
                00:c4:c3:85:d9:7f:...
            Exponent: 65537 (0x10001)

**Klucz publiczny właściciela:**
- **Algorytm:** RSA, ECDSA, Ed25519
- **Długość:** 2048-bit, 3072-bit, 4096-bit (RSA) lub 256-bit (ECDSA)
- **Modulus:** Część matematyczna klucza (dla RSA)

**Używany do:** Szyfrowania w TLS Handshake.

---

#### 8. Extensions (Rozszerzenia X.509v3)

**Najważniejsze rozszerzenia:**

##### A. Subject Alternative Name (SAN)

    X509v3 Subject Alternative Name:
        DNS:www.example.com
        DNS:example.com
        DNS:*.example.com
        DNS:api.example.com

**Lista wszystkich domen** objętych certyfikatem.

**Przykład:** Certyfikat google.com ma ~50 SANs:
- `google.com`
- `*.google.com`
- `youtube.com`
- `*.youtube.com`
- `gmail.com`
- itd.

---

##### B. Key Usage

    X509v3 Key Usage: critical
        Digital Signature, Key Encipherment

**Do czego można użyć klucza:**
- `Digital Signature` - Podpisywanie danych
- `Key Encipherment` - Szyfrowanie kluczy sesji
- `Certificate Sign` - Podpisywanie innych certyfikatów (tylko CA)

---

##### C. Extended Key Usage

    X509v3 Extended Key Usage:
        TLS Web Server Authentication, TLS Web Client Authentication

**Specyficzne zastosowania:**
- `TLS Web Server Authentication` - Serwer HTTPS
- `TLS Web Client Authentication` - Certyfikat klienta (mTLS)
- `Code Signing` - Podpisywanie oprogramowania
- `Email Protection` - S/MIME (szyfrowanie emaili)

---

##### D. Authority Information Access (AIA)

    Authority Information Access:
        OCSP - URI:http://ocsp.digicert.com
        CA Issuers - URI:http://cacerts.digicert.com/DigiCertSHA2SecureServerCA.crt

**Gdzie sprawdzić status certyfikatu:**
- **OCSP:** Online Certificate Status Protocol (czy certyfikat odwołano?)
- **CA Issuers:** Gdzie pobrać certyfikat pośredni CA

---

##### E. CRL Distribution Points

    X509v3 CRL Distribution Points:
        Full Name:
          URI:http://crl3.digicert.com/DigiCertSHA2SecureServerCA.crl

**Lista odwołanych certyfikatów** (Certificate Revocation List).

---

#### 9. Signature (Podpis Cyfrowy CA)

    Signature Algorithm: sha256WithRSAEncryption
         0f:3a:c7:b2:...
         (2048-bit RSA signature)

**Cyfrowy podpis CA** potwierdzający autentyczność certyfikatu.

**Jak weryfikować:**

    1. CA bierze cały certyfikat (bez podpisu)
    2. Oblicza hash (SHA-256)
    3. Szyfruje hash swoim kluczem PRYWATNYM = PODPIS
    
    Weryfikacja przez przeglądarkę:
    1. Oblicz hash certyfikatu
    2. Odszyfruj podpis kluczem PUBLICZNYM CA
    3. Porównaj hashe: identyczne? ✅ Certyfikat autentyczny!

---

## Łańcuch Zaufania (Chain of Trust)

### Hierarchia Certyfikatów

**Struktura piramidy zaufania:**

    ┌─────────────────────────────────────┐
    │  Root CA Certificate                │  ← Najwyższy poziom
    │  (DigiCert Global Root CA)          │     (w systemie operacyjnym)
    └─────────────────┬───────────────────┘
                      │ podpisuje
                      ↓
    ┌─────────────────────────────────────┐
    │  Intermediate CA Certificate        │  ← Pośredni poziom
    │  (DigiCert SHA2 Secure Server CA)   │
    └─────────────────┬───────────────────┘
                      │ podpisuje
                      ↓
    ┌─────────────────────────────────────┐
    │  End-Entity Certificate             │  ← Twój certyfikat
    │  (www.example.com)                  │
    └─────────────────────────────────────┘

---

### Jak Działa Weryfikacja?

**Krok po kroku:**

#### Krok 1: Przeglądarka otrzymuje certyfikat

    www.example.com przedstawia:
    - Certyfikat end-entity (www.example.com)
    - Certyfikat pośredni (DigiCert SHA2 Secure Server CA)

#### Krok 2: Weryfikacja podpisu

    1. Sprawdź podpis certyfikatu www.example.com
       Podpisany przez: DigiCert SHA2 Secure Server CA
       Weryfikacja kluczem publicznym z certyfikatu pośredniego: ✅
    
    2. Sprawdź podpis certyfikatu pośredniego
       Podpisany przez: DigiCert Global Root CA
       Weryfikacja kluczem publicznym z Root CA: ✅

#### Krok 3: Sprawdź Root CA

    Czy DigiCert Global Root CA jest w Trust Store?
    (Lista zaufanych CA wbudowana w system operacyjny)
    
    Windows: certmgr.msc → Trusted Root Certification Authorities
    Linux: /etc/ssl/certs/
    macOS: Keychain Access → System Roots
    
    Znaleziono? ✅ ZAUFANY ŁAŃCUCH!

---

### Trust Store (Magazyn Zaufanych CA)

**Gdzie przechowywane:**

| System | Lokalizacja |
|--------|-------------|
| **Windows** | Windows Certificate Store (`certmgr.msc`) |
| **Linux** | `/etc/ssl/certs/` + `/usr/local/share/ca-certificates/` |
| **macOS** | Keychain Access (System Roots) |
| **Firefox** | Własny store (niezależny od OS) |

**Ilu jest Root CA?**
- ~50-100 zaufanych Root CA globalnie
- Przykłady: DigiCert, Let's Encrypt, GlobalSign, Sectigo

---

## Public Key Infrastructure (PKI)

### Komponenty PKI

#### 1. Certificate Authority (CA)

**Rola:** Wystawca certyfikatów (jak urząd paszportowy).

**Typy CA:**

**Root CA:**
- **Najwyższy autorytet** w hierarchii
- Certyfikat **self-signed** (podpisany sam przez siebie)
- Klucz prywatny trzymany **OFFLINE** (cold storage, HSM)
- Używany **TYLKO** do podpisywania Intermediate CA

**Intermediate CA:**
- Podpisany przez Root CA
- Używany do **codziennego** wystawiania certyfikatów
- Jeśli skompromitowany → łatwo odwołać (bez wpływu na Root)

**Przykład hierarchii DigiCert:**

    DigiCert Global Root CA (Root)
     ├── DigiCert SHA2 Secure Server CA (Intermediate)
     │    ├── www.google.com
     │    ├── www.facebook.com
     │    └── ...
     └── DigiCert EV SHA256 CA (Intermediate)
          ├── www.bank.com (EV)
          └── ...

---

#### 2. Registration Authority (RA)

**Rola:** Weryfikacja tożsamości wnioskodawcy.

**Proces:**

    1. Firma Example Corp chce certyfikat dla example.com
    2. RA sprawdza:
       - Czy domena należy do firmy? (WHOIS, DNS)
       - Czy firma istnieje? (KRS, NIP)
       - Czy osoba reprezentuje firmę? (pełnomocnictwo)
    3. RA zatwierdza wniosek
    4. CA wystawia certyfikat

---

#### 3. Certificate Repository

**Rola:** Publiczne repozytorium certyfikatów i CRL.

**Zawiera:**
- Wystawione certyfikaty
- CRL (Certificate Revocation List)
- OCSP responder

**Przykład:** http://crl.digicert.com/

---

#### 4. Validation Authority (VA)

**Rola:** Sprawdzanie statusu certyfikatu (OCSP).

**Proces:**

    Przeglądarka → VA: Czy certyfikat nr 12345 jest ważny?
    VA → Przeglądarka: TAK (Good) / NIE (Revoked) / NIE WIEM (Unknown)

---

## Rodzaje Certyfikatów

### 1. Domain Validation (DV)

**Weryfikacja:** Tylko **własność domeny** (przez email lub DNS).

**Czas wystawienia:** **Minuty** (automatyczny).

**Koszt:** **Darmowy** (Let's Encrypt) do ~50 PLN/rok.

**Informacje w certyfikacie:**
- ✅ Domena (example.com)
- ❌ Nazwa firmy
- ❌ Adres

**Użycie:**
- Blogi osobiste
- Małe strony WWW
- API deweloperskie

**Przykład (Let's Encrypt):**

    Subject: CN=example.com
    Issuer: CN=Let's Encrypt Authority X3
    Validity: 90 days

**Przeglądarka pokazuje:** 🔒 (bez nazwy firmy)

---

### 2. Organization Validation (OV)

**Weryfikacja:** Własność domeny + **weryfikacja firmy** (KRS, NIP, telefon).

**Czas wystawienia:** **1-3 dni** (manual verification).

**Koszt:** ~200-500 PLN/rok.

**Informacje w certyfikacie:**
- ✅ Domena (example.com)
- ✅ Nazwa firmy (Example Corp)
- ✅ Miasto, Kraj

**Użycie:**
- Firmowe strony WWW
- Platformy e-commerce (średnie)
- Intranety korporacyjne

**Przykład:**

    Subject: C=PL, ST=Mazovia, L=Warsaw, O=Example Corp, CN=www.example.com
    Issuer: CN=DigiCert SHA2 Secure Server CA

**Przeglądarka pokazuje:** 🔒 Example Corp (kliknij kłódkę)

---

### 3. Extended Validation (EV)

**Weryfikacja:** Najwyższa - **pełny audyt firmy** (istnienie legalne, adres fizyczny, telefon, dokumenty).

**Czas wystawienia:** **7-14 dni**.

**Koszt:** ~1000-3000 PLN/rok.

**Informacje w certyfikacie:**
- ✅ Pełna nazwa prawna firmy
- ✅ Numer rejestracyjny (KRS)
- ✅ Adres siedziby
- ✅ Kraj, miasto

**Użycie:**
- **Banki**
- **E-commerce** (duże portale)
- **Płatności** (PayPal, Stripe dashboards)

**Przykład (PayPal):**

    Subject: 
      businessCategory=Private Organization
      serialNumber=3014267
      C=US, ST=California, L=San Jose
      O=PayPal, Inc.
      CN=www.paypal.com

**Przeglądarka pokazuje (stara wersja Chrome):**
🔒 **PayPal, Inc. [US]** (zielony pasek w adresie)

**UWAGA:** Od Chrome 77 (2019) zielony pasek EV został usunięty (kontrowersja!). Teraz tylko widać nazwę firmy po kliknięciu kłódki.

---

### 4. Wildcard Certificate

**Pokrywa:** Wszystkie **subdomeny pierwszego poziomu**.

**Format:** `*.example.com`

**Obejmuje:**
- ✅ `www.example.com`
- ✅ `api.example.com`
- ✅ `blog.example.com`
- ❌ `sub.api.example.com` (drugi poziom - NIE!)
- ❌ `example.com` (root - trzeba dodać jako SAN!)

**Koszt:** ~300-1000 PLN/rok (droższy niż single domain).

**Użycie:**
- Firmy z wieloma subdomenami
- SaaS (tenant1.app.com, tenant2.app.com)

**Przykład:**

    Subject: CN=*.example.com
    Subject Alternative Name:
        DNS:*.example.com
        DNS:example.com  ← często dodawany

---

### 5. Multi-Domain (SAN) Certificate

**Pokrywa:** Wiele **różnych domen** w jednym certyfikacie.

**Format:** Lista SANs (Subject Alternative Names).

**Przykład:**

    Subject: CN=example.com
    Subject Alternative Name:
        DNS:example.com
        DNS:www.example.com
        DNS:shop.example.com
        DNS:example.org
        DNS:example.net

**Koszt:** ~500 PLN/rok + ~50 PLN za każdy dodatkowy SAN.

**Użycie:**
- Konsolidacja certyfikatów (mniej zarządzania)
- Microsoft Exchange (wiele hostnames)

---

### 6. Code Signing Certificate

**Użycie:** Podpisywanie **oprogramowania** (exe, dll, msi, jar, apk).

**Weryfikacja:** OV lub EV (dla firmy/developera).

**Dlaczego potrzebne:**
- Windows SmartScreen: "Zweryfikowany wydawca" ✅
- macOS Gatekeeper: Aplikacja z podpisem Apple

**Przykład (Microsoft Authenticode):**

    Subject: CN=Example Software Inc, O=Example Software Inc, C=US
    Extended Key Usage: Code Signing

**Koszt:** ~800-2000 PLN/rok.

---

### 7. S/MIME Certificate

**Użycie:** Szyfrowanie i podpisywanie **emaili**.

**Funkcje:**
- ✅ Szyfruje treść emaila (tylko odbiorca może odczytać)
- ✅ Podpisuje email (potwierdzenie nadawcy)

**Przykład:**

    Subject: CN=john.doe@example.com, E=john.doe@example.com
    Extended Key Usage: Email Protection

**Koszt:** Darmowy (Actalis) do ~200 PLN/rok.

**Użycie:** Korporacje, wymiana poufnych dokumentów.

---

# Część III: Praktyka

## Jak Uzyskać Certyfikat SSL/TLS?

### Metoda 1: Let's Encrypt (Darmowy, Automatyczny)

**Let's Encrypt** = non-profit CA, darmowe certyfikaty DV.

#### Wymagania:
- Serwer Linux/Windows z dostępem SSH/RDP
- Port 80 lub 443 otwarty (dla walidacji)
- Domena wskazująca na serwer (DNS A record)

#### Instalacja Certbot (Linux - Ubuntu/Debian)

    # Zainstaluj Certbot
    sudo apt update
    sudo apt install certbot python3-certbot-nginx

#### Uzyskanie Certyfikatu (Nginx)

    # Automatyczna konfiguracja Nginx
    sudo certbot --nginx -d example.com -d www.example.com

**Proces:**

    1. Certbot wysyła żądanie do Let's Encrypt
    2. Let's Encrypt: "Udowodnij że kontrolujesz example.com"
    3. Certbot tworzy plik: http://example.com/.well-known/acme-challenge/xyz123
    4. Let's Encrypt pobiera plik → weryfikacja ✅
    5. Let's Encrypt wystawia certyfikat (90 dni)
    6. Certbot konfiguruje Nginx automatycznie

**Automatyczne odnowienie:**

    # Dodaj do cron (odnowienie co 12h)
    0 */12 * * * certbot renew --quiet

---

#### Uzyskanie Certyfikatu (Apache)

    sudo apt install certbot python3-certbot-apache
    sudo certbot --apache -d example.com -d www.example.com

---

#### Wildcard Certificate (Let's Encrypt)

**Wymagane:** DNS challenge (nie HTTP).

    sudo certbot certonly --manual --preferred-challenges dns -d "*.example.com" -d example.com

**Proces:**

    1. Certbot prosi o utworzenie DNS TXT record:
       _acme-challenge.example.com TXT "abc123xyz..."
    
    2. Dodaj rekord w panelu DNS (np. Cloudflare, OVH)
    
    3. Poczekaj 5 minut (propagacja DNS)
    
    4. Naciśnij Enter w Certbot
    
    5. Let's Encrypt weryfikuje DNS → certyfikat ✅

---

### Metoda 2: Płatny CA (DigiCert, Sectigo, GlobalSign)

**Kiedy wybrać płatny:**
- Potrzebujesz **OV** lub **EV**
- Wsparcie techniczne 24/7
- Warranty (odszkodowanie w razie błędu CA)
- Długość ważności (do 398 dni zamiast 90)

#### Proces Zakupu (Przykład: DigiCert OV)

**Krok 1: Wygeneruj CSR (Certificate Signing Request)**

**Linux/macOS:**

    openssl req -new -newkey rsa:2048 -nodes -keyout example.com.key -out example.com.csr

**Wypełnij dane:**

    Country Name: PL
    State: Mazovia
    Locality: Warsaw
    Organization: Example Corp
    Common Name: www.example.com
    Email: admin@example.com

**Pliki:**
- `example.com.key` - **KLUCZ PRYWATNY** (TRZYMAJ W TAJEMNICY!)
- `example.com.csr` - Certificate Signing Request (wysyłasz do CA)

---

**Krok 2: Złóż Zamówienie u CA**

1. Idź do: https://www.digicert.com/
2. Wybierz: **OV SSL Certificate**
3. Wklej **CSR**:
   
       -----BEGIN CERTIFICATE REQUEST-----
       MIICszCCAZsCAQAwbjELMAkGA1UEBhMCUEwx...
       -----END CERTIFICATE REQUEST-----

4. Wypełnij dane firmy (nazwa, adres, telefon)
5. Wybierz metodę walidacji domeny:
   - Email (admin@example.com)
   - DNS TXT record
   - HTTP file upload

---

**Krok 3: Walidacja Domeny**

**Przykład (Email):**

    1. CA wysyła email na: admin@example.com
    2. Email zawiera link weryfikacyjny
    3. Kliknij link → domena zweryfikowana ✅

**Przykład (DNS):**

    1. CA podaje TXT record:
       _validation.example.com TXT "abc123xyz..."
    2. Dodaj w panelu DNS
    3. CA sprawdza DNS → zweryfikowane ✅

---

**Krok 4: Weryfikacja Firmy (OV)**

CA dzwoni na numer telefonu z KRS lub WHOIS:

    CA: Dzień dobry, DigiCert. Weryfikujemy zamówienie certyfikatu dla example.com.
    Ty: Tak, potwierdzam zamówienie.
    CA: Dziękujemy. Certyfikat zostanie wystawiony w ciągu 1-3 dni.

---

**Krok 5: Otrzymanie Certyfikatu**

CA wysyła email z plikami:
- `example_com.crt` - Twój certyfikat
- `DigiCertCA.crt` - Certyfikat pośredni CA
- `TrustedRoot.crt` - Root CA (opcjonalnie)

---

**Krok 6: Instalacja na Serwerze**

(Patrz sekcja: [Instalacja certyfikatu na serwerze](#instalacja-certyfikatu-na-serwerze))

---

### Metoda 3: Self-Signed Certificate (Tylko Testy!)

**UWAGA:** Przeglądarki będą pokazywać ostrzeżenie! Tylko dla:
- Localhost
- Środowisko deweloperskie
- Testowanie (patrz: Docker Testing)

#### Generowanie Self-Signed (OpenSSL)

    # Wygeneruj certyfikat ważny 365 dni
    openssl req -x509 -newkey rsa:2048 -nodes \
      -keyout selfsigned.key \
      -out selfsigned.crt \
      -days 365 \
      -subj "/C=PL/ST=Mazovia/L=Warsaw/O=Test/CN=localhost"

**Pliki:**
- `selfsigned.key` - Klucz prywatny
- `selfsigned.crt` - Certyfikat

---

## Instalacja Certyfikatu na Serwerze

### Nginx

#### Krok 1: Przygotuj Pliki

Skopiuj certyfikaty do `/etc/nginx/ssl/`:

    sudo mkdir -p /etc/nginx/ssl
    sudo cp example.com.crt /etc/nginx/ssl/
    sudo cp example.com.key /etc/nginx/ssl/
    sudo cp DigiCertCA.crt /etc/nginx/ssl/

#### Krok 2: Połącz Łańcuch Certyfikatów

Nginx wymaga **pełnego łańcucha** (end-entity + intermediate):

    cat example.com.crt DigiCertCA.crt > /etc/nginx/ssl/fullchain.crt

#### Krok 3: Nadaj Uprawnienia

    sudo chmod 600 /etc/nginx/ssl/example.com.key
    sudo chmod 644 /etc/nginx/ssl/fullchain.crt

#### Krok 4: Konfiguracja Nginx

Edytuj `/etc/nginx/sites-available/example.com`:

    server {
        listen 443 ssl http2;
        server_name example.com www.example.com;
    
        # Certyfikat SSL
        ssl_certificate /etc/nginx/ssl/fullchain.crt;
        ssl_certificate_key /etc/nginx/ssl/example.com.key;
    
        # Silne szyfrowanie
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
        ssl_prefer_server_ciphers on;
    
        # OCSP Stapling
        ssl_stapling on;
        ssl_stapling_verify on;
        ssl_trusted_certificate /etc/nginx/ssl/DigiCertCA.crt;
    
        # HSTS (wymusz HTTPS)
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
        location / {
            root /var/www/example.com;
            index index.html;
        }
    }
    
    # Przekierowanie HTTP → HTTPS
    server {
        listen 80;
        server_name example.com www.example.com;
        return 301 https://$server_name$request_uri;
    }

#### Krok 5: Test i Restart

    # Sprawdź składnię
    sudo nginx -t
    
    # Restart
    sudo systemctl restart nginx

#### Krok 6: Weryfikacja

    curl -I https://example.com
    # HTTP/1.1 200 OK

---

### Apache

#### Krok 1: Włącz Moduł SSL

    sudo a2enmod ssl
    sudo a2ensite default-ssl

#### Krok 2: Konfiguracja Apache

Edytuj `/etc/apache2/sites-available/example.com-ssl.conf`:

    <VirtualHost *:443>
        ServerName example.com
        ServerAlias www.example.com
    
        DocumentRoot /var/www/example.com
    
        SSLEngine on
        SSLCertificateFile /etc/apache2/ssl/example.com.crt
        SSLCertificateKeyFile /etc/apache2/ssl/example.com.key
        SSLCertificateChainFile /etc/apache2/ssl/DigiCertCA.crt
    
        # Silne szyfrowanie
        SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
        SSLCipherSuite HIGH:!aNULL:!MD5
        SSLHonorCipherOrder on
    
        # HSTS
        Header always set Strict-Transport-Security "max-age=31536000"
    </VirtualHost>
    
    # Przekierowanie HTTP → HTTPS
    <VirtualHost *:80>
        ServerName example.com
        Redirect permanent / https://example.com/
    </VirtualHost>

#### Krok 3: Restart

    sudo a2ensite example.com-ssl
    sudo systemctl restart apache2

---

### IIS (Windows Server)

#### Krok 1: Importuj Certyfikat

1. Otwórz **IIS Manager** (Win + R → `inetmgr`)
2. Kliknij nazwę serwera (lewy panel)
3. Dwukrotnie kliknij **"Server Certificates"**
4. Prawy panel → **"Import..."**
5. Wybierz plik `.pfx` (lub `.p12`)
   
   **Jeśli masz `.crt` + `.key`, najpierw konwertuj do PFX:**
   
       openssl pkcs12 -export -out example.com.pfx \
         -inkey example.com.key \
         -in example.com.crt \
         -certfile DigiCertCA.crt

6. Podaj hasło (jeśli ustawione)
7. Kliknij **OK**

#### Krok 2: Bind Certyfikat do Witryny

1. Rozwiń **"Sites"** (lewy panel)
2. Kliknij prawym na witrynę → **"Edit Bindings..."**
3. Kliknij **"Add..."**
4. **Type:** `https`
5. **Port:** `443`
6. **SSL Certificate:** Wybierz `example.com`
7. Kliknij **OK**

#### Krok 3: Test

Otwórz: `https://example.com` w przeglądarce.

---

## Odnowienie Certyfikatów

### Dlaczego Certyfikaty Wygasają?

**Bezpieczeństwo:**
- Krótszy okres = mniejsze okno ataku gdyby klucz wyciekł
- Wymusza regularne sprawdzanie konfiguracji

**CA/Browser Forum (od 2020):**
- Maksymalny okres: **398 dni** (13 miesięcy)
- Wcześniej było 2-3 lata!

---

### Automatyczne Odnowienie (Let's Encrypt + Certbot)

Certbot automatycznie odnawia certyfikaty < 30 dni przed wygaśnięciem.

**Cron (uruchom 2x dziennie):**

    0 */12 * * * certbot renew --quiet --post-hook "systemctl reload nginx"

**Test suchego uruchomienia:**

    sudo certbot renew --dry-run

**Oczekiwany output:**

    Cert not yet due for renewal
    
    Congratulations, all simulated renewals succeeded:
      /etc/letsencrypt/live/example.com/fullchain.pem (success)

---

### Ręczne Odnowienie (Płatne CA)

**Proces podobny do pierwszego zakupu:**

#### Opcja A: Rekey (Nowy Klucz)

1. Wygeneruj nowy CSR:
   
       openssl req -new -newkey rsa:2048 -nodes -keyout example.com-new.key -out example.com-new.csr

2. Złóż zamówienie odnowienia u CA
3. Wklej nowy CSR
4. Walidacja (email/DNS - szybsza przy odnowieniu)
5. Otrzymaj nowy certyfikat
6. Zainstaluj na serwerze

---

#### Opcja B: Renew (Ten Sam Klucz)

1. Użyj starego klucza + wygeneruj CSR:
   
       openssl req -new -key example.com.key -out example.com-renew.csr

2. Wklej CSR do CA
3. Otrzymaj certyfikat

**UWAGA:** Zalecane **rekey** (nowy klucz) dla lepszego bezpieczeństwa.

---

### Monitoring Wygaśnięcia

**To jest właśnie cel tego projektu!**

    python scripts/main.py --check-now --threshold 30

**Otrzymasz alert** gdy certyfikat wygasa < 30 dni.

---

# Część IV: Bezpieczeństwo

## Typowe Zagrożenia i Ataki

### 1. Man-in-the-Middle (MITM)

**Opis:** Atakujący przechwytuje komunikację między klientem a serwerem.

**Scenariusz:**

    Ty → [☠️ Atakujący] → Serwer
    
    Atakujący:
    - Podszywa się pod serwer (dla Ciebie)
    - Podszywa się pod Ciebie (dla serwera)
    - Widzi WSZYSTKO (hasła, dane karty)

**Jak SSL/TLS chroni:**
- **Certyfikat** potwierdza tożsamość serwera
- Atakujący **nie ma klucza prywatnego** serwera → nie może odszyfrować

**Ale uwaga:** MITM możliwy gdy:
- Użytkownik kliknie "Kontynuuj mimo ostrzeżenia" (invalid cert)
- Zainstalowano złośliwy Root CA (malware)
- Korporacyjny proxy SSL interception

---

### 2. SSL Stripping

**Opis:** Atakujący zmusza użytkownika do użycia HTTP zamiast HTTPS.

**Scenariusz:**

    1. Użytkownik wpisuje: example.com (bez https://)
    2. Przeglądarka próbuje HTTP: http://example.com
    3. Atakujący przechwytuje i blokuje przekierowanie HTTPS
    4. Użytkownik pozostaje na HTTP (nieszyfrowane!)

**Ochrona:**
- **HSTS** (HTTP Strict Transport Security):
  
      Strict-Transport-Security: max-age=31536000; includeSubDomains

- Przeglądarka **wymusza HTTPS** przez rok (nawet jeśli użytkownik wpisze http://)
- **HSTS Preload List:** https://hstspreload.org/ (wbudowane w Chrome, Firefox)

---

### 3. Certificate Spoofing (Fałszywy Certyfikat)

**Opis:** Atakujący wystawia fałszywy certyfikat dla example.com.

**Jak to możliwe:**
- Skompromitowany CA (bardzo rzadkie, np. DigiNotar 2011)
- Exploit w implementacji SSL (Heartbleed)
- Użytkownik zainstalował złośliwy Root CA

**Ochrona:**
- **Certificate Transparency (CT):** Wszystkie certyfikaty logowane publicznie
  - https://crt.sh/ - wyszukiwarka CT logs
  - Można monitorować czy ktoś wystawił certyfikat dla Twojej domeny
- **CAA DNS record:** Określ które CA mogą wystawiać certyfikaty
  
      example.com. CAA 0 issue "letsencrypt.org"
      example.com. CAA 0 issue "digicert.com"

---

### 4. Downgrade Attack (Wymuszenie Słabego Szyfrowania)

**Opis:** Atakujący zmusza serwer do użycia starego, słabego protokołu (SSL 3.0, TLS 1.0).

**Przykład:** POODLE Attack (2014) - exploit w SSL 3.0.

**Ochrona:**
- **Wyłącz stare protokoły:**
  
      # Nginx
      ssl_protocols TLSv1.2 TLSv1.3;
      
      # Apache
      SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1

---

### 5. Expired Certificate (Wygasły Certyfikat)

**Opis:** Certyfikat wygasł, przeglądarka pokazuje ostrzeżenie.

**Skutki:**
- Użytkownicy nie zaufają witrynie
- Utrata konwersji (~95%)
- Google penalty (niższe pozycje)

**Ochrona:** **Ten projekt!** Certificate Expiry Monitor

---

## Best Practices Bezpieczeństwa

### 1. Używaj Silnych Algorytmów

**Zalecane:**
- **Klucz:** RSA 2048-bit (minimum) lub ECDSA P-256
- **Hash:** SHA-256 (minimum)
- **Szyfrowanie:** AES-256-GCM, ChaCha20-Poly1305

**Zabronione (podatne):**
- ❌ RSA 1024-bit (łamany przez NSA)
- ❌ MD5, SHA-1 (kolizje hashowania)
- ❌ RC4, DES, 3DES (słabe cipher suites)

---

### 2. Implementuj HSTS

    # Nginx
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

**Parametry:**
- `max-age=31536000` - Wymuszaj HTTPS przez 1 rok
- `includeSubDomains` - Dotyczy też subdomen
- `preload` - Dodaj do HSTS Preload List (https://hstspreload.org/)

---

### 3. Włącz OCSP Stapling

**Czym jest OCSP Stapling?**

Bez stapling:

    1. Przeglądarka łączy się z serwerem
    2. Pobiera certyfikat
    3. Łączy się z OCSP responder CA (dodatkowe połączenie!)
    4. Sprawdza status certyfikatu
    5. Ładuje stronę

Z stapling:

    1. Serwer okresowo odpytuje OCSP responder
    2. Przechowuje odpowiedź (cache)
    3. Wysyła response razem z certyfikatem
    4. Przeglądarka weryfikuje offline

**Korzyści:**
- **Szybsze** (brak dodatkowego połączenia)
- **Privacy** (CA nie widzi IP użytkownika)

**Konfiguracja (Nginx):**

    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/nginx/ssl/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;

---

### 4. Chroń Klucz Prywatny

**NIGDY NIE:**
- ❌ Commituj klucza do Git
- ❌ Wysyłaj przez email
- ❌ Przechowuj w public S3 bucket
- ❌ Nadawaj uprawnień 777

**ZAWSZE:**
- ✅ Uprawnienia `chmod 600` (tylko root może czytać)
- ✅ Backup zaszyfrowany (GPG, AWS KMS)
- ✅ HSM (Hardware Security Module) dla produkcji krytycznej

---

### 5. Regularnie Odnawiane Certyfikaty

**Automatyzacja:**
- Certbot dla Let's Encrypt
- ACME protocol dla innych CA
- Monitoring (ten projekt!)

**Harmonogram:**
- Certyfikat 90-dniowy (Let's Encrypt): odnowienie po 60 dniach
- Certyfikat 1-roczny: odnowienie po 300 dniach (30 dni bufor)

---

### 6. Sprawdź Konfigurację (SSL Labs)

**Narzędzie:** https://www.ssllabs.com/ssltest/

**Test:**

    1. Idź do: https://www.ssllabs.com/ssltest/
    2. Wpisz: example.com
    3. Poczekaj 2 minuty
    4. Otrzymasz ocenę: A+, A, B, C, F

**Cele:**
- **A+** - Idealna konfiguracja
- **A** - Dobra (wystarczająca dla większości)
- **B** - Słaba (przestarzałe protokoły)
- **F** - Krytyczne błędy (wygasły certyfikat, self-signed)

---

## Compliance i Standardy

### PCI-DSS (Payment Card Industry)

**Wymogi dla płatności kartą:**
- ✅ TLS 1.2+ (zakaz TLS 1.0, 1.1)
- ✅ Minimum RSA 2048-bit
- ✅ Zakaz słabych cipher suites
- ✅ Regular vulnerability scanning

**Konsekwencje braku compliance:**
- Brak możliwości przyjmowania płatności kartą
- Kary finansowe (do $100,000/miesiąc)

---

### RODO (GDPR)

**Art. 32: Bezpieczeństwo przetwarzania**

*"Stosowanie odpowiednich środków technicznych... w tym szyfrowanie danych osobowych"*

**Interpretacja:**
- HTTPS **wymagane** dla formularzy z danymi osobowymi
- Brak HTTPS = naruszenie RODO = kara do 20M EUR (lub 4% obrotu)

---

### HIPAA (Ochrona Zdrowia, USA)

**Wymogi:**
- ✅ TLS dla transmisji danych medycznych
- ✅ Audit logs (kto dostęp do danych)
- ✅ Business Associate Agreement (z CA)

---

# Część V: Troubleshooting

## Diagnostyka Problemów

### Narzędzie 1: OpenSSL (CLI)

**Test połączenia:**

    openssl s_client -connect example.com:443 -servername example.com

**Output:**

    CONNECTED(00000003)
    depth=2 C=US, O=DigiCert Inc, OU=www.digicert.com, CN=DigiCert Global Root CA
    verify return:1
    depth=1 C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA
    verify return:1
    depth=0 C=US, ST=California, L=San Francisco, O=Example Corp, CN=www.example.com
    verify return:1
    ---
    Certificate chain
     0 s:CN=www.example.com
       i:CN=DigiCert SHA2 Secure Server CA
     1 s:CN=DigiCert SHA2 Secure Server CA
       i:CN=DigiCert Global Root CA
    ---
    Server certificate
    -----BEGIN CERTIFICATE-----
    MIIFdzCCBF+gAwIBAgIQE/xFPPvvMm3JKQxLHXKq...
    -----END CERTIFICATE-----
    subject=CN=www.example.com
    issuer=CN=DigiCert SHA2 Secure Server CA
    ---
    SSL handshake has read 4567 bytes and written 456 bytes
    ---
    New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
    ---

**Sprawdź:**
- `verify return:1` = certyfikat OK ✅
- `New, TLSv1.3` = protokół ✅
- `Certificate chain` = łańcuch kompletny ✅

---

### Narzędzie 2: curl

**Test HTTPS:**

    curl -I https://example.com

**Output:**

    HTTP/2 200
    server: nginx
    date: Wed, 28 Jan 2026 22:30:00 GMT
    content-type: text/html
    strict-transport-security: max-age=31536000

**Jeśli błąd:**

    curl: (60) SSL certificate problem: certificate has expired

**Debug:**

    curl -v https://example.com 2>&1 | grep -i 'ssl\|certificate'

---

### Narzędzie 3: Browser DevTools

**Chrome:**
1. Otwórz `https://example.com`
2. F12 → **Security** tab
3. Kliknij **"View certificate"**

**Sprawdź:**
- ✅ Valid certificate
- ✅ Secure connection
- ✅ Issued by trusted CA

**Jeśli ostrzeżenie:**
- "Your connection is not private" = invalid cert
- "NET::ERR_CERT_DATE_INVALID" = wygasły
- "NET::ERR_CERT_COMMON_NAME_INVALID" = zła domena

---

## Najczęstsze Błędy

### Błąd 1: "Certificate has expired"

**Przyczyna:** Certyfikat wygasł.

**Diagnoza:**

    openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

**Output:**

    notBefore=Jan  1 00:00:00 2025 GMT
    notAfter =Jan  1 00:00:00 2026 GMT  ← PRZESZŁA DATA!

**Rozwiązanie:** Odnów certyfikat (patrz: [Odnowienie certyfikatów](#odnowienie-certyfikatów))

---

### Błąd 2: "Common name mismatch"

**Przyczyna:** Certyfikat wystawiony dla innej domeny.

**Przykład:**
- Certyfikat: `CN=example.com`
- Odwiedzasz: `www.example.com` ← BŁĄD!

**Rozwiązanie:**
- Użyj certyfikatu z SAN: `DNS:example.com, DNS:www.example.com`
- Lub wildcard: `*.example.com`

---

### Błąd 3: "Incomplete certificate chain"

**Przyczyna:** Serwer nie wysyła certyfikatu pośredniego (intermediate).

**Diagnoza:**

    openssl s_client -connect example.com:443 -showcerts

**Jeśli widzisz tylko 1 certyfikat → BRAK ŁAŃCUCHA!**

**Rozwiązanie:**

    # Nginx
    ssl_certificate /etc/nginx/ssl/fullchain.crt;  # ← end-entity + intermediate
    
    # Apache
    SSLCertificateChainFile /etc/apache2/ssl/intermediate.crt

---

### Błąd 4: "Self-signed certificate"

**Przyczyna:** Certyfikat podpisany sam przez siebie (nie przez CA).

**Kiedy OK:**
- Localhost (dev)
- Internal tools (intranet)

**Kiedy ŹLE:**
- Publiczna strona WWW
- E-commerce

**Rozwiązanie:** Użyj Let's Encrypt (darmowy) lub płatnego CA.

---

### Błąd 5: "Mixed content" (HTTP + HTTPS)

**Przyczyna:** Strona HTTPS ładuje zasoby przez HTTP.

**Przykład:**

    <html>
    <head>
        <link rel="stylesheet" href="http://example.com/style.css">  ← HTTP!
    </head>

**Przeglądarka blokuje:** "Mixed Content: The page was loaded over HTTPS, but requested an insecure resource..."

**Rozwiązanie:**

    # Zmień na HTTPS
    <link rel="stylesheet" href="https://example.com/style.css">
    
    # Lub protocol-relative
    <link rel="stylesheet" href="//example.com/style.css">

---

## 🎓 Podsumowanie

**Gratulacje!** Ukończyłeś kompletne szkolenie SSL/TLS! 🎉

**Poznałeś:**
- ✅ Czym są certyfikaty i jak działają
- ✅ TLS Handshake krok po kroku
- ✅ Anatomia certyfikatu X.509
- ✅ Jak uzyskać i zainstalować certyfikat
- ✅ Bezpieczeństwo i best practices
- ✅ Troubleshooting i narzędzia

**Następne kroki:**
1. **[Installation Guide](INSTALLATION_AND_USAGE.md)** - Zainstaluj Certificate Monitor
2. **[Docker Testing](DOCKER_TESTING.md)** - Przetestuj w środowisku Docker
3. **[Real-World Scenarios](REAL_WORLD_SCENARIOS.md)** - Praktyczne przykłady użycia

---

**Powodzenia w zarządzaniu certyfikatami!** 🚀🔒
