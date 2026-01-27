# 🔴 Routery OSPF – Konfiguracja Dynamicznego Routingu WAN

## 🎯 Cel konfiguracji

Skonfigurowanie 3 routerów w topologii WAN z dynamicznym routingiem OSPF:
- ✅ Utworzenie połączeń **point-to-point** między routerami (WAN links)
- ✅ Konfiguracja **OSPF Area 0** (Backbone) dla wymiany tras
- ✅ Propagacja sieci lokalnych (LAN) do całej domeny OSPF
- ✅ Zapewnienie redundancji i automatycznego failover (jeśli link padnie, OSPF wybiera alternatywną ścieżkę)

---

## 📋 Wymagania wstępne

| Wymaganie | Szczegóły |
|-----------|-----------|
| **Model routerów** | Cisco 2811 (3 sztuki) |
| **Topologia** | Partial Mesh (każdy router połączony z dwoma innymi) |
| **Protokół routingu** | OSPF (Open Shortest Path First) |
| **OSPF Area** | Area 0 (Backbone) |
| **Połączenie do Core** | Router0 → Switch L3 (`10.50.10.0/24`) |

---

## 🔍 Architektura połączeń

### Router0 (Główny – połączenie do Switch L3)
- **Fa0/0:** `10.50.10.2/24` → Switch L3 (10.50.10.1)
- **Fa1/0:** `172.16.0.1/24` → Router1 (172.16.0.2)
- **Fa1/1:** `192.168.10.1/24` → Router2 (192.168.10.2) + LAN lokalny

### Router1 (Węzeł pośredni)
- **Fa0/0:** `10.50.20.1/24` → LAN lokalny (switche + hosty)
- **Fa0/1:** `172.16.10.2/24` → Router2 (172.16.10.1)
- **Fa1/0:** `172.16.0.2/24` → Router0 (172.16.0.1)

### Router2 (Węzeł pośredni)
- **Fa0/0:** `10.50.30.1/24` → LAN lokalny (switche + hosty)
- **Fa0/1:** `172.16.10.1/24` → Router1 (172.16.10.2)
- **Fa1/1:** `192.168.10.2/24` → Router0 (192.168.10.1)

---

## ⚙️ Konfiguracja krok po kroku

## 🟦 Router0 – Główny router (połączenie do Core)

### Krok 1: Wejście w tryb konfiguracyjny

    enable
    configure terminal
    hostname Router0

---

### Krok 2: Konfiguracja interfejsu do Switch L3 (Core)

    interface FastEthernet0/0
     ip address 10.50.10.2 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- Połączenie do **Switch L3** (rdzeń sieci VLANów)
- Dzięki temu Router0 może propagować trasy VLANów do innych routerów WAN

---

### Krok 3: Konfiguracja linku WAN do Router1

    interface FastEthernet1/0
     ip address 172.16.0.1 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- Link point-to-point z Router1 (172.16.0.2)
- Sieć `/24` dla łatwości (w produkcji używa się `/30` dla 2 hostów)

---

### Krok 4: Konfiguracja linku WAN do Router2 + LAN

    interface FastEthernet1/1
     ip address 192.168.10.1 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- Ten interfejs pełni podwójną rolę:
  - Link do Router2 (192.168.10.2)
  - Gateway dla lokalnych hostów (switche/laptopy)

---

### Krok 5: Konfiguracja OSPF

    router ospf 1
     network 10.50.10.0 0.0.0.255 area 0
     network 172.16.0.0 0.0.0.255 area 0
     network 192.168.10.0 0.0.0.255 area 0
     network 10.10.10.0 0.0.0.255 area 0
     network 10.10.20.0 0.0.0.255 area 0
     network 10.10.30.0 0.0.0.255 area 0
     exit

**Wyjaśnienie:**
- **Process ID 1** – Lokalny identyfikator OSPF (musi być taki sam na wszystkich routerach)
- **`network ... area 0`** – Ogłaszamy sieci w OSPF Area 0:
  - `10.50.10.0` – Link do Switch L3
  - `172.16.0.0`, `192.168.10.0` – Linki WAN
  - `10.10.x.0` – Sieci VLANów (propagowane z Switch L3)
- **Wildcard mask** (`0.0.0.255`) = odwrotność subnet mask

---

### Krok 6: Zapisanie konfiguracji

    end
    write memory

---

## 🟩 Router1 – Węzeł pośredni

### Krok 1: Wejście w tryb konfiguracyjny

    enable
    configure terminal
    hostname Router1

---

### Krok 2: Konfiguracja interfejsu LAN

    interface FastEthernet0/0
     ip address 10.50.20.1 255.255.255.0
     no shutdown
     exit

**Wyjaśnienie:**
- Gateway dla lokalnej sieci (hosty w lokalizacji Router1)

---

### Krok 3: Konfiguracja linku WAN do Router2

    interface FastEthernet0/1
     ip address 172.16.10.2 255.255.255.0
     no shutdown
     exit

---

### Krok 4: Konfiguracja linku WAN do Router0

    interface FastEthernet1/0
     ip address 172.16.0.2 255.255.255.0
     no shutdown
     exit

---

### Krok 5: Konfiguracja OSPF

    router ospf 1
     network 10.50.20.0 0.0.0.255 area 0
     network 172.16.0.0 0.0.0.255 area 0
     network 172.16.10.0 0.0.0.255 area 0
     exit

**Wyjaśnienie:**
- Ogłaszamy 3 sieci:
  - `10.50.20.0` – LAN lokalny
  - `172.16.0.0`, `172.16.10.0` – Linki WAN

---

### Krok 6: Zapisanie konfiguracji

    end
    write memory

---

## 🟧 Router2 – Węzeł pośredni

