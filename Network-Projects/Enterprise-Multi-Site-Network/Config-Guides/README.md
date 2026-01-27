# 🛠️ Przewodniki konfiguracyjne / Configuration Guides

Ten folder zawiera **szczegółowe instrukcje krok-po-kroku** do konfiguracji wszystkich urządzeń w projekcie **Enterprise Multi-Site Network**.

Każdy przewodnik zawiera:
- 🎯 Cel konfiguracji
- 📋 Wymagania wstępne
- ⚙️ Komendy krok po kroku z wyjaśnieniami
- ✅ Procedury weryfikacji

---

## 📚 Dostępne przewodniki

<div align="center">

[![Switch L3 Config](https://img.shields.io/badge/01-Switch_L3_Configuration-0056D2?style=for-the-badge&logo=cisco&logoColor=white)](./01-SwitchL3-Configuration-Guide.md)

[![Switch Access Config](https://img.shields.io/badge/02-Switch_L2_Configuration-00BFFF?style=for-the-badge&logo=cisco&logoColor=white)](./02-Switch-Access-Configuration-Guide.md)

[![OSPF Routers Config](https://img.shields.io/badge/03-OSPF_Routers_Configuration-FF6B35?style=for-the-badge&logo=cisco&logoColor=white)](./03-OSPF-Routers-Configuration-Guide.md)

[![ASA Firewall Config](https://img.shields.io/badge/04-ASA_Firewall_Configuration-D32F2F?style=for-the-badge&logo=cisco&logoColor=white)](./04-ASA-Firewall-Configuration-Guide.md)

</div>

---

## 🔄 Zalecana kolejność konfiguracji

1. **Switch L3** – Fundament (VLANy, SVI, Routing)
2. **Switche Access (L2)** – Trunk i przypisanie portów do VLANów
3. **Routery OSPF** – Dynamiczny routing w WAN
4. **ASA Firewall** – Bezpieczeństwo i kontrola dostępu

---

## 📖 Dla kogo są te przewodniki?

- ✅ Rekruterzy techniczni oceniający umiejętności
- ✅ Inżynierowie chcący odtworzyć projekt
- ✅ Studenci uczący się konfiguracji Cisco
- ✅ Ja sam – jako dokumentacja moich projektów

---

**💡 Wskazówka:** Jeśli potrzebujesz surowych konfiguracji (output z `show run`), sprawdź folder:  
👉 **[configs](../configs/)** – RAW pliki tekstowe z urządzeń.
