# 🔶 Switche Access – Konfiguracja Trunk i VLANów

## 🎯 Cel konfiguracji

Skonfigurowanie switchy Layer 2 (Access Layer) do obsługi ruchu VLANowego:
- ✅ Utworzenie VLANów lokalnie na switchach
- ✅ Konfiguracja **trunk ports** do Switch L3 (802.1Q tagging)
- ✅ Przypisanie **access ports** do odpowiednich VLANów (departamenty)
- ✅ Zapewnienie łączności hostów końcowych z gateway (Switch L3)

---

## 📋 Wymagania wstępne

| Wymaganie | Szczegóły |
|-----------|-----------|
| **Model switchy** | Cisco 2960-24TT (Layer 2, 24 porty Fast Ethernet) |
| **Liczba switchy** | 2 sztuki (Switch0, Switch1) |
| **Połączenia trunk** | Fa0/1 i G0/1 do Switch L3 (redundancja) |
| **Hosty** | Laptopy w VLANach 10, 20, 30 (po 2 laptopy per VLAN) |

---

## 🔍 Architektura połączeń

### Switch0 (Dolny)
- **Trunk:** Fa0/1, G0/1 → Switch L3
- **Access Ports:**
  - Fa0/2 → VLAN 10 (Laptop0)
  - Fa0/3 → VLAN 20 (Laptop1)
  - Fa0/4 → VLAN 30 (Laptop2)

### Switch1 (Górny)
- **Trunk:** Fa0/1, G0/1 → Switch L3
- **Access Ports:**
  - Fa0/2 → VLAN 10 (Laptop3)
  - Fa0/3 → VLAN 20 (Laptop4)
  - Fa0/4 → VLAN 30 (Laptop5)

---

## ⚙️ Konfiguracja krok po kroku

### Krok 1: Wejście w tryb konfiguracyjny

    enable
    configure terminal
    hostname Switch-Access-0

**Wyjaśnienie:**
- Zmieniamy hostname na `Switch-Access-0` (lub `Switch-Access-1` dla drugiego switcha)
- Ułatwia identyfikację urządzeń w sieci

---

### Krok 2: Utworzenie VLANów lokalnie

    vlan 10
     name Sprzedaz
     exit
    vlan 20
     name Finanse
     exit
    vlan 30
     name IT
     exit

**Wyjaśnienie:**
- **Ważne:** VLANy muszą być utworzone lokalnie na każdym switchu!
- Switch L2 **nie propaguje** VLANów automatycznie (w przeciwieństwie do VTP, którego tutaj nie używamy)
- Nazwy są opcjonalne, ale ułatwiają debugowanie (`show vlan brief`)

---

### Krok 3: Konfiguracja trunk ports (do Switch L3)

    interface FastEthernet0/1
     switchport mode trunk
     no shutdown
     exit

    interface GigabitEthernet0/1
     switchport mode trunk
     no shutdown
     exit

**Wyjaśnienie:**
- **Trunk port** = Port który przesyła ruch **wielu VLANów jednocześnie**
- Każda ramka (frame) jest **tagowana** 4-bajtowym nagłówkiem 802.1Q z numerem VLANu
- Switch L3 odbiera ramkę, czyta tag, i routuje do odpowiedniego SVI
- **Dlaczego dwa trunk porty?**
  - Redundancja – jeśli jeden kabel się uszkodzi, drugi przejmuje ruch
  - Spanning Tree Protocol (STP) blokuje jeden, aby uniknąć pętli

---

### Krok 4: Przypisanie access ports do VLANów

#### Switch0:

    interface FastEthernet0/2
     switchport mode access
     switchport access vlan 10
     no shutdown
     exit

    interface FastEthernet0/3
     switchport mode access
     switchport access vlan 20
     no shutdown
     exit

    interface FastEthernet0/4
     switchport mode access
     switchport access vlan 30
     no shutdown
     exit

#### Switch1 (analogicznie):

    interface FastEthernet0/2
     switchport mode access
     switchport access vlan 10
     no shutdown
     exit

    interface FastEthernet0/3
     switchport mode access
     switchport access vlan 20
     no shutdown
     exit

    interface FastEthernet0/4
     switchport mode access
     switchport access vlan 30
     no shutdown
     exit

**Wyjaśnienie:**
- **Access port** = Port który należy **tylko do jednego VLANu**
- Ramki wysyłane do hosta są **untagged** (host nie wie o istnieniu VLANów)
- `switchport mode access` – Ustawia port w tryb dostępowy (nie trunk)
- `switchport access vlan X` – Przypisuje port do VLANu X

