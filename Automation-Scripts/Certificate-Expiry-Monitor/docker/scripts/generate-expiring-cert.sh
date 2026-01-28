#!/bin/bash
# ===================================================
# Skrypt: generate-expiring-cert.sh
# Opis: Generuje certyfikat wygasający za 7 dni
# ===================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}====================================================${NC}"
echo -e "${YELLOW}Generowanie certyfikatu WYGASAJĄCEGO (7 dni)${NC}"
echo -e "${YELLOW}====================================================${NC}"

CERT_DIR="../nginx/certs/expiring"
mkdir -p "$CERT_DIR"

DAYS_VALID=7
COUNTRY="PL"
STATE="Mazovia"
CITY="Warsaw"
ORGANIZATION="Test Organization"
COMMON_NAME="expiring.test.local"

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
echo ""
echo -e "${YELLOW}Szczegóły certyfikatu:${NC}"
openssl x509 -in "$CERT_DIR/cert.pem" -noout -subject -dates -fingerprint

# Oblicz dokładną datę wygaśnięcia
EXPIRY_DATE=$(openssl x509 -in "$CERT_DIR/cert.pem" -noout -enddate | cut -d= -f2)

echo ""
echo -e "${YELLOW}⚠️  UWAGA: Certyfikat wygasa za $DAYS_VALID dni!${NC}"
echo -e "${YELLOW}   Data wygaśnięcia: $EXPIRY_DATE${NC}"
echo -e "${GREEN}✅ Certyfikat został wygenerowany pomyślnie!${NC}"
echo -e "${GREEN}   Lokalizacja: $CERT_DIR${NC}"
echo ""

# ===================================================
# DLACZEGO 7 DNI?
# ===================================================
#
# W rzeczywistych środowiskach produkcyjnych:
# - Administratorzy ustawiają alerty na 30/14/7 dni przed wygaśnięciem
# - 7 dni = Ostatnia szansa na odnowienie przed wpływem na biznes
# - Let's Encrypt certyfikaty (darmowe) są ważne tylko 90 dni
# - Wymuszają automatyzację odnowień (np. przez certbot)
#
# W tym projekcie:
# - 7 dni symuluje "stan alarmowy" (WARNING)
# - Skrypt Python wysyła email/Slack z alertem
# - Administrator ma czas na reakcję przed wygaśnięciem
