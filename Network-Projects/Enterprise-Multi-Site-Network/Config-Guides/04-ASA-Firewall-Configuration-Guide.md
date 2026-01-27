# 🔥 ASA Firewall – Konfiguracja Bezpieczeństwa Sieci

## 🎯 Cel konfiguracji

Skonfigurowanie firewall Cisco ASA 5506-X jako **bramy bezpieczeństwa** między strefami:
- ✅ Utworzenie **stref bezpieczeństwa** (Inside, Outside)
- ✅ Konfiguracja **Security Levels** (kontrola kierunku ruchu)
- ✅ Wdrożenie **ACL** (Access Control Lists) dla precyzyjnej kontroli dostępu
- ✅ Routing statyczny do VLANów (przez Switch L3) i sieci WAN
- ✅ Umożliwienie ruchu DHCP między strefami

---

## 📋 Wymagania wstępne

| Wymaganie | Szczegóły |
|-----------|-----------|
| **Model firewall** | Cisco ASA 5506-X |
| **Strefy** | Inside (serwery), Outside (Switch L3 + VLANy) |
| **Połączenia** | G1/1 (Inside), G1/2 (Outside) |
| **Routing** | Static routes do VLANów |

---

## 🔍 Architektura stref bezpieczeństwa

### 🟢 Inside Zone (Strefa zaufana – Security Level 100)
- **Interface:** GigabitEthernet1/1
- **IP Address:** `10.40.10.1/24`
- **Zawiera:**
  - Serwer DHCP (`10.40.10.254`)
  - Serwer DNS (`10.40.10.253`)
  - Serwer HTTP (`10.40.10.252`)
  - Switch2 (agregacja serwerów)

**Zasada:** Ruch z Inside → Outside jest **domyślnie dozwolony** (wyższy security level może inicjować połączenia do niższego)

---

### 🔴 Outside Zone (Strefa niezaufana – Security Level 0)
- **Interface:** GigabitEthernet1/2
- **IP Address:** `10.30.40.2/24`
- **Zawiera:**
  - Switch L3 (`10.30.40.1`)
  - VLANy (10.10.10.0/24, 10.10.20.0/24, 10.10.30.0/24)
  - Routery WAN

**Zasada:** Ruch z Outside → Inside jest **domyślnie blokowany** (wymaga explicit ACL)

---

## ⚙️ Konfiguracja krok po kroku

### Krok 1: Wejście w tryb konfiguracyjny

    enable
    configure terminal
    hostname ASA-Firewall

**Wyjaśnienie:**
- ASA używa podobnej składni jak routery/switche Cisco
- Tryb enable wymaga hasła (domyślnie brak – ustaw później!)

---

### Krok 2: Konfiguracja interfejsu Inside (Strefa serwerowa)

    interface GigabitEthernet1/1
     nameif inside
     security-level 100
     ip address 10.40.10.1 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- **`nameif inside`** – Nazwanie interfejsu (logiczna nazwa strefy)
- **`security-level 100`** – Najwyższy poziom zaufania (0-100)
  - Ruch z poziomu 100 → 0 jest domyślnie dozwolony
  - Ruch z poziomu 0 → 100 jest domyślnie blokowany (wymaga ACL)
- **`10.40.10.1`** – Gateway dla serwerów

---

### Krok 3: Konfiguracja interfejsu Outside (Strefa Switch L3 + VLANy)

    interface GigabitEthernet1/2
     nameif outside
     security-level 0
     ip address 10.30.40.2 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- **`security-level 0`** – Najniższy poziom (strefa niezaufana)
- Połączenie do Switch L3 (`10.30.40.1`)

---

### Krok 4: Wyłączenie nieużywanych interfejsów

    interface GigabitEthernet1/3
     shutdown
     exit
    interface GigabitEthernet1/4
     shutdown
     exit
    interface GigabitEthernet1/5
     shutdown
     exit
    interface GigabitEthernet1/6
     shutdown
     exit
    interface GigabitEthernet1/7
     shutdown
     exit
    interface GigabitEthernet1/8
     shutdown
     exit
    interface Management1/1
     shutdown
     exit

**Wyjaśnienie:**
- **Best practice bezpieczeństwa:** Wyłączaj nieużywane porty
- Zapobiega nieautoryzowanym połączeniom

---

### Krok 5: Routing statyczny do VLANów

    route outside 10.10.10.0 255.255.255.0 10.30.40.1 1
    route outside 10.10.20.0 255.255.255.0 10.30.40.1 1
    route outside 10.10.30.0 255.255.255.0 10.30.40.1 1
    route outside 0.0.0.0 0.0.0.0 10.30.40.1 1