---

### Krok 5: Zapisanie konfiguracji

    end
    write memory

**Wyjaśnienie:**
- Zapisujemy konfigurację do pamięci NVRAM
- Konfiguracja przetrwa restart switcha

---

## ✅ Weryfikacja konfiguracji

### Sprawdzenie VLANów i przypisania portów

    show vlan brief

**Oczekiwany output:**

    VLAN Name                             Status    Ports
    ---- -------------------------------- --------- -------------------------------
    1    default                          active    Fa0/5-Fa0/23
    10   Sprzedaz                         active    Fa0/2
    20   Finanse                          active    Fa0/3
    30   IT                               active    Fa0/4

**Sprawdź:**
- ✅ VLANy 10, 20, 30 są **active**
- ✅ Porty access są przypisane do właściwych VLANów
- ✅ Porty trunk (Fa0/1, G0/1) **nie powinny być widoczne** na liście (są w trybie trunk, nie access)

---

### Sprawdzenie statusu trunk portów

    show interfaces trunk

**Oczekiwany output:**

    Port        Mode         Encapsulation  Status        Native vlan
    Fa0/1       on           802.1q         trunking      1
    Gig0/1      on           802.1q         trunking      1

    Port        Vlans allowed on trunk
    Fa0/1       1-4094
    Gig0/1      1-4094

**Sprawdź:**
- ✅ Status: **trunking**
- ✅ Encapsulation: **802.1q**
- ✅ VLANs allowed: **1-4094** (wszystkie)

---

### Sprawdzenie statusu interfejsów

    show ip interface brief

**Oczekiwany output:**

    Interface              Status         Protocol
    FastEthernet0/1        up             up
    FastEthernet0/2        up             up
    GigabitEthernet0/1     up             up

**Sprawdź:**
- ✅ Wszystkie używane porty są **up/up**
- ✅ Nieużywane porty mogą być **down/down** (to normalne)

---

### Test łączności (z poziomu laptopa)

**Na Laptop0 (VLAN 10):**

    ipconfig

**Oczekiwany output:**
- IP Address: `10.10.10.11` (lub kolejny z puli DHCP)
- Subnet Mask: `255.255.255.0`
- Default Gateway: `10.10.10.1` (SVI na Switch L3)
- DNS Server: `10.40.10.253`

**Test ping:**

    ping 10.10.10.1

**Oczekiwany rezultat:**
- ✅ Ping do gateway (Switch L3) – **Sukces**

---

## 🔍 Rozwiązywanie problemów (Troubleshooting)

### Problem: Laptop nie otrzymuje IP przez DHCP

**Możliwe przyczyny:**
1. Port nie jest przypisany do właściwego VLANu → `show vlan brief`
2. Trunk port do Switch L3 jest down → `show interfaces trunk`
3. VLAN nie istnieje lokalnie → `show vlan brief` (jeśli VLAN nie istnieje, stwórz go)
4. DHCP Relay (IP Helper) nie jest skonfigurowany na Switch L3

**Rozwiązanie:**
- Sprawdź konfigurację Switch L3 (SVI + `ip helper-address`)
- Sprawdź czy serwer DHCP działa (`ping 10.40.10.254` z Switch L3)

---

### Problem: Laptop pinguje gateway, ale nie hosty w innych VLANach

**Możliwa przyczyna:**
- Switch L3 nie ma włączonego `ip routing`
- ACL na ASA blokuje ruch Inter-VLAN

**Rozwiązanie:**
- Na Switch L3: `show ip route` – Sprawdź czy widać sieci VLANów
- Jeśli brak, dodaj: `ip routing`

---

## 🎯 Podsumowanie – Co osiągnęliśmy?

✅ **VLANy utworzone** – Segmentacja sieci na departamenty  
✅ **Trunk ports** – Ruch wielu VLANów przez jedno łącze do Switch L3  
✅ **Access ports** – Hosty przypisane do właściwych VLANów  
✅ **Redundancja** – Dwa trunk linki (Fa0/1 + G0/1) jako backup  
✅ **Łączność** – Laptopy otrzymują IP przez DHCP i mogą komunikować się z gateway  

Switche Access pełnią rolę **warstwy dostępowej** (Access Layer), łącząc użytkowników końcowych z rdzeniem sieci!

---

**Autor:** Sebastian Ciborowski  
**Data utworzenia:** 27.01.2026  
**Projekt:** [Enterprise Multi-Site Network](../)
