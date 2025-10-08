"""
Legal Case Finder - Asystent Prawny
Główna aplikacja do analizy problemów prawnych

Aplikacja oparta o prawo obowiązujące w Polsce
Integracja z Systemem Analizy Orzeczeń Sądowych
Uses OpenAI Responses API (GPT-5) 

To nie jest porada prawna - zawsze kontaktuj się z ustalonym ekspertem!

# Author: Sebastian C.
# Repository: https://github.com/sebastian-c87/my-IT-profile-hub
"""

import os
import sys
import json
import logging
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import Dict, Any, List, Optional

from config import config
from openai_client import LegalAIClient
from saos_client import SAOSClient

# Konfiguracja logowania
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class LegalCaseFinderApp:
    """Główna aplikacja Legal Case Finder"""
    
    def __init__(self):
        self.ai_client = LegalAIClient(config)
        self.saos_client = SAOSClient()
        self.current_analysis: Optional[Dict[str, Any]] = None
        self.logger = logging.getLogger(__name__)
    
    def run(self):
        """Uruchom aplikację"""
        self._display_welcome()
        
        while True:
            try:
                choice = self._show_main_menu()
                
                if choice == "1":
                    self.analyze_legal_problem()
                elif choice == "2":
                    self.search_court_judgments()
                elif choice == "3":
                    self.download_analysis()
                elif choice == "4":
                    self.show_help_and_domains()
                elif choice == "5":
                    self._display_goodbye()
                    break
                else:
                    print("❌ Nieprawidłowa opcja. Wybierz 1-5.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Aplikacja zakończona przez użytkownika.")
                break
            except Exception as e:
                self.logger.error(f"Błąd aplikacji: {str(e)}")
                print(f"\n❌ Wystąpił błąd: {str(e)}")
                input("\nNaciśnij Enter aby kontynuować...")
    
    def _display_welcome(self):
        """Wyświetl ekran powitalny"""
        print("\n" + "="*70)
        print("⚖️  LEGAL CASE FINDER - ASYSTENT PRAWNY")
        print("Zasilany przez GPT-5-nano z wyszukiwaniem internetowym")
        print("="*70)
        print("\n✨ Witamy w profesjonalnym asystencie prawnym!")
        print("📚 Specjalizacja: Prawo polskie")
        print("🔍 Możliwości: Analiza problemów prawnych + orzeczenia SAOS")
        print("\n⚠️  WAŻNE: Aplikacja dostarcza informacji, NIE zastępuje prawnika!")
        print("="*70 + "\n")
    
    def _show_main_menu(self) -> str:
        """Pokaż menu główne - UPROSZCZONE"""
        print("\n" + "─"*70)
        print("🎯 MENU GŁÓWNE:")
        print("─"*70)
        print("1. 🔍 Analiza problemu prawnego")
        print("2. ⚖️  Przeglądaj orzeczenia sądowe (SAOS)")
        print("3. 💾 Pobierz analizę")
        print("4. ❓ Pomoc i informacje o dziedzinach prawa")
        print("5. 🚪 Zakończ")
        print("─"*70)
        
        return input("\n🔢 Wybierz opcję (1-5): ").strip()
    
    def analyze_legal_problem(self):
        """Główna funkcja analizy problemu prawnego"""
        print("\n" + "="*70)
        print("🔍 ANALIZA PROBLEMU PRAWNEGO")
        print("="*70)
        
        # Wybór dziedziny prawa
        legal_domain = self._select_legal_domain()
        if not legal_domain:
            return
        
        # Opis problemu - UPROSZCZONE (Enter kończy)
        print(f"\n📝 Wybrałeś dziedzinę: **{legal_domain}**")
        print("\n💬 Opisz swój problem prawny:")
        print("   (naciśnij Enter aby zakończyć opis)")
        print()
        
        problem_description = input("   > ").strip()
        
        if not problem_description:
            print("❌ Nie podano opisu problemu!")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        # Analiza - BEZ pytania o web search (zawsze włączony)
        print("\n⏳ Analizuję problem prawny...")
        print("🌐 Używam wyszukiwania internetowego...")
        print("🤖 To może potrwać kilkadziesiąt sekund...")
        
        result = self.ai_client.analyze_legal_problem(
            problem_description=problem_description,
            legal_domain=legal_domain
        )
        
        if result["success"]:
            print("\n" + "="*70)
            print("📊 ANALIZA PRAWNA:")
            print("="*70)
            print(result["analysis"])
            print("="*70)
            
            # Zapisz aktualną analizę do pobrania
            self.current_analysis = {
                "type": "legal_analysis",
                "legal_domain": legal_domain,
                "problem": problem_description,
                "analysis": result["analysis"],
                "timestamp": result["timestamp"]
            }
            
            print("\n✅ Analiza gotowa!")
            print("💡 Możesz ją teraz pobrać wybierając opcję '3. Pobierz analizę' z menu")
            
        else:
            print(f"\n❌ Błąd analizy: {result.get('error', 'Nieznany błąd')}")
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def _select_legal_domain(self) -> Optional[str]:
        """Wybór dziedziny prawa"""
        print("\n📚 Wybierz dziedzinę prawa:")
        print("─"*70)
        
        for idx, domain in enumerate(config.legal_domains, 1):
            print(f"  {idx}. {domain}")
        
        print("─"*70)
        
        try:
            choice = input(f"\n🔢 Wybierz (1-{len(config.legal_domains)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(config.legal_domains):
                return config.legal_domains[choice_idx]
            else:
                print("❌ Nieprawidłowy wybór!")
                return None
        except ValueError:
            print("❌ Wprowadź numer!")
            return None
    
    def search_court_judgments(self):
        """Wyszukaj orzeczenia w SAOS"""
        print("\n" + "="*70)
        print("⚖️  WYSZUKIWANIE ORZECZEŃ SĄDOWYCH")
        print("="*70)
        print("\n📚 System: SAOS (System Analizy Orzeczeń Sądowych)")
        print("🌐 Źródło: Ministerstwo Sprawiedliwości RP")
        
        print("\n🔎 Wprowadź słowa kluczowe do wyszukania:")
        query = input("   > ").strip()
        
        if not query:
            print("❌ Nie podano zapytania!")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        print("\n📊 Typ sądu (opcjonalnie):")
        print("  1. Wszystkie")
        print("  2. Sąd Najwyższy")
        print("  3. Sądy powszechne")
        print("  4. Sądy administracyjne")
        
        court_type_choice = input("\nWybór (1-4, Enter=1): ").strip() or "1"
        
        court_types = {
            "1": None,
            "2": "SUPREME",
            "3": "COMMON",
            "4": "ADMINISTRATIVE"
        }
        
        court_type = court_types.get(court_type_choice)
        
        print(f"\n⏳ Wyszukuję orzeczenia dla: {query}...")
        
        judgments = self.saos_client.search_judgments(
            query=query,
            page_size=5,
            court_type=court_type
        )
        
        if judgments:
            print(f"\n✅ Znaleziono {len(judgments)} orzeczeń:")
            
            for idx, judgment in enumerate(judgments, 1):
                print(f"\n{'─'*70}")
                print(f"ORZECZENIE #{idx}")
                print(self.saos_client.format_judgment_display(judgment))
            
            print("\n✅ Wyszukiwanie zakończone!")
        else:
            print("\n❌ Nie znaleziono orzeczeń pasujących do zapytania.")
            print("💡 Spróbuj użyć innych słów kluczowych.")
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def download_analysis(self):
        """Pobierz/zapisz ostatnią analizę"""
        print("\n" + "="*70)
        print("💾 POBIERANIE ANALIZY")
        print("="*70)
        
        if not self.current_analysis:
            print("\n❌ Brak analizy do pobrania!")
            print("💡 Najpierw wykonaj analizę problemu prawnego (opcja 1)")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        try:
            # Generuj nazwę pliku
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analiza_prawna_{timestamp}.txt"
            
            # Zapisz do pliku
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("ANALIZA PRAWNA - LEGAL CASE FINDER\n")
                f.write("="*70 + "\n\n")
                f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Dziedzina prawa: {self.current_analysis['legal_domain']}\n\n")
                f.write("PROBLEM:\n")
                f.write("-"*70 + "\n")
                f.write(self.current_analysis['problem'] + "\n\n")
                f.write("ANALIZA:\n")
                f.write("-"*70 + "\n")
                f.write(self.current_analysis['analysis'] + "\n\n")
                f.write("="*70 + "\n")
                f.write("Wygenerowano przez Legal Case Finder\n")
                f.write("PAMIĘTAJ: To nie jest porada prawna!\n")
                f.write("="*70 + "\n")
            
            print(f"\n✅ Analiza zapisana do pliku: {filename}")
            print(f"📂 Lokalizacja: {os.path.abspath(filename)}")
            
            # Opcja JSON
            save_json = input("\n💾 Zapisać również w formacie JSON? (T/n): ").strip().upper()
            if save_json != "N":
                json_filename = f"analiza_prawna_{timestamp}.json"
                with open(json_filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_analysis, f, indent=2, ensure_ascii=False)
                print(f"✅ Zapisano również: {json_filename}")
            
        except Exception as e:
            print(f"\n❌ Błąd zapisu: {str(e)}")
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def show_help_and_domains(self):
        """Pokaż pomoc i informacje o dziedzinach prawa """
        print("\n" + "="*70)
        print("❓ POMOC I INFORMACJE")
        print("="*70)
        
        # Instrukcja użytkowania
        print("\n📖 JAK KORZYSTAĆ Z APLIKACJI:")
        print("─"*70)
        print("""
1. **Wybierz opcję 1** - Analiza problemu prawnego
   • Wybierz dziedzinę prawa najbliższą Twojemu problemowi
   • Opisz szczegółowo swoją sytuację (zakończ Enter)
   • System automatycznie wyszuka przepisy i przedstawi analizę

2. **Wybierz opcję 2** - Przeglądaj orzeczenia SAOS
   • Wyszukaj podobne sprawy rozstrzygnięte przez polskie sądy
   • Podaj słowa kluczowe związane z Twoją sprawą
   • Otrzymasz oficjalne orzeczenia z systemu SAOS

3. **Wybierz opcję 3** - Pobierz analizę
   • Zapisz ostatnią analizę do pliku TXT lub JSON
   • Możesz przesłać plik swojemu prawnikowi

4. **Ta opcja** - Pomoc i informacje o dziedzinach prawa

5. **Zakończ** - Wyjście z aplikacji
""")
        
        print("\n⚠️  WAŻNE INFORMACJE:")
        print("─"*70)
        print("""
• Aplikacja NIE zastępuje profesjonalnej porady prawnej
• Zawsze konsultuj ważne sprawy z adwokatem/radcą prawnym
• Przepisy prawne mogą się zmieniać - weryfikuj aktualność
• System automatycznie używa wyszukiwania internetowego
• Opisuj problem szczegółowo i konkretnie
""")
        
        # Informacje o dziedzinach prawa
        print("\n📚 DZIEDZINY PRAWA - SZCZEGÓŁY:")
        print("="*70)
        
        domain_info = {
            "Prawo karne": "Przestępstwa, wykroczenia, odpowiedzialność karna, kary, postępowanie karne, ściganie",
            "Prawo cywilne": "Umowy, własność, zobowiązania, odszkodowania, roszczenia cywilne, dochodzenie roszczeń",
            "Prawo rodzinne": "Małżeństwo, rozwód, separacja, alimenty, władza rodzicielska, opieka nad dziećmi",
            "Prawo pracy": "Umowy o pracę, wynagrodzenie, urlopy, zwolnienia, mobbing, dyskryminacja w pracy",
            "Prawo spadkowe": "Spadki, testamenty, dziedziczenie ustawowe, zachowek, dział spadku, odrzucenie spadku",
            "Prawo gospodarcze": "Działalność gospodarcza, spółki, upadłość, restrukturyzacja, konkurencja",
            "Prawo administracyjne": "Decyzje administracyjne, samorząd, budownictwo, środowisko, skargi do sądów administracyjnych",
            "Prawo podatkowe": "Podatki (VAT, PIT, CIT), deklaracje, kontrole skarbowe, interpretacje podatkowe",
            "Prawo nieruchomości": "Kupno, sprzedaż, najem, dzierżawa, własność, księgi wieczyste, służebności",
            "Prawo konsumenckie": "Ochrona konsumentów, reklamacje, zwroty, umowy konsumenckie, nieuczciwe praktyki",
            "Prawo własności intelektualnej i AI": "Prawa autorskie, patenty, znaki towarowe, AI, ochrona danych, RODO, cyfryzacja"
        }
        
        for idx, domain in enumerate(config.legal_domains, 1):
            print(f"\n{idx}. **{domain}**")
            print(f"   {domain_info.get(domain, 'Opis niedostępny')}")
        
        print("\n" + "="*70)
        input("\nNaciśnij Enter aby powrócić do menu...")
    
    def _display_goodbye(self):
        """Wyświetl komunikat pożegnalny w OKNIE POPUP"""
    
        # Komunikat do popup
        popup_title = "Legal Case Finder - Polecana Pomoc Prawna"
        popup_message = f"""⚖️ DZIĘKUJEMY ZA KORZYSTANIE Z LEGAL CASE FINDER!

    ⚠️ PAMIĘTAJ:
    W ważnych sprawach prawnych zawsze skonsultuj się 
    z profesjonalnym prawnikiem!

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    💼 POLECANA POMOC PRAWNA:

    Mecenas {config.lawyer_name}
    📍 {config.lawyer_location}

    {config.lawyer_description}
    
    ✓ Profesjonalne doświadczenie w prawie polskim
    ✓ Indywidualne podejście do każdego klienta
    ✓ Skuteczna reprezentacja w sądach i urzędach

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Skontaktuj się z Kancelarią już dziś!

[KONTAKT - szczegóły zostaną dodane]

🌟 Do zobaczenia!"""
    
        # Pokaż popup
        try:
        # Utwórz niewidoczne główne okno tkinter
            root = tk.Tk()
            root.withdraw()  # Ukryj główne okno
        
            # KLUCZOWE: Wymuś okno na pierwszym planie
            root.attributes('-topmost', True)  # Zawsze na wierzchu
            root.update()  # Wymuszenie aktualizacji
        
            # Pokaż messagebox
            messagebox.showinfo(popup_title, popup_message)
            
            root.attributes('-topmost', False)
        
        # Zamknij tkinter
            root.destroy()
        
        except Exception as e:
            # Fallback - konsola (jeśli brak GUI)
            self.logger.warning(f"Popup niedostępny: {e}")
            print("\n" + "="*70)
            print("👋 DZIĘKUJEMY ZA KORZYSTANIE Z LEGAL CASE FINDER!")
            print("="*70)
            print(popup_message)
            print("="*70 + "\n")


# ═══════════════════════════════════════════════════════════════════════════
# GŁÓWNA FUNKCJA URUCHOMIENIA
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Główna funkcja aplikacji"""
    try:
        app = LegalCaseFinderApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Aplikacja zakończona.")
    except Exception as e:
        print(f"\n❌ Krytyczny błąd aplikacji: {str(e)}")
        logging.error(f"Krytyczny błąd: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
