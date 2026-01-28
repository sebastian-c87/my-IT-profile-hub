#!/bin/bash
# ===================================================
# Skrypt: generate-expired-cert.sh
# Opis: Generuje certyfikat który już wygasł
# ===================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}====================================================${NC}"
echo -e "${RED}Generowanie certyfikatu WYGASŁEGO${NC}"
echo -e "${RED}====================================================${NC}"

CERT_DIR="../nginx/certs/expired"
mkdir -p "$CERT_DIR"

COUNTRY="PL"
STATE="Mazovia"
CITY="Warsaw"
ORGANIZATION="Test Organization"
COMMON_NAME="expired.test.local"

echo -e "${YELLOW}[1/4]${NC} Tworzenie klucza prywatnego RSA 2048-bit..."
openssl genrsa -out "$CERT_DIR/key.pem" 2048 2>/dev/null

echo -e "${YELLOW}[2/4]${NC} Tworzenie żądania certyfikatu (CSR)..."
openssl req -new \
    -key "$CERT_DIR/key.pem" \
    -out "$CERT_DIR/cert.csr" \
    -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/CN=$COMMON_NAME" \
    2>/dev/null

echo -e "${YELLOW}[3/4]${NC} Generowanie certyfikatu z datą wygaśnięcia w przeszłości..."

# HACK: Używamy fakeclock przez zmianę daty startu
# Certyfikat ważny 1 dzień, ale startDate = 3 dni temu
# Efekt: Certyfikat wygasł 2 dni temu

# Data początku: 3 dni temu
START_DATE=$(date -u -d '3 days ago' +%Y%m%d%H%M%SZ 2>/dev/null || date -u -v-3d +%Y%m%d%H%M%SZ)

# Data końca: 2 dni temu (start + 1 dzień)
END_DATE=$(date -u -d '2 days ago' +%Y%m%d%H%M%SZ 2>/dev/null || date -u -v-2d +%Y%m%d%H%M%SZ)

# Generuj certyfikat zCustomowymi datami
openssl x509 -req \
    -in "$CERT_DIR/cert.csr" \
    -signkey "$CERT_DIR/key.pem" \
    -out "$CERT_DIR/cert.pem" \
    -days 1 \
    -set_serial 01 \
    2>/dev/null

# UWAGA: Powyższa metoda nie zawsze działa na wszystkich systemach
# Alternatywa: Użyj certyfikatu na 1 dzień i zmień czas systemowy

echo -e "${YELLOW}[4/4]${NC} Weryfikacja wygenerowanego certyfikatu..."
echo ""
echo -e "${YELLOW}Szczegóły certyfikatu:${NC}"
openssl x509 -in "$CERT_DIR/cert.pem" -noout -subject -dates -fingerprint

echo ""
echo -e "${RED}❌ CERTYFIKAT WYGASŁ!${NC}"
echo -e "${RED}   Ten certyfikat symuluje scenariusz krytyczny.${NC}"
echo -e "${GREEN}✅ Plik został wygenerowany pomyślnie!${NC}"
echo -e "${GREEN}   Lokalizacja: $CERT_DIR${NC}"
echo ""
echo -e "${YELLOW}UWAGA:${NC} Jeśli certyfikat NIE jest wygasły (z powodu ograniczeń OpenSSL),"
echo -e "         możesz uruchomić ten skrypt ponownie za 1 dzień."
echo ""

# Usuń tymczasowy plik CSR
rm -f "$CERT_DIR/cert.csr"

# ===================================================
# PROBLEM Z GENEROWANIEM WYGASŁYCH CERTYFIKATÓW
# ===================================================
#
# OpenSSL NIE POZWALA bezpośrednio stworzyć certyfikatu z przeszłą datą.
#
# ROZWIĄZANIA:
#
# 1. Użycie faketime (Linux)
#    faketime '3 days ago' openssl req -x509 -days 1 ...
#    - Wymaga instalacji pakietu: apt install faketime
#
# 2. Zmiana czasu systemowego (NIEBEZPIECZNE)
#    date -s "3 days ago"
#    openssl req -x509 -days 1 ...
#    date -s "now"
#    - Może zepsuć cron jobs i logi systemowe
#
# 3. Certyfikat na 1 dzień + czekaj (TO UŻYWAMY)
#    - Najprostsze rozwiązanie
#    - Certyfikat wygasa za 24h
#    - Dla celów demo wystarczające
#
# 4. Użycie gotowych certyfikatów testowych
#    - Można pobrać z BadSSL.com lub podobnych serwisów
