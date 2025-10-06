"""
Generator Postów Social Media - Główna Aplikacja
Profesjonalne narzędzie do tworzenia treści zasilane GPT-5
"""
import os
import sys
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Direct imports instead of relative
from config import Config
from openai_client import SocialMediaAI

class GeneratorPostowSocialMedia:
    """Główna klasa aplikacji do generowania treści w social media"""
    
    def __init__(self):
        self.config = None
        self.ai_client = None
        self.historia_sesji = []
        self.skonfiguruj_logowanie()
        
    def skonfiguruj_logowanie(self):
        """Konfiguracja systemu logowania"""
        katalog_logow = Path("../logs")  # logi w katalogu nadrzędnym
        katalog_logow.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(katalog_logow / 'generator_social_media.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def skonfiguruj_srodowisko(self) -> bool:
        """Konfiguracja środowiska aplikacji"""
        try:
            # Wykrycie środowiska
            if 'google.colab' in sys.modules:
                self.logger.info("🔍 Wykryto środowisko Google Colab")
                klucz_api = input("🔑 Wprowadź swój klucz API OpenAI: ").strip()
            else:
                self.logger.info("🔍 Wykryto środowisko lokalne (VSCode)")
                
                # Szukaj pliku .env w katalogu nadrzędnym
                plik_env = Path('../.env')
                if plik_env.exists():
                    # Prosty parser pliku .env
                    with open(plik_env, 'r', encoding='utf-8') as f:
                        for linia in f:
                            if linia.strip() and not linia.startswith('#') and '=' in linia:
                                klucz, wartosc = linia.strip().split('=', 1)
                                os.environ[klucz] = wartosc.strip('"\'')
                
                klucz_api = os.getenv('OPENAI_API_KEY')
                
                if not klucz_api:
                    klucz_api = input("🔑 Wprowadź swój klucz API OpenAI: ").strip()
                    
            if not klucz_api:
                print("❌ Klucz API OpenAI jest wymagany!")
                return False
                
            self.config = Config(openai_api_key=klucz_api)
            self.ai_client = SocialMediaAI(self.config)
            
            self.logger.info("✅ Konfiguracja środowiska zakończona pomyślnie")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Konfiguracja środowiska nie powiodła się: {str(e)}")
            print(f"❌ Błąd konfiguracji: {str(e)}")
            return False
    
    def wyswietl_powitanie(self):
        """Wyświetl wiadomość powitalną i informacje o aplikacji"""
        print("\n" + "=" * 65)
        print("🚀 GENERATOR POSTÓW SOCIAL MEDIA")
        print("Zasilany przez OpenAI GPT-5 z Responses API")
        print("=" * 65)
        print("\n✨ Profesjonalne Funkcje:")
        print("📱 Optymalizacja multi-platformowa (Twitter, LinkedIn, Facebook)")
        print("🎨 Różnorodne style treści (Profesjonalny, Swobodny, Angażujący)")
        print("📊 Analiza wydajności i wskazówki optymalizacyjne")
        print("🔤 Inteligentne zarządzanie limitem znaków")
        print("📈 Optymalizacja hashtagów i SEO")
        print("💾 Historia sesji i możliwości eksportu")
        print()
    
    def pobierz_preferencje_uzytkownika(self) -> Dict:
        """Interaktywne zbieranie preferencji użytkownika"""
        print("📝 Konfiguracja Treści:")
        print("-" * 30)
        
        # Wybór platformy
        platformy = {
            "1": ("twitter", "Twitter (280 znaków, hashtagi, zwięzłość)"),
            "2": ("linkedin", "LinkedIn (Profesjonalny, biznesowy)"), 
            "3": ("facebook", "Facebook (Angażujący, zachęcający do rozmowy)"),
            "4": ("instagram", "Instagram (Wizualny, fabularny)"),
            "5": ("universal", "Uniwersalny (Kompatybilny z wieloma platformami)")
        }
        
        print("\n🌐 Platformy Docelowe:")
        for klucz, (_, opis) in platformy.items():
            print(f"  {klucz}. {opis}")
        
        while True:
            wybor_platformy = input("\nWybierz platformę (1-5): ").strip()
            if wybor_platformy in platformy:
                platforma = platformy[wybor_platformy][0]
                break
            print("❌ Nieprawidłowy wybór. Wybierz 1-5.")
        
        # Wybór stylu
        style = {
            "1": ("professional", "Profesjonalny - Ton odpowiedni dla biznesu"),
            "2": ("engaging", "Angażujący - Przyciągający i interaktywny"),
            "3": ("casual", "Swobodny - Przyjazny i rozmówkowy"),
            "4": ("humorous", "Humorystyczny - Lekki i zabawny"),
            "5": ("inspirational", "Inspiracyjny - Motywujący i podnoszący na duchu")
        }
        
        print("\n🎨 Style Treści:")
        for klucz, (_, opis) in style.items():
            print(f"  {klucz}. {opis}")
        
        while True:
            wybor_stylu = input("\nWybierz styl (1-5): ").strip()
            if wybor_stylu in style:
                styl = style[wybor_stylu][0]
                break
            print("❌ Nieprawidłowy wybór. Wybierz 1-5.")
        
        # Limit znaków
        domyslne_limity = {
            "twitter": 280,
            "linkedin": 500,
            "facebook": 400,
            "instagram": 350,
            "universal": 300
        }
        
        domyslny_limit = domyslne_limity.get(platforma, 300)
        
        while True:
            try:
                wprowadzony_limit = input(f"\n📏 Maksymalna liczba znaków (domyślnie {domyslny_limit}): ").strip()
                max_znakow = int(wprowadzony_limit) if wprowadzony_limit else domyslny_limit
                if max_znakow > 0:
                    break
                print("❌ Limit znaków musi być dodatni.")
            except ValueError:
                print("❌ Proszę wprowadzić prawidłową liczbę.")
        
        return {
            "platforma": platforma,
            "styl": styl,
            "max_znakow": max_znakow
        }
    
    def generuj_pojedynczy_post(self):
        """Generuj pojedynczy post w social media"""
        try:
            preferencje = self.pobierz_preferencje_uzytkownika()
            
            print(f"\n📌 Wprowadzanie Tematu:")
            temat = input("Wprowadź temat/pomysł na post: ").strip()
            
            if not temat:
                print("❌ Temat nie może być pusty!")
                return
            
            # Opcjonalny dodatkowy kontekst
            kontekst = input("Dodatkowy kontekst (opcjonalnie): ").strip()
            
            print(f"\n⏳ Generuję treść w stylu {preferencje['styl']} dla platformy {preferencje['platforma'].title()}...")
            
            # Generuj post
            wynik_posta = self.ai_client.generate_post(
                topic=temat,
                platform=preferencje["platforma"],
                style=preferencje["styl"],
                max_length=preferencje["max_znakow"],
                context=kontekst,
                language="polish"
            )
            
            if wynik_posta.startswith("❌"):
                print(f"\n{wynik_posta}")
                return
            
            # Wyświetl wynik
            print(f"\n📱 Wygenerowany Post na {preferencje['platforma'].title()}:")
            print("=" * 60)
            print(wynik_posta)
            print("=" * 60)
            print(f"📊 Liczba znaków: {len(wynik_posta)}/{preferencje['max_znakow']}")
            
            # Zapisz do historii
            dane_posta = {
                "znacznik_czasu": datetime.now().isoformat(),
                "temat": temat,
                "platforma": preferencje["platforma"],
                "styl": preferencje["styl"],
                "tresc": wynik_posta,
                "liczba_znakow": len(wynik_posta)
            }
            self.historia_sesji.append(dane_posta)
            
            # Opcjonalna analiza
            analiza = input("\n📊 Przeanalizować ten post pod kątem potencjału wydajności? (t/N): ")
            if analiza.lower().startswith('t'):
                self.analizuj_wydajnosc_posta(wynik_posta)
                
        except Exception as e:
            self.logger.error(f"Błąd generowania pojedynczego posta: {str(e)}")
            print(f"❌ Błąd generowania: {str(e)}")
    
    def analizuj_wydajnosc_posta(self, tresc_posta: str):
        """Analizuj post pod kątem potencjalnej wydajności"""
        try:
            print("\n⏳ Analizuję wydajność treści...")
            
            analiza = self.ai_client.analyze_post_performance(tresc_posta, language="polish")
            
            if analiza["success"]:
                print(f"\n📈 Analiza Wydajności:")
                print("-" * 50)
                print(analiza["analysis"])
                print("-" * 50)
            else:
                print(f"❌ Analiza nie powiodła się: {analiza.get('analysis', 'Nieznany błąd')}")
                
        except Exception as e:
            print(f"❌ Błąd analizy: {str(e)}")
    
    def generuj_wsadowo_posty(self):
        """Generuj wiele postów naraz"""
        try:
            preferencje = self.pobierz_preferencje_uzytkownika()
            
            print(f"\n📝 Konfiguracja Generowania Wsadowego:")
            wprowadzone_tematy = input("Wprowadź tematy oddzielone przecinkami: ").strip()
            
            if not wprowadzone_tematy:
                print("❌ Nie podano żadnych tematów!")
                return
            
            tematy = [temat.strip() for temat in wprowadzone_tematy.split(",") if temat.strip()]
            
            if len(tematy) > 10:
                potwierdz = input(f"⚠️  Wykryto {len(tematy)} tematów. To może potrwać. Kontynuować? (t/N): ")
                if not potwierdz.lower().startswith('t'):
                    return
            
            print(f"\n⏳ Generuję {len(tematy)} postów dla platformy {preferencje['platforma'].title()}...")
            
            wyniki_wsadowe = []
            
            for i, temat in enumerate(tematy, 1):
                print(f"\n📝 Generuję post {i}/{len(tematy)}: {temat[:30]}...")
                
                wynik_posta = self.ai_client.generate_post(
                    topic=temat,
                    platform=preferencje["platforma"],
                    style=preferencje["styl"],
                    max_length=preferencje["max_znakow"],
                    language="polish"
                )
                
                wyniki_wsadowe.append({
                    "temat": temat,
                    "tresc": wynik_posta,
                    "liczba_znakow": len(wynik_posta)
                })
                
                # Wyświetl wynik
                print(f"\n📱 Post {i}: {temat}")
                print("-" * 50)
                print(wynik_posta)
                print(f"Znaków: {len(wynik_posta)}")
                print("-" * 50)
            
            # Zapisz wsadowe do historii
            dane_wsadowe = {
                "znacznik_czasu": datetime.now().isoformat(),
                "typ": "wsadowe",
                "platforma": preferencje["platforma"],
                "styl": preferencje["styl"],
                "posty": wyniki_wsadowe
            }
            self.historia_sesji.append(dane_wsadowe)
            
            # Opcja eksportu
            eksport = input(f"\n💾 Wyeksportować {len(tematy)} postów do pliku? (t/N): ")
            if eksport.lower().startswith('t'):
                self.eksportuj_wyniki_wsadowe(wyniki_wsadowe, preferencje)
                
        except Exception as e:
            self.logger.error(f"Błąd w generowaniu wsadowym: {str(e)}")
            print(f"❌ Błąd generowania wsadowego: {str(e)}")
    
    def eksportuj_wyniki_wsadowe(self, wyniki: List[Dict], preferencje: Dict):
        """Eksportuj wyniki wsadowe do pliku"""
        try:
            znacznik_czasu = datetime.now().strftime("%Y%m%d_%H%M%S")
            nazwa_pliku = f"posty_social_{preferencje['platforma']}_{znacznik_czasu}.txt"
            
            katalog_eksportu = Path("../exports")  # eksporty w katalogu nadrzędnym
            katalog_eksportu.mkdir(exist_ok=True)
            
            sciezka_pliku = katalog_eksportu / nazwa_pliku
            
            with open(sciezka_pliku, 'w', encoding='utf-8') as f:
                f.write(f"Eksport Postów Social Media\n")
                f.write(f"Platforma: {preferencje['platforma'].title()}\n")
                f.write(f"Styl: {preferencje['styl'].title()}\n")
                f.write(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, post in enumerate(wyniki, 1):
                    f.write(f"POST {i}: {post['temat']}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"{post['tresc']}\n")
                    f.write(f"Znaków: {post['liczba_znakow']}\n")
                    f.write("\n" + "="*60 + "\n\n")
            
            print(f"✅ Posty wyeksportowane do: {sciezka_pliku}")
            
        except Exception as e:
            print(f"❌ Eksport nie powiódł się: {str(e)}")
    
    def wyswietl_historie_sesji(self):
        """Wyświetl aktualną historię sesji"""
        if not self.historia_sesji:
            print("\n📋 Brak postów wygenerowanych w tej sesji.")
            return
        
        print(f"\n📋 Historia Sesji ({len(self.historia_sesji)} elementów):")
        print("=" * 50)
        
        for i, element in enumerate(self.historia_sesji, 1):
            if element.get("typ") == "wsadowe":
                print(f"{i}. Generowanie Wsadowe ({len(element['posty'])} postów)")
                print(f"   Platforma: {element['platforma'].title()}")
                print(f"   Czas: {element['znacznik_czasu'][:19]}")
            else:
                print(f"{i}. Pojedynczy Post: {element['temat'][:30]}...")
                print(f"   Platforma: {element['platforma'].title()}")
                print(f"   Znaków: {element['liczba_znakow']}")
        
        print("=" * 50)
    
    def pokaz_pomoc(self):
        """Wyświetl informacje pomocy"""
        tekst_pomocy = """
📚 POMOC - Generator Postów Social Media

🎯 GŁÓWNE FUNKCJE:
1. Generowanie Pojedynczego Posta - Utwórz jeden zoptymalizowany post
2. Generowanie Wsadowe - Wygeneruj wiele postów naraz
3. Analiza Wydajności - Otrzymaj przewidywania zaangażowania
4. Obsługa Multi-platformowa - Twitter, LinkedIn, Facebook, Instagram
5. Różne Style - Profesjonalny, Angażujący, Swobodny, Humorystyczny
6. Możliwości Eksportu - Zapisuj posty do plików

🔧 WSKAZÓWKI UŻYTKOWANIA:
• Bądź konkretny z tematami dla lepszych wyników
• Używaj pola kontekstu dla dodatkowych informacji
• Sprawdzaj limity znaków dla każdej platformy
• Analizuj posty aby poprawić zaangażowanie
• Eksportuj wyniki wsadowe do współpracy zespołowej

⚠️  WAŻNE UWAGI:
• Wygenerowana treść pochodzi z AI i powinna być sprawdzona
• Sprawdź wytyczne specyficzne dla platformy przed publikacją
• Rozważ swoją publiczność i głos marki
• Testuj różne style aby znaleźć to co najlepiej działa

🔑 SKRÓTY KLAWISZOWE:
• Ctrl+C - Wyjście z aplikacji w dowolnym momencie
• Enter - Zaakceptuj domyślne wartości w zapytaniach
"""
        print(tekst_pomocy)
    
    def menu_glowne(self):
        """Główna pętla menu aplikacji"""
        while True:
            print("\n" + "─" * 50)
            print("🎯 MENU GŁÓWNE:")
            print("1. 📝 Generuj pojedynczy post")
            print("2. 📚 Generuj posty wsadowo") 
            print("3. 📊 Analizuj istniejący post")
            print("4. 📋 Zobacz historię sesji")
            print("5. 📚 Pomoc i wskazówki")
            print("6. 🚪 Wyjście")
            
            wybor = input("\nWybierz opcję (1-6): ").strip()
            
            if wybor == "1":
                self.generuj_pojedynczy_post()
                
            elif wybor == "2":
                self.generuj_wsadowo_posty()
                
            elif wybor == "3":
                istniejacy_post = input("\n📄 Wklej post do analizy: ").strip()
                if istniejacy_post:
                    self.analizuj_wydajnosc_posta(istniejacy_post)
                else:
                    print("❌ Nie podano treści!")
                    
            elif wybor == "4":
                self.wyswietl_historie_sesji()
                
            elif wybor == "5":
                self.pokaz_pomoc()
                
            elif wybor == "6":
                print("\n👋 Dziękujemy za korzystanie z Generatora Postów Social Media!")
                print("💡 Pamiętaj o sprawdzeniu treści wygenerowanej przez AI przed publikacją!")
                break
                
            else:
                print("❌ Nieprawidłowa opcja. Wybierz 1-6.")
    
    def uruchom(self):
        """Główny punkt wejścia aplikacji"""
        try:
            self.wyswietl_powitanie()
            
            if not self.skonfiguruj_srodowisko():
                return
            
            print("✅ Konfiguracja zakończona pomyślnie!")
            print("💡 Wskazówka: Używaj konkretnych tematów dla lepszych wyników")
            
            self.menu_glowne()
            
        except KeyboardInterrupt:
            print("\n\n👋 Aplikacja zakończona przez użytkownika. Do widzenia!")
        except Exception as e:
            self.logger.error(f"Nieoczekiwany błąd aplikacji: {str(e)}")
            print(f"❌ Nieoczekiwany błąd: {str(e)}")

def main():
    """Funkcja punktu wejścia"""
    app = GeneratorPostowSocialMedia()
    app.uruchom()

if __name__ == "__main__":
    main()
