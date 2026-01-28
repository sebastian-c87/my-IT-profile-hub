# ===================================================
# Dockerfile - Obraz Nginx z Obsługą SSL/TLS
# ===================================================
# 
# Ten plik definiuje, jak Docker ma zbudować obraz
# kontenera z serwerem Nginx gotowym do testowania
# certyfikatów SSL/TLS w różnych stanach.
#
# ===================================================

# Bazowy obraz - oficjalny Nginx w wersji Alpine (lekki)
FROM nginx:alpine

# Metadane obrazu
LABEL maintainer="Sebastian Ciborowski <sebastian-c87>"
LABEL description="Nginx test environment for SSL/TLS certificate monitoring"
LABEL version="1.0"

# Instalacja dodatkowych narzędzi
# - curl: Potrzebny do healthcheck w docker-compose.yml
# - openssl: Do debugowania certyfikatów (opcjonalne)
RUN apk add --no-cache curl openssl

# Utworzenie katalogów na certyfikaty
# (Foldery będą montowane z hosta przez volumes w docker-compose.yml)
RUN mkdir -p /etc/nginx/certs/valid \
             /etc/nginx/certs/expiring \
             /etc/nginx/certs/expired

# Kopiowanie domyślnej strony HTML (opcjonalne)
# Ta strona będzie wyświetlana, gdy użytkownik połączy się przez HTTPS
RUN echo '<html><head><title>Certificate Test Environment</title></head>' > /usr/share/nginx/html/index.html && \
    echo '<body style="font-family: Arial; text-align: center; padding: 50px;">' >> /usr/share/nginx/html/index.html && \
    echo '<h1>🔒 SSL/TLS Certificate Test Server</h1>' >> /usr/share/nginx/html/index.html && \
    echo '<p>This server is part of the <strong>Certificate-Expiry-Monitor</strong> testing environment.</p>' >> /usr/share/nginx/html/index.html && \
    echo '<p>Check the certificate details in your browser or use:</p>' >> /usr/share/nginx/html/index.html && \
    echo '<code>openssl s_client -connect localhost:8443 -showcerts</code>' >> /usr/share/nginx/html/index.html && \
    echo '</body></html>' >> /usr/share/nginx/html/index.html

# Eksponowanie portów
# (Te porty będą dostępne dla innych kontenerów w tej samej sieci Docker)
EXPOSE 8443 8444 8445

# Domyślne polecenie - uruchomienie Nginx w trybie foreground
# (Nginx musi działać w trybie foreground, aby kontener się nie zatrzymał)
CMD ["nginx", "-g", "daemon off;"]

# ===================================================
# WYJAŚNIENIE KROK PO KROKU
# ===================================================
#
# 1. FROM nginx:alpine
#    - Używamy oficjalnego obrazu Nginx w wersji Alpine Linux
#    - Alpine to minimalistyczna dystrybucja (rozmiar ~5MB vs ~130MB)
#    - Zawiera już skompilowany Nginx z obsługą SSL/TLS
#
# 2. LABEL
#    - Metadane obrazu (autor, opis, wersja)
#    - Widoczne przez: docker inspect <obraz>
#
# 3. RUN apk add --no-cache curl openssl
#    - apk = package manager w Alpine Linux (odpowiednik apt/yum)
#    - --no-cache = Nie zapisuj cache pakietów (mniejszy obraz)
#    - curl = Do healthcheck (docker-compose sprawdza, czy serwer działa)
#    - openssl = Do ręcznego debugowania certyfikatów
#
# 4. RUN mkdir -p /etc/nginx/certs/*
#    - Tworzy strukturę katalogów na certyfikaty
#    - -p = Tworzy katalogi rekursywnie (nie zgłasza błędu, jeśli istnieją)
#    - Te foldery będą "przysłonięte" przez volumes z docker-compose.yml
#
# 5. RUN echo ... > /usr/share/nginx/html/index.html
#    - Tworzy prostą stronę HTML, która wyświetli się po otwarciu https://localhost:8443
#    - Użytkownik zobaczy informację o środowisku testowym
#
# 6. EXPOSE 8443 8444 8445
#    - Informuje Docker, że kontener nasłuchuje na tych portach
#    - To NIE mapuje portów na host (to robi docker-compose.yml w sekcji "ports")
#
# 7. CMD ["nginx", "-g", "daemon off;"]
#    - Uruchamia Nginx w trybie foreground (nie w tle)
#    - Dlaczego? Docker zatrzymuje kontener, gdy główny proces kończy działanie
#    - "daemon off;" = Nginx nie przechodzi w tryb demona (zostaje na pierwszym planie)