**Wyjaśnienie:**
- **Składnia:** `route <interface> <network> <mask> <next-hop> <metric>`
- Trasy do VLANów (10.10.x.0/24) prowadzą przez Switch L3
- **Default Route (`0.0.0.0/0`)** – Cały nieznany ruch kierujemy do Switch L3
- **Metric 1** – Dystans administracyjny (im niższy, tym priorytet wyższy)

---

### Krok 6: Utworzenie ACL (Access Control Lists)

#### ACL dla ruchu Inside → Outside

    access-list INSIDE_OUT extended permit ip any any
    access-list INSIDE_OUT extended permit udp any any eq bootps
    access-list INSIDE_OUT extended permit udp any any eq bootpc

**Wyjaśnienie:**
- **`permit ip any any`** – Zezwól na cały ruch IP z Inside do Outside
- **`permit udp ... eq bootps`** – Zezwól na DHCP Server (port 67)
- **`permit udp ... eq bootpc`** – Zezwól na DHCP Client (port 68)
- W praktyce linia 1 wystarcza, ale linie 2-3 są explicit dla DHCP

---

#### ACL dla ruchu Outside → Inside

    access-list OUTSIDE_IN extended permit ip any any
    access-list OUTSIDE_IN extended permit udp any any eq bootps
    access-list OUTSIDE_IN extended permit udp any any eq bootpc

**Wyjaśnienie:**
- **Uwaga:** `permit ip any any` to **bardzo permisywna** reguła!
- W produkcji powinieneś **zawęzić** ACL:
  - Zezwalaj tylko na konkretne źródła (VLANy)
  - Zezwalaj tylko na konkretne destynacje (serwery)
  - Przykład: `permit ip 10.10.10.0 0.0.0.255 10.40.10.0 0.0.0.255`

---

### Krok 7: Przypisanie ACL do interfejsów

    access-group INSIDE_OUT in interface inside
    access-group OUTSIDE_IN in interface outside

**Wyjaśnienie:**
- **`access-group <ACL_name> in interface <interface>`** – Stosuje ACL na interfejsie
- **`in`** – Reguły stosowane do ruchu **wchodzącego** na interfejs
- ASA sprawdza ACL dla każdego pakietu:
  1. Pakiet przychodzi na interfejs
  2. ASA sprawdza ACL `in` dla tego interfejsu
  3. Jeśli **permit** – pakiet przechodzi
  4. Jeśli **deny** (domyślnie na końcu listy) – pakiet jest odrzucany

---

### Krok 8: Konfiguracja inspekcji protokołów (Stateful Firewall)

    class-map inspection_default
     match default-inspection-traffic
     exit

    policy-map global_policy
     class inspection_default
      inspect dns
      inspect ftp
      inspect icmp
      inspect tftp
     exit

    service-policy global_policy global

**Wyjaśnienie:**
- **Stateful Inspection** – ASA śledzi stan połączeń (TCP handshake, sesje)
- **`inspect dns`** – Inspekcja DNS (blokuje złośliwe zapytania)
- **`inspect icmp`** – Zezwala na ping (ale tylko dla istniejących sesji)
- **`inspect ftp`** – Dynamiczne otwieranie portów dla FTP data channel
- **`service-policy global_policy global`** – Stosuje politykę globalnie

---

### Krok 9: Zapisanie konfiguracji

    write memory

**lub**

    copy running-config startup-config

---

## ✅ Weryfikacja konfiguracji

### Sprawdzenie statusu interfejsów

    show interface ip brief

**Oczekiwany output:**

    Interface                  IP-Address      OK? Method Status                Protocol
    GigabitEthernet1/1         10.40.10.1      YES manual up                    up
    GigabitEthernet1/2         10.30.40.2      YES manual up                    up

**Sprawdź:**
- ✅ Oba interfejsy są **up/up**
- ✅ IP są poprawne

---

### Sprawdzenie tablicy routingu

    show route

**Oczekiwany output:**

    S    10.10.10.0 255.255.255.0 [1/0] via 10.30.40.1, outside
    S    10.10.20.0 255.255.255.0 [1/0] via 10.30.40.1, outside
    S    10.10.30.0 255.255.255.0 [1/0] via 10.30.40.1, outside
    S*   0.0.0.0 0.0.0.0 [1/0] via 10.30.40.1, outside
    C    10.40.10.0 255.255.255.0 is directly connected, inside
    C    10.30.40.0 255.255.255.0 is directly connected, outside

**Sprawdź:**
- ✅ Static routes (`S`) do VLANów
- ✅ Default route (`S*`)
- ✅ Connected routes (`C`)

---

### Sprawdzenie ACL

    show access-list

**Oczekiwany output:**

    access-list INSIDE_OUT; 3 elements
    access-list INSIDE_OUT line 1 extended permit ip any any (hitcnt=0)
    access-list INSIDE_OUT line 2 extended permit udp any any eq bootps (hitcnt=0)
    access-list INSIDE_OUT line 3 extended permit udp any any eq bootpc (hitcnt=0)

