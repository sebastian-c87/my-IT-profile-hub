# 📋 Konfiguracje urządzeń / Device Configurations

Ten folder zawiera **surowe konfiguracje** (output z `show running-config`) wszystkich urządzeń sieciowych w projekcie.

---

## 📂 Zawartość folderu

| Plik | Urządzenie | Opis |
|------|------------|------|
| `SwitchL3-InterVLAN.txt` | Switch 3560-24PS (L3) | Inter-VLAN Routing, OSPF, DHCP Relay |
| `Switch0.txt` | Switch 2960-24TT | Trunk + Access Ports (VLANy) |
| `Switch1.txt` | Switch 2960-24TT | Access Ports dla VLANów 10/20/30 |
| `Router0.txt` | Router 2811 | OSPF Area 0, połączenia WAN |
| `Router1.txt` | Router 2811 | OSPF Area 0, połączenia WAN |
| `Router2.txt` | Router 2811 | OSPF Area 0, połączenia WAN |
| `Firewall-ASA.txt` | ASA 5506-X | Firewall z ACL, strefy Inside/Outside |

---

## 🎯 Jak używać tych plików?

Te pliki służą jako **backup** konfiguracji oraz jako **referencyjna dokumentacja** dla rekruterów technicznych, którzy chcą zobaczyć surowy kod konfiguracyjny.

**Jeśli szukasz instrukcji krok-po-kroku**, przejdź do folderu:  
👉 **[Config-Guides](../Config-Guides/)** – Szczegółowe przewodniki konfiguracyjne z wyjaśnieniami.

---

## 🔍 Kluczowe elementy konfiguracyjne

### Switch L3
- **Inter-VLAN Routing** (SVI dla VLAN 10/20/30)
- **DHCP Relay** (`ip helper-address 10.40.10.254`)
- **OSPF** (propagacja tras VLANów)
- **Static Routes** do ASA i routerów

### Switche Access (L2)
- **Trunk Ports** (802.1Q do Switch L3)
- **Access Ports** przypisane do VLANów 10, 20, 30

### Routery OSPF
- **Area 0 (Backbone)** między 3 routerami
- **WAN Links** (połączenia point-to-point)
- **LAN Interfaces** dla lokalnych hostów

### ASA Firewall
- **Strefy bezpieczeństwa** (Inside: 100, Outside: 0)
- **ACL** (ruch inside → outside, outside → inside)
- **Static Routes** do VLANów przez Switch L3

---

**💡 Wskazówka:** Możesz skopiować fragmenty tych konfiguracji bezpośrednio do CLI Packet Tracera lub rzeczywistego sprzętu Cisco.