### Krok 1: Wejście w tryb konfiguracyjny

    enable
    configure terminal
    hostname Router2

---

### Krok 2: Konfiguracja interfejsu LAN

    interface FastEthernet0/0
     ip address 10.50.30.1 255.255.255.0
     no shutdown
     exit

---

### Krok 3: Konfiguracja linku WAN do Router1

    interface FastEthernet0/1
     ip address 172.16.10.1 255.255.255.0
     no shutdown
     exit

---

### Krok 4: Konfiguracja linku WAN do Router0

    interface FastEthernet1/1
     ip address 192.168.10.2 255.255.255.0
     no shutdown
     exit

---

### Krok 5: Konfiguracja OSPF

    router ospf 1
     network 10.50.30.0 0.0.0.255 area 0
     network 192.168.10.0 0.0.0.255 area 0
     network 172.16.10.0 0.0.0.255 area 0
     exit

**Wyjaśnienie:**
- Ogłaszamy 3 sieci:
  - `10.50.30.0` – LAN lokalny
  - `192.168.10.0`, `172.16.10.0` – Linki WAN

---

### Krok 6: Zapisanie konfiguracji

    end
    write memory

---

## ✅ Weryfikacja konfiguracji

### Sprawdzenie sąsiadów OSPF (na każdym routerze)

    show ip ospf neighbor

**Oczekiwany output (Router0):**

    Neighbor ID     Pri   State           Dead Time   Address         Interface
    172.16.0.2      1     FULL/DR         00:00:35    172.16.0.2      FastEthernet1/0
    192.168.10.2    1     FULL/DR         00:00:38    192.168.10.2    FastEthernet1/1

**Sprawdź:**
- ✅ Stan: **FULL** (pełna synchronizacja)
- ✅ Widoczni wszyscy sąsiedzi (Router0 widzi Router1 i Router2)

---

### Sprawdzenie tablicy routingu (na każdym routerze)

    show ip route ospf

**Oczekiwany output (Router1):**

    O    10.50.10.0/24 [110/2] via 172.16.0.1, 00:05:23, FastEthernet1/0
    O    10.50.30.0/24 [110/2] via 172.16.10.1, 00:05:23, FastEthernet0/1
    O    192.168.10.0/24 [110/2] via 172.16.0.1, 00:05:23, FastEthernet1/0

**Sprawdź:**
- ✅ Widoczne są sieci **innych routerów** (oznaczone literą `O`)
- ✅ Metryka OSPF (`[110/2]`) – im mniejsza, tym lepsza trasa
- ✅ Next Hop – adres IP sąsiedniego routera

---

### Sprawdzenie pełnej tablicy routingu

    show ip route

**Sprawdź obecność:**
- `C` – **Connected** (sieci bezpośrednio podłączone)
- `O` – **OSPF** (trasy nauczone dynamicznie)
- `S` – **Static** (trasy statyczne, jeśli są)

---

### Test łączności między routerami

**Z Router1 pinguj Router2:**

    ping 172.16.10.1

**Z Router1 pinguj Switch L3 (przez Router0):**

    ping 10.50.10.1

**Oczekiwany rezultat:**
- ✅ **Sukces** – Routery mogą się komunikować

---

### Test redundancji (symulacja awarii linku)

**Na Router0 wyłącz interfejs do Router1:**

    configure terminal
    interface FastEthernet1/0
     shutdown
     exit
    end

**Sprawdź tablicę routingu:**

    show ip route ospf

**Oczekiwany rezultat:**
- ✅ OSPF **automatycznie** wybiera alternatywną ścieżkę przez Router2
- ✅ Tablica routingu się zaktualizowała (czas konwergencji: 5-10 sekund)

**Przywróć interfejs:**

    configure terminal
    interface FastEthernet1/0
     no shutdown
     exit

---

## 🔍 Rozwiązywanie problemów (Troubleshooting)

### Problem: Sąsiedzi OSPF nie pojawiają się (State: DOWN)

**Możliwe przyczyny:**
1. Interfejsy są wyłączone (`shutdown`) → `no shutdown`
2. Błędna konfiguracja `network` → Sprawdź wildcard mask
3. OSPF Process ID różni się (nie musi być taki sam, ale obszar Area musi!)
4. Problem z fizyczną łącznością → `show ip interface brief`

**Rozwiązanie:**
- Sprawdź czy interfejsy są **up/up**: `show ip interface brief`
- Sprawdź timery OSPF: `show ip ospf interface`

---

### Problem: Trasy OSPF nie pojawiają się w tablicy routingu

**Możliwe przyczyny:**
1. OSPF nie został włączony na danym interfejsie → Dodaj `network` statement
2. Area mismatch (router ogłasza w Area 1, a sąsiad w Area 0)

**Rozwiązanie:**
- Sprawdź które interfejsy są w OSPF: `show ip ospf interface`
- Upewnij się, że wszystkie routery są w **Area 0**

---

## 🎯 Podsumowanie – Co osiągnęliśmy?

✅ **OSPF Area 0** – Dynamiczny routing między 3 routerami  
✅ **Automatyczna propagacja tras** – Każdy router zna ścieżki do wszystkich sieci  
✅ **Redundancja** – Jeśli jeden link padnie, OSPF wybiera backup  
✅ **Skalowalność** – Dodanie nowego routera wymaga tylko konfiguracji OSPF (reszta automatyczna)  
✅ **Load Balancing** – OSPF może korzystać z równoległych ścieżek o tej samej metryce  

Routery tworzą teraz **stabilną sieć WAN** (Distribution Layer), łączącą oddziały firmy!

---

**Autor:** Sebastian Ciborowski  
**Data utworzenia:** 27.01.2026  
**Projekt:** [Enterprise Multi-Site Network](../)
