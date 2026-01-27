# 🔷 Switch L3 – Konfiguracja Inter-VLAN Routing

## 🎯 Cel konfiguracji

Skonfigurowanie Switch Layer 3 jako **centralnego punktu routingu** w sieci:
- ✅ Utworzenie VLANów dla departamentów (Sprzedaż, Finanse, IT)
- ✅ Konfiguracja SVI (Switched Virtual Interfaces) jako gateway dla każdego VLANu
- ✅ Wdrożenie **DHCP Relay** (IP Helper) do przekazywania żądań DHCP do serwera
- ✅ Konfiguracja **OSPF** dla propagacji tras VLANów do routerów WAN
- ✅ Routing statyczny do ASA Firewall (strefa serwerowa)

---

## 📋 Wymagania wstępne

| Wymaganie | Szczegóły |
|-----------|-----------|
| **Model switcha** | Cisco 3560-24PS (Layer 3 capable) |
| **Połączenia trunk** | Fa0/1, Fa0/2 do Switchy Access (802.1Q) |
| **Połączenie do OSPF** | Fa0/24 do Router0 (`10.50.10.0/24`) |
| **Połączenie do ASA** | Fa0/20 do ASA Inside (`10.30.40.0/24`) |
| **Serwer DHCP** | `10.40.10.254` (dostępny przez ASA) |

---

## ⚙️ Konfiguracja krok po kroku

### Krok 1: Wejście w tryb konfiguracyjny

    enable
    configure terminal
    hostname SwitchL3-Core

**Wyjaśnienie:**
- `enable` – Przejście do trybu uprzywilejowanego (privileged EXEC mode)
- `configure terminal` – Wejście w tryb konfiguracji globalnej
- `hostname` – Zmiana nazwy urządzenia (ułatwia identyfikację)

---

### Krok 2: Utworzenie VLANów

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
- Tworzymy 3 VLANy odpowiadające departamentom firmy
- Nazwy VLANów (`name`) są opcjonalne, ale ułatwiają zarządzanie
- Każdy VLAN to osobna domena broadcast

---

### Krok 3: Konfiguracja SVI (Gateway dla VLANów)

    interface Vlan10
     ip address 10.10.10.1 255.255.255.0
     ip helper-address 10.40.10.254
     no shutdown
     exit

    interface Vlan20
     ip address 10.10.20.1 255.255.255.0
     ip helper-address 10.40.10.254
     no shutdown
     exit

    interface Vlan30
     ip address 10.10.30.1 255.255.255.0
     ip helper-address 10.40.10.254
     no shutdown
     exit

**Wyjaśnienie:**
- **SVI (Switched Virtual Interface)** to wirtualny interfejs L3 dla każdego VLANu
- Działa jako **Default Gateway** dla hostów w danym VLANie
- **`ip helper-address 10.40.10.254`** – Kluczowa komenda!
  - Przekazuje broadcasty DHCP DISCOVER z VLANu do serwera DHCP jako unicast
  - Bez tego hosty nie otrzymałyby IP automatycznie (DHCP działa na broadcastach, które nie przechodzą przez routery)
- **`no shutdown`** – Aktywacja interfejsu (domyślnie SVI są wyłączone)

---

### Krok 4: Włączenie routingu IP

    ip routing

**Wyjaśnienie:**
- **Kluczowa komenda** – bez niej switch działa tylko w L2!
- Umożliwia routowanie pakietów między VLANami i sieciami WAN
- Switch staje się routerem (Inter-VLAN Routing)

---

### Krok 5: Konfiguracja portów trunk do switchy Access

    interface FastEthernet0/1
     switchport trunk encapsulation dot1q
     switchport mode trunk
     no shutdown
     exit

    interface FastEthernet0/2
     switchport trunk encapsulation dot1q
     switchport mode trunk
     no shutdown
     exit

**Wyjaśnienie:**
- **Trunk** – Port który przesyła ruch **wszystkich VLANów** (tagged)
- **dot1q (802.1Q)** – Standard taggowania VLANów (dodaje 4-bajtowy tag do ramki)
- Fa0/1 i Fa0/2 łączą się ze switchami Access (Switch0 i Switch1)
- Switch Access rozdziela ruch do odpowiednich portów dostępowych

---

### Krok 6: Konfiguracja połączenia do Router0 (OSPF)

    interface FastEthernet0/24
     no switchport
     ip address 10.50.10.1 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- **`no switchport`** – Konwertuje port L2 na port L3 (routed port)
- Teraz port działa jak interfejs na routerze (można przypisać IP)
- `10.50.10.1` – Adres do komunikacji z Router0 (`10.50.10.2`)

