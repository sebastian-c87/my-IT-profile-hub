#!/bin/bash
# ===================================================
# Skrypt: generate-valid-cert.sh
# Opis: Generuje certyfikat SSL/TLS ważny przez 90 dni
# ===================================================

set -e  # Zatrzymaj skrypt przy błędzie

# Kolory dla czytelności outputu
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}====================================================${NC}"
echo -e "${YELLOW}Generowanie certyfikatu WAŻNEGO (90 dni)${NC}"
echo -e "${YELLOW}====================================================${NC}"

# Ścieżka do folderu z certyfikatami
CERT_DIR="../nginx/certs/valid"

# Utwórz folder, jeśli nie istnieje
mkdir -p "$CERT_DIR"

# Parametry certyfikatu
DAYS_VALID=90
COUNTRY="PL"
STATE="Mazovia"
CITY="Warsaw"
ORGANIZATION="Test Organization"
COMMON_NAME="valid.test.local"

echo -e "${GREEN}[1/3]${NC} Tworzenie klucza prywatnego RSA 2048-bit..."
openssl genrsa -out "$CERT_DIR/key.pem" 2048 2>/dev/null

echo -e "${GREEN}[2/3]${NC} Generowanie certyfikatu X.509 (self-signed)..."
openssl req -new -x509 \
    -key "$CERT_DIR/key.pem" \
    -out "$CERT_DIR/cert.pem" \
    -days $DAYS_VALID \
    -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/CN=$COMMON_NAME" \
    2>/dev/null

echo -e "${GREEN}[3/3]${NC} Weryfikacja wygenerowanego certyfikatu..."

# Wyświetl informacje o certyfikacie
echo ""
echo -e "${YELLOW}Szczegóły certyfikatu:${NC}"
openssl x509 -in "$CERT_DIR/cert.pem" -noout -subject -dates -fingerprint

echo ""
echo -e "${GREEN}✅ Certyfikat ważny został wygenerowany pomyślnie!${NC}"
echo -e "${GREEN}   Lokalizacja: $CERT_DIR${NC}"
echo -e "${GREEN}   Ważność: $DAYS_VALID dni${NC}"
echo ""

# ===================================================
# WYJAŚNIENIE KROK PO KROKU
# ===================================================
#
# 1. set -e
#    - Zatrzymuje wykonanie skryptu, jeśli jakakolwiek komenda zwróci błąd
#    - Bezpieczeństwo: Zapobiega użyciu uszkodzonych certyfikatów
#
# 2. mkdir -p "$CERT_DIR"
#    - Tworzy katalog na certyfikaty
#    - -p = Nie zgłasza błędu, jeśli katalog już istnieje
#
# 3. openssl genrsa -out "$CERT_DIR/key.pem" 2048
#    - genrsa = Generuje klucz prywatny RSA
#    - 2048 = Długość klucza w bitach (standard bezpieczeństwa)
#    - key.pem = Plik z kluczem prywatnym (MUSI BYĆ CHRONIONY!)
#    - 2>/dev/null = Ukrywa verbose output OpenSSL
#
# 4. openssl req -new -x509
#    - req = Request (żądanie certyfikatu)
#    - -new = Nowe żądanie
#    - -x509 = Generuj certyfikat X.509 (standard SSL/TLS)
#    - -key = Użyj tego klucza prywatnego
#    - -out = Zapisz certyfikat do tego pliku
#    - -days 90 = Certyfikat ważny przez 90 dni
#    - -subj = Dane identyfikacyjne (Subject)
#       /C=PL = Country (Kraj)
#       /ST=Mazovia = State (Województwo)
#       /L=Warsaw = Locality (Miasto)
#       /O=Test Organization = Organization (Organizacja)
#       /CN=valid.test.local = Common Name (Nazwa hosta)
#
# 5. openssl x509 -in ... -noout -subject -dates -fingerprint
#    - x509 = Operacje na certyfikatach X.509
#    - -noout = Nie wyświetlaj całego certyfikatu (tylko wybrane pola)
#    - -subject = Pokaż dane identyfikacyjne (CN, O, C, etc.)
#    - -dates = Pokaż daty ważności (notBefore, notAfter)
#    - -fingerprint = Pokaż odcisk palca SHA-1 (unikalny identyfikator)
#
# RÓŻNICA: Self-Signed vs CA-Signed
#    - Self-signed: Certyfikat podpisany własnym kluczem (do testów)
#    - CA-signed: Certyfikat podpisany przez zaufane CA (Let's Encrypt, DigiCert)
#    - Przeglądarki ufają tylko CA-signed, dlatego self-signed wyświetla ostrzeżenie
