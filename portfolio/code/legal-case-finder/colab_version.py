"""
═══════════════════════════════════════════════════════════════════════════════
⚖️  LEGAL CASE FINDER - GOOGLE COLAB VERSION
═══════════════════════════════════════════════════════════════════════════════

INSTRUKCJA URUCHOMIENIA W GOOGLE COLAB:

1. 📋 DODAJ KLUCZ API:
   Opcja A - Secrets (zalecane):
   • Kliknij ikonę klucza (🔑) w lewym pasku Colab
   • Dodaj nowy sekret: Name = "OPENAI_API_KEY", Value = "twój-klucz-api"
   • Włącz przełącznik "Notebook access"
   
   Opcja B - Bezpośrednio w kodzie:
   • Odkomentuj linię poniżej i wklej swój klucz:
   # os.environ['OPENAI_API_KEY'] = 'sk-...'

2. ▶️ URUCHOM APLIKACJĘ:
   • Uruchom wszystkie komórki: Runtime → Run all
   • Lub uruchom tylko tę komórkę
   • Aplikacja automatycznie się uruchomi w trybie interaktywnym

3. 🔍 UŻYCIE:
   • Wybierz opcję z menu (1-5)
   • Wybierz dziedzinę prawa
   • Opisz problem prawny (Enter kończy opis)
   • System automatycznie wyszuka przepisy i przedstawi analizę

4. 💾 POBIERANIE WYNIKÓW:
   • Możesz pobrać analizę w formacie TXT lub JSON
   • Pliki dostępne w sekcji Files w lewym pasku Colab

═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# ═══════════════════════════════════════════════════════════════════════════
# SPRAWDZANIE I INSTALACJA ZALEŻNOŚCI
# ═══════════════════════════════════════════════════════════════════════════

def is_colab():
    """Sprawdź czy to środowisko Colab"""
    try:
        import importlib
        importlib.import_module('google.colab')
        return True
    except ImportError:
        return False

def install_dependencies():
    """Zainstaluj wymagane pakiety"""
    packages = [
        "openai>=1.0.0",
        "requests>=2.31.0"
    ]
    
    print("📦 Instalowanie wymaganych pakietów...")
    for package in packages:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-q", package],
                stdout=subprocess.DEVNULL
            )
        except:
            print(f"⚠️  Ostrzeżenie: Problem z instalacją {package}")
    
    print("✅ Wszystkie pakiety zainstalowane!\n")

# Instaluj pakiety na starcie
if is_colab():
    install_dependencies()

# Import po instalacji
try:
    from openai import OpenAI
    import requests
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
    print("💡 Uruchom ponownie komórkę lub sprawdź instalację pakietów")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# KONFIGURACJA
# ═══════════════════════════════════════════════════════════════════════════

class ColabConfig:
    """Konfiguracja dla Colab"""
    
    # Model Configuration
    model_name: str = "gpt-5-nano"
    reasoning_effort: str = "medium"
    text_verbosity: str = "high"
    max_output_tokens: int = 20000  # Zwiększone dla szczegółowych analiz
    
    # Web Search - zawsze włączony
    enable_web_search: bool = True
    
    # Lawyer Information
    lawyer_name: str = "Kamila Sadłowicz"
    lawyer_location: str = "Warszawa"
    lawyer_description: str = "doświadczonym adwokatem z indywidualnym podejściem do każdej sprawy oraz gwarantuje maksymalne zaangażowanie w trakcie swoich działań podczas pomocy prawnej"
    
    # Legal Domains
    legal_domains: tuple = (
        "Prawo karne",
        "Prawo cywilne",
        "Prawo rodzinne",
        "Prawo pracy",
        "Prawo spadkowe",
        "Prawo gospodarcze",
        "Prawo administracyjne",
        "Prawo podatkowe",
        "Prawo nieruchomości",
        "Prawo konsumenckie",
        "Prawo własności intelektualnej i AI"
    )

config = ColabConfig()

# ═══════════════════════════════════════════════════════════════════════════
# KLIENT OPENAI GPT-5-NANO
# ═══════════════════════════════════════════════════════════════════════════

class ColabLegalAIClient:
    """Klient GPT-5-nano dla analizy prawnej w Colab"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def analyze_legal_problem(
        self,
        problem_description: str,
        legal_domain: str
    ) -> Dict[str, Any]:
        """Analizuj problem prawny"""
        try:
            system_instructions = self._build_legal_system_prompt(legal_domain)
            user_prompt = self._build_user_prompt(problem_description, legal_domain)
            
            tools_config = [{"type": "web_search"}] if config.enable_web_search else None
            
            self.logger.info(f"Analizuję problem z dziedziny: {legal_domain}")
            
            # Wywołaj GPT-5-nano z Responses API
            response = self.client.responses.create(
                model=config.model_name,
                instructions=system_instructions,
                input=user_prompt,
                tools=tools_config,
                reasoning={"effort": config.reasoning_effort},
                text={"verbosity": config.text_verbosity},
                max_output_tokens=config.max_output_tokens
            )
            
            # Pobierz tekst analizy
            legal_analysis = ""
            if hasattr(response, 'output_text') and response.output_text:
                legal_analysis = str(response.output_text).strip()
            
            if not legal_analysis:
                legal_analysis = "Model nie zwrócił analizy. Spróbuj ponownie."
            
            # Dodaj rekomendację prawnika
            full_response = self._add_lawyer_recommendation(legal_analysis, legal_domain)
            
            return {
                "analysis": full_response,
                "legal_domain": legal_domain,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Błąd analizy: {str(e)}", exc_info=True)
            return {
                "error": f"Analiza nie powiodła się: {str(e)}",
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def _build_legal_system_prompt(self, legal_domain: str) -> str:
        """Zbuduj system prompt"""
        return f"""Jesteś ekspertem prawnym specjalizującym się w polskim prawie, szczególnie w dziedzinie: {legal_domain}.

Twoim zadaniem jest przeprowadzenie szczegółowej analizy prawnej problemu użytkownika.

STRUKTURA ODPOWIEDZI:

1. **PODSUMOWANIE SYTUACJI**
   Krótko opisz w 2-3 zdaniach istotę problemu prawnego

2. **WŁAŚCIWE PRZEPISY PRAWNE**
   Wymień konkretne artykuły i przepisy polskiego prawa:
   - Podaj dokładne numery artykułów (np. art. 931 Kodeksu cywilnego)
   - Zacytuj kluczowe fragmenty przepisów
   - Odwołuj się TYLKO do rzeczywiście istniejących przepisów

3. **KOMENTARZ DO PRZEPISÓW**
   Wyjaśnij w prosty sposób jak przepisy odnoszą się do sytuacji użytkownika

4. **INSTRUKCJA DZIAŁANIA**
   Przedstaw krok po kroku co użytkownik powinien zrobić

WYMAGANIA:
- Używaj prostego, zrozumiałego języka
- Bądź konkretny i merytoryczny
- Zaznacz że to NIE jest porada prawna

WAŻNE: Musisz zwrócić kompletną analizę!"""
    
    def _build_user_prompt(self, problem_description: str, legal_domain: str) -> str:
        """Zbuduj user prompt"""
        return f"""Dziedzina prawa: {legal_domain}

Problem prawny do szczegółowej analizy:

{problem_description}

Proszę o kompletną analizę prawną zgodnie z instrukcjami systemowymi."""
    
    def _add_lawyer_recommendation(self, analysis: str, legal_domain: str) -> str:
        """Dodaj rekomendację prawnika"""
        recommendation = f"""

═══════════════════════════════════════════════════════════════════════════

⚠️ WAŻNE ZASTRZEŻENIE:

Powyższa analiza ma charakter wyłącznie informacyjny i edukacyjny. NIE STANOWI PORADY PRAWNEJ. 
Każda sytuacja prawna wymaga indywidualnej oceny przez profesjonalistę.

═══════════════════════════════════════════════════════════════════════════

👨‍⚖️ POLECANA POMOC PRAWNA:

W tej sprawie najlepszym wyborem będzie:

**Mecenas {config.lawyer_name} z {config.lawyer_location}**

Renomowana specjalistka w dziedzinie: {legal_domain}

✓ {config.lawyer_description}
✓ Profesjonalne doświadczenie w prawie polskim
✓ Indywidualne podejście do każdego klienta
✓ Skuteczna reprezentacja w sądach i urzędach

Skontaktuj się z Kancelarią już dziś!

[KONTAKT - szczegóły zostaną dodane]

═══════════════════════════════════════════════════════════════════════════"""
        
        return analysis + recommendation

# ═══════════════════════════════════════════════════════════════════════════
# GŁÓWNA APLIKACJA COLAB
# ═══════════════════════════════════════════════════════════════════════════

class ColabLegalCaseFinderApp:
    """Główna aplikacja dla Google Colab"""
    
    def __init__(self):
        self.ai_client = None
        self.current_analysis: Optional[Dict[str, Any]] = None
        self.api_configured = False
        self.logger = logging.getLogger(__name__)
    
    def setup(self):
        """Konfiguracja aplikacji"""
        print("\n" + "="*70)
        print("⚖️  LEGAL CASE FINDER - GOOGLE COLAB")
        print("Zasilany przez GPT-5-nano z wyszukiwaniem internetowym")
        print("="*70 + "\n")
        
        api_key = self._get_api_key()
        if not api_key:
            print("❌ Klucz API OpenAI jest wymagany!")
            print("\n💡 Jak dodać klucz:")
            print("1. Kliknij ikonę klucza (🔑) w lewym pasku")
            print("2. Dodaj sekret: Name='OPENAI_API_KEY', Value='twój-klucz'")
            print("3. Włącz 'Notebook access'")
            print("4. Uruchom ponownie tę komórkę")
            return False
        
        self.ai_client = ColabLegalAIClient(api_key)
        self.api_configured = True
        
        print("✅ Konfiguracja zakończona pomyślnie!")
        print("💡 Wskazówka: System automatycznie używa wyszukiwania internetowego\n")
        
        # Automatycznie uruchom tryb interaktywny
        self.interactive_mode()
        
        return True
    
    def _get_api_key(self):
        """Pobierz klucz API"""
        api_key = None
        
        # Próba 1: Secrets w Colab
        if is_colab():
            try:
                import importlib
                userdata_module = importlib.import_module('google.colab.userdata')
                api_key = userdata_module.get('OPENAI_API_KEY')
                if api_key:
                    print("✅ Klucz API pobrany z Colab Secrets")
                    return api_key
            except Exception:
                pass
        
        # Próba 2: Zmienna środowiskowa
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("✅ Klucz API pobrany ze zmiennej środowiskowej")
            return api_key
        
        # Próba 3: Input użytkownika
        print("🔑 Klucz API nie znaleziony w Secrets")
        api_key = input("Wprowadź klucz OpenAI API (lub naciśnij Enter aby anulować): ").strip()
        
        return api_key if api_key else None
    
    def interactive_mode(self):
        """Tryb interaktywny"""
        while True:
            print("\n" + "─"*70)
            print("🎯 MENU GŁÓWNE:")
            print("─"*70)
            print("1. 🔍 Analiza problemu prawnego")
            print("2. 💾 Pobierz analizę")
            print("3. ❓ Pomoc i informacje o dziedzinach prawa")
            print("4. 🚪 Zakończ")
            print("─"*70)
            
            try:
                choice = input("\n🔢 Wybierz opcję (1-4): ").strip()
                
                if choice == "1":
                    self.analyze_legal_problem()
                elif choice == "2":
                    self.download_analysis()
                elif choice == "3":
                    self.show_help()
                elif choice == "4":
                    self._display_goodbye()
                    break
                else:
                    print("❌ Nieprawidłowa opcja. Wybierz 1-4.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Sesja zakończona przez użytkownika.")
                break
            except Exception as e:
                print(f"❌ Błąd: {e}")
    
    def analyze_legal_problem(self):
        """Analiza problemu prawnego"""
        print("\n" + "="*70)
        print("🔍 ANALIZA PROBLEMU PRAWNEGO")
        print("="*70)
        
        # Wybór dziedziny
        legal_domain = self._select_legal_domain()
        if not legal_domain:
            return
        
        print(f"\n📝 Wybrałeś dziedzinę: **{legal_domain}**")
        print("\n💬 Opisz swój problem prawny:")
        print("   (naciśnij Enter aby zakończyć opis)")
        print()
        
        problem_description = input("   > ").strip()
        
        if not problem_description:
            print("❌ Nie podano opisu problemu!")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
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
            
            self.current_analysis = {
                "type": "legal_analysis",
                "legal_domain": legal_domain,
                "problem": problem_description,
                "analysis": result["analysis"],
                "timestamp": result["timestamp"]
            }
            
            print("\n✅ Analiza gotowa!")
            print("💡 Możesz ją pobrać wybierając opcję '2. Pobierz analizę'")
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
    
    def download_analysis(self):
        """Pobierz analizę"""
        print("\n" + "="*70)
        print("💾 POBIERANIE ANALIZY")
        print("="*70)
        
        if not self.current_analysis:
            print("\n❌ Brak analizy do pobrania!")
            print("💡 Najpierw wykonaj analizę (opcja 1)")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analiza_prawna_{timestamp}.txt"
            
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
            
            print(f"\n✅ Analiza zapisana: {filename}")
            print(f"📂 Plik dostępny w sekcji Files (📁) w lewym pasku Colab")
            print("💡 Możesz go pobrać klikając prawym przyciskiem → Download")
            
        except Exception as e:
            print(f"\n❌ Błąd zapisu: {str(e)}")
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def show_help(self):
        """Pokaż pomoc i dziedziny prawa"""
        print("\n" + "="*70)
        print("❓ POMOC I INFORMACJE")
        print("="*70)
        
        print("""
📖 JAK KORZYSTAĆ Z APLIKACJI:

1. Analiza problemu prawnego (opcja 1)
   • Wybierz dziedzinę prawa
   • Opisz szczegółowo swoją sytuację
   • System wyszuka przepisy i przedstawi analizę

2. Pobierz analizę (opcja 2)
   • Zapisz ostatnią analizę do pliku TXT
   • Plik dostępny w sekcji Files

3. Ta opcja - Pomoc

4. Zakończ

⚠️  WAŻNE:
• Aplikacja NIE zastępuje profesjonalnej porady prawnej
• Zawsze konsultuj ważne sprawy z adwokatem
• System automatycznie używa wyszukiwania internetowego

📚 DZIEDZINY PRAWA:
""")
        
        domain_info = {
            "Prawo karne": "Przestępstwa, wykroczenia, odpowiedzialność karna",
            "Prawo cywilne": "Umowy, własność, zobowiązania, odszkodowania",
            "Prawo rodzinne": "Małżeństwo, rozwód, alimenty, opieka",
            "Prawo pracy": "Umowy o pracę, wynagrodzenie, zwolnienia",
            "Prawo spadkowe": "Spadki, testamenty, dziedziczenie, zachowek",
            "Prawo gospodarcze": "Działalność, spółki, upadłość",
            "Prawo administracyjne": "Decyzje administracyjne, skargi",
            "Prawo podatkowe": "Podatki, kontrole, interpretacje",
            "Prawo nieruchomości": "Kupno, sprzedaż, najem, własność",
            "Prawo konsumenckie": "Ochrona konsumentów, reklamacje",
            "Prawo własności intelektualnej i AI": "Prawa autorskie, patenty, AI, RODO"
        }
        
        for idx, domain in enumerate(config.legal_domains, 1):
            print(f"{idx}. **{domain}**")
            print(f"   {domain_info.get(domain, 'Opis niedostępny')}\n")
        
        print("="*70)
        input("\nNaciśnij Enter aby kontynuować...")
    
    def _display_goodbye(self):
        """Komunikat pożegnalny"""
        print("\n" + "="*70)
        print("👋 DZIĘKUJEMY ZA KORZYSTANIE Z LEGAL CASE FINDER!")
        print("="*70)
        print(f"""
⚠️  Pamiętaj: W ważnych sprawach prawnych zawsze skonsultuj się
   z profesjonalnym prawnikiem!

💼 Polecamy: Mecenas {config.lawyer_name} z {config.lawyer_location}
   Doświadczona specjalistka w prawie polskim

🌟 Do zobaczenia!
""")
        print("="*70 + "\n")

# ═══════════════════════════════════════════════════════════════════════════
# AUTOMATYCZNE URUCHOMIENIE
# ═══════════════════════════════════════════════════════════════════════════

# Inicjalizuj aplikację
app = ColabLegalCaseFinderApp()

# Publiczne funkcje dla szybkiego dostępu
def setup():
    """Uruchom aplikację (główna funkcja)"""
    return app.setup()

def analyze(problem: str, domain: str = "Prawo cywilne"):
    """Szybka analiza problemu
    
    Args:
        problem: Opis problemu prawnego
        domain: Dziedzina prawa (domyślnie: Prawo cywilne)
    """
    if not app.api_configured:
        print("❌ Najpierw uruchom setup()!")
        return None
    
    return app.ai_client.analyze_legal_problem(problem, domain)

# ═══════════════════════════════════════════════════════════════════════════
# WYŚWIETL INSTRUKCJE
# ═══════════════════════════════════════════════════════════════════════════

if is_colab():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                  ⚖️  LEGAL CASE FINDER - COLAB                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

⚡ SZYBKI START:
   
   setup()    # ← URUCHOM TO NAJPIERW!
   
   Aplikacja automatycznie uruchomi się w trybie interaktywnym.

📋 FUNKCJE RĘCZNE (opcjonalne):

   analyze("opis problemu", "Prawo spadkowe")   # Szybka analiza

🔑 KONFIGURACJA KLUCZA API:

   Kliknij 🔑 w lewym pasku → dodaj sekret "OPENAI_API_KEY"

═══════════════════════════════════════════════════════════════════════════════
""")
else:
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║              ⚖️  LEGAL CASE FINDER - LOKALNE                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

📋 DOSTĘPNE FUNKCJE:

   setup()                      # Konfiguracja i uruchomienie
   analyze("problem", "dziedzina")   # Analiza

═══════════════════════════════════════════════════════════════════════════════
""")