---

### Krok 7: Konfiguracja połączenia do ASA Firewall

    interface FastEthernet0/20
     no switchport
     ip address 10.30.40.1 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- Połączenie do **Outside** interface ASA (`10.30.40.2`)
- Cały ruch do strefy serwerowej (`10.40.10.0/24`) przechodzi przez ASA

---

### Krok 8: Konfiguracja OSPF

    router ospf 1
     network 10.10.10.0 0.0.0.255 area 0
     network 10.10.20.0 0.0.0.255 area 0
     network 10.10.30.0 0.0.0.255 area 0
     network 10.50.10.0 0.0.0.255 area 0
     exit

**Wyjaśnienie:**
- **Process ID 1** – Lokalny identyfikator OSPF (musi być taki sam na wszystkich routerach w domenie)
- **`network ... area 0`** – Ogłaszamy sieci VLANów i link do Router0 w OSPF
- **Area 0 (Backbone)** – Główna strefa OSPF, do której łączą się inne obszary
- Dzięki temu routery WAN wiedzą, jak dotrzeć do VLANów

---

### Krok 9: Routing statyczny (trasy do sieci WAN i ASA)

    ip route 10.1.10.0 255.255.255.0 10.50.10.2
    ip route 10.1.20.0 255.255.255.0 10.50.10.2
    ip route 10.50.20.0 255.255.255.0 10.50.10.2
    ip route 172.16.0.0 255.255.255.0 10.50.10.2
    ip route 10.40.10.0 255.255.255.0 10.30.40.2
    ip route 0.0.0.0 0.0.0.0 10.30.40.2

**Wyjaśnienie:**
- **Static Routes** – Ręcznie definiujemy ścieżki do sieci, które nie są ogłaszane przez OSPF
- `10.50.10.2` (Router0) – Next hop dla sieci WAN
- `10.30.40.2` (ASA) – Next hop dla strefy serwerowej (`10.40.10.0/24`)
- **Default Route (`0.0.0.0/0`)** – Cały nieznany ruch kierujemy do ASA (firewall decyduje dalej)

---

### Krok 10: Zapisanie konfiguracji

    end
    write memory

**Wyjaśnienie:**
- `write memory` – Zapisuje konfigurację do NVRAM (przetrwa restart)
- Bez tego – po restarcie urządzenie wróci do poprzedniej konfiguracji

---

## ✅ Weryfikacja konfiguracji

### Sprawdzenie SVI i ich statusu

    show ip interface brief

**Oczekiwany output:**

    Interface              IP-Address      OK? Method Status                Protocol 
    Vlan10                 10.10.10.1      YES manual up                    up
    Vlan20                 10.10.20.1      YES manual up                    up
    Vlan30                 10.10.30.1      YES manual up                    up
    FastEthernet0/20       10.30.40.1      YES manual up                    up
    FastEthernet0/24       10.50.10.1      YES manual up                    up

---

### Sprawdzenie tablicy routingu

    show ip route

**Sprawdź czy widać:**
- ✅ Sieci VLANów (`C` – Connected)
- ✅ Trasy OSPF (`O` – OSPF Routes)
- ✅ Static Routes (`S`)
- ✅ Default Route (`S* 0.0.0.0/0`)

---

### Sprawdzenie sąsiadów OSPF

    show ip ospf neighbor

**Oczekiwany output:**
- Powinien pokazać Router0 jako sąsiada w stanie **FULL/DR** lub **FULL/BDR**

---

### Test łączności

    ping 10.40.10.254
    ping 10.50.10.2

**Oczekiwany rezultat:**
- ✅ Ping do serwera DHCP (`10.40.10.254`) – Sukces (przez ASA)
- ✅ Ping do Router0 (`10.50.10.2`) – Sukces

---

## 🎯 Podsumowanie – Co osiągnęliśmy?

✅ **Inter-VLAN Routing** – Hosty z różnych VLANów mogą się komunikować  
✅ **DHCP Relay** – Laptopy automatycznie otrzymują IP z centralnego serwera  
✅ **OSPF** – Dynamiczna propagacja tras do routerów WAN  
✅ **Routing statyczny** – Dostęp do strefy serwerowej przez ASA  
✅ **Default Route** – Cały nieznany ruch kierowany do firewalla  

Switch L3 jest teraz **rdzeniem sieci** (Core Layer), łączącym wszystkie strefy!

---

**Autor:** Sebastian Ciborowski  
**Data utworzenia:** 27.01.2026  
**Projekt:** [Enterprise Multi-Site Network](../)