**Sprawdź:**
- ✅ ACL są widoczne
- **`hitcnt`** – Licznik trafień (ile pakietów pasowało do reguły)

---

### Test łączności z ASA

**Ping do Switch L3:**

    ping 10.30.40.1

**Ping do serwera DHCP:**

    ping 10.40.10.254

**Oczekiwany rezultat:**
- ✅ **Sukces** – ASA może komunikować się z obiema strefami

---

### Test ruchu przez firewall (z laptopa w VLANie)

**Na Laptop0 (VLAN 10) pinguj serwer DNS:**

    ping 10.40.10.253

**Oczekiwany rezultat:**
- ✅ **Sukces** – Ruch przechodzi przez ASA (Outside → Inside)
- Jeśli **timeout** – Sprawdź ACL `OUTSIDE_IN`

---

### Sprawdzenie aktywnych połączeń (Connection Table)

    show conn

**Wyjaśnienie:**
- Pokazuje **aktywne sesje** przechodząc przez firewall
- Przykład: `TCP outside:10.10.10.11 inside:10.40.10.253`
- Użyteczne do debugowania problemów z łącznością

---

## 🔒 Zalecenia bezpieczeństwa (Production Best Practices)

### 1. Zawęź ACL Outside → Inside

**Zamiast:**

    access-list OUTSIDE_IN extended permit ip any any

**Użyj:**

    access-list OUTSIDE_IN extended permit ip 10.10.10.0 255.255.255.0 host 10.40.10.254
    access-list OUTSIDE_IN extended permit ip 10.10.20.0 255.255.255.0 host 10.40.10.254
    access-list OUTSIDE_IN extended permit ip 10.10.30.0 255.255.255.0 host 10.40.10.254
    access-list OUTSIDE_IN extended permit udp any any eq bootps
    access-list OUTSIDE_IN extended permit udp any any eq bootpc

**Wyjaśnienie:**
- Zezwalaj tylko VLANom na dostęp do konkretnych serwerów
- Blokuj cały inny ruch (default deny)

---

### 2. Dodaj logowanie podejrzanych zdarzeń

    access-list OUTSIDE_IN extended deny ip any any log

**Wyjaśnienie:**
- Umieść jako **ostatnią regułę** (przed implicit deny)
- Loguje pakiety odrzucone przez firewall
- Sprawdzaj logi: `show logging`

---

### 3. Ustaw hasła

    enable password <hasło>
    username admin password <hasło> privilege 15

---

### 4. Włącz SSH (zamiast Telnet)

    crypto key generate rsa modulus 2048
    ssh 10.40.10.0 255.255.255.0 inside
    ssh timeout 30

---

## 🔍 Rozwiązywanie problemów (Troubleshooting)

### Problem: Laptopy w VLANach nie mogą pingować serwerów

**Możliwe przyczyny:**
1. ACL `OUTSIDE_IN` blokuje ruch → Sprawdź `show access-list`
2. Brak trasy zwrotnej – Serwery nie wiedzą jak wrócić do VLANów
3. Security Level blokuje ruch (ale nie w tym przypadku – Outside→Inside wymaga ACL)

**Rozwiązanie:**
- Sprawdź czy ACL zezwala na ruch: `access-list OUTSIDE_IN ... permit ip ...`
- Sprawdź tablicę routingu na serwerach (Default Gateway powinien wskazywać na ASA)

---

### Problem: DHCP nie działa przez firewall

**Możliwa przyczyna:**
- ACL nie zezwala na porty DHCP (67, 68)

**Rozwiązanie:**
- Dodaj explicit permit dla DHCP:
  
      access-list OUTSIDE_IN extended permit udp any any eq bootps
      access-list OUTSIDE_IN extended permit udp any any eq bootpc

---

## 🎯 Podsumowanie – Co osiągnęliśmy?

✅ **Strefy bezpieczeństwa** – Separacja serwerów (Inside) od VLANów (Outside)  
✅ **Security Levels** – Automatyczna kontrola kierunku ruchu  
✅ **ACL** – Precyzyjna kontrola dostępu między strefami  
✅ **Routing statyczny** – ASA zna ścieżki do wszystkich sieci  
✅ **Stateful Inspection** – Firewall śledzi stan połączeń (bezpieczniejsze niż stateless)  
✅ **Obsługa DHCP** – Ruch DHCP przechodzi przez firewall  

ASA Firewall pełni rolę **bramy bezpieczeństwa**, chroniąc krytyczne serwery przed nieautoryzowanym dostępem!

---

**Autor:** Sebastian Ciborowski  
**Data utworzenia:** 27.01.2026  
**Projekt:** [Enterprise Multi-Site Network](../)
