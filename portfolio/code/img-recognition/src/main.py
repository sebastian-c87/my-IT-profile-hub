"""
Rozpoznawanie Obrazów AI - Główna Aplikacja
Zaawansowane narzędzie analizy obrazów zasilane GPT-5 Vision
"""
import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Direct imports
from config import Config
from openai_client import ImageRecognitionAI
from image_processor import ImageProcessor

class GeneratorRozpoznawaniaObrazow:
    """Główna klasa aplikacji do rozpoznawania obrazów"""
    
    def __init__(self):
        self.config = None
        self.ai_client = None
        self.image_processor = None
        self.historia_analiz = []
        self.skonfiguruj_logowanie()
        
    def skonfiguruj_logowanie(self):
        """Konfiguracja systemu logowania"""
        katalog_logow = Path("../logs")
        katalog_logow.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(katalog_logow / 'rozpoznawanie_obrazow.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def skonfiguruj_srodowisko(self) -> bool:
        """Konfiguracja środowiska aplikacji"""
        try:
            if 'google.colab' in sys.modules:
                self.logger.info("🔍 Wykryto środowisko Google Colab")
                klucz_api = input("🔑 Wprowadź swój klucz API OpenAI: ").strip()
            else:
                self.logger.info("🔍 Wykryto środowisko lokalne (VSCode)")
                
                # Szukaj pliku .env w katalogu nadrzędnym
                plik_env = Path('../.env')
                if plik_env.exists():
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
            self.ai_client = ImageRecognitionAI(self.config)
            self.image_processor = ImageProcessor(self.config)
            
            self.logger.info("✅ Konfiguracja środowiska zakończona pomyślnie")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Konfiguracja środowiska nie powiodła się: {str(e)}")
            print(f"❌ Błąd konfiguracji: {str(e)}")
            return False
    
    def wyswietl_powitanie(self):
        """Wyświetl wiadomość powitalną"""
        print("\n" + "=" * 70)
        print("🖼️  ROZPOZNAWANIE OBRAZÓW AI")
        print("Zasilane przez OpenAI GPT-5 Vision")
        print("=" * 70)
        print("\n✨ Zaawansowane Funkcje:")
        print("🔍 Szczegółowa analiza obrazów")
        print("🏷️  Rozpoznawanie obiektów i scen") 
        print("📝 Ekstraktowanie tekstu z obrazów (OCR)")
        print("🎨 Analiza artystyczna i techniczna")
        print("⚖️  Porównywanie dwóch obrazów")
        print("🌐 Obsługa URL i plików lokalnych")
        print("💾 Historia analiz i eksport wyników")
        print()
    
    def pobierz_sciezke_obrazu(self) -> Optional[str]:
        """Pobierz ścieżkę do obrazu od użytkownika"""
        print("📂 Źródło obrazu:")
        print("1. Plik lokalny")
        print("2. URL (link)")
        
        while True:
            wybor = input("\nWybierz źródło (1-2): ").strip()
            
            if wybor == "1":
                sciezka = input("📁 Podaj ścieżkę do pliku: ").strip().strip('"\'')
                if sciezka and os.path.exists(sciezka):
                    return sciezka
                else:
                    print("❌ Plik nie istnieje lub ścieżka jest nieprawidłowa!")
                    
            elif wybor == "2":
                url = input("🌐 Podaj URL obrazu: ").strip()
                if url and url.startswith(('http://', 'https://')):
                    return url
                else:
                    print("❌ Nieprawidłowy URL!")
                    
            else:
                print("❌ Nieprawidłowy wybór. Wybierz 1 lub 2.")
        
        return None
    
    def wybierz_typ_analizy(self) -> str:
        """Wybierz typ analizy obrazu"""
        typy_analiz = {
            "1": ("comprehensive", "Kompleksowa - pełna analiza obrazu"),
            "2": ("objects", "Obiekty - identyfikacja przedmiotów"),
            "3": ("scene", "Scena - opis sytuacji i kontekstu"),
            "4": ("text", "Tekst - wykrywanie i odczytywanie napisów"),
            "5": ("artistic", "Artystyczna - analiza estetyczna"),
            "6": ("custom", "Niestandardowa - własny prompt")
        }
        
        print("\n🎯 Rodzaje analizy:")
        for klucz, (_, opis) in typy_analiz.items():
            print(f"  {klucz}. {opis}")
        
        while True:
            wybor = input("\nWybierz typ analizy (1-6): ").strip()
            if wybor in typy_analiz:
                if wybor == "6":  # custom
                    custom_prompt = input("✍️  Wprowadź własny prompt analizy: ").strip()
                    return f"custom:{custom_prompt}"
                return typy_analiz[wybor][0]
            print("❌ Nieprawidłowy wybór. Wybierz 1-6.")
    
    def analizuj_pojedynczy_obraz(self):
        """Analizuj pojedynczy obraz"""
        try:
            sciezka_obrazu = self.pobierz_sciezke_obrazu()
            if not sciezka_obrazu:
                return
            
            typ_analizy = self.wybierz_typ_analizy()
            
            # Sprawdź czy to custom prompt
            custom_prompt = ""
            if typ_analizy.startswith("custom:"):
                custom_prompt = typ_analizy[7:]  # Usuń prefiks "custom:"
                typ_analizy = "custom"
            
            print(f"\n⏳ Analizuję obraz: {os.path.basename(sciezka_obrazu)}...")
            print("🤖 To może potrwać kilka sekund...")
            
            # Wykonaj analizę
            wynik = self.ai_client.analyze_image(
                image_path=sciezka_obrazu,
                analysis_type=typ_analizy,
                language="polish",
                custom_prompt=custom_prompt
            )
            
            if wynik["success"]:
                # Wyświetl wyniki
                print(f"\n🖼️  ANALIZA OBRAZU")
                print("=" * 60)
                print(wynik["analysis"])
                print("=" * 60)
                
                # Informacje techniczne
                if "image_info" in wynik:
                    info = wynik["image_info"]
                    print(f"\n📊 Informacje techniczne:")
                    print(f"📏 Wymiary: {info.get('dimensions', 'N/A')}")
                    print(f"📁 Format: {info.get('format', 'N/A')}")
                    print(f"💾 Rozmiar: {info.get('size_bytes', 0)} bajtów")
                
                # Zapisz do historii
                self.historia_analiz.append({
                    "timestamp": datetime.now().isoformat(),
                    "sciezka": sciezka_obrazu,
                    "typ_analizy": typ_analizy,
                    "wynik": wynik["analysis"],
                    "info_techniczne": wynik.get("image_info", {})
                })
                
                print("\n✅ Analiza zakończona pomyślnie!")
                
            else:
                print(f"\n❌ Błąd analizy: {wynik.get('error', 'Nieznany błąd')}")
                
        except Exception as e:
            self.logger.error(f"Błąd analizy pojedynczego obrazu: {str(e)}")
            print(f"❌ Błąd analizy: {str(e)}")
    
    def porownaj_obrazy(self):
        """Porównaj dwa obrazy"""
        try:
            print("🔍 Porównywanie dwóch obrazów\n")
            
            print("📷 PIERWSZY OBRAZ:")
            obraz1 = self.pobierz_sciezke_obrazu()
            if not obraz1:
                return
            
            print("\n📷 DRUGI OBRAZ:")
            obraz2 = self.pobierz_sciezke_obrazu()
            if not obraz2:
                return
            
            print(f"\n⏳ Porównuję obrazy...")
            print("🤖 Analiza może potrwać chwilę...")
            
            wynik = self.ai_client.compare_images(obraz1, obraz2, language="polish")
            
            if wynik["success"]:
                print(f"\n⚖️  PORÓWNANIE OBRAZÓW")
                print("=" * 60)
                print(wynik["comparison"])
                print("=" * 60)
                
                # Zapisz do historii
                self.historia_analiz.append({
                    "timestamp": datetime.now().isoformat(),
                    "typ": "porownanie",
                    "obraz1": obraz1,
                    "obraz2": obraz2,
                    "wynik": wynik["comparison"]
                })
                
                print("\n✅ Porównanie zakończone pomyślnie!")
            else:
                print(f"\n❌ Błąd porównania: {wynik.get('error', 'Nieznany błąd')}")
                
        except Exception as e:
            self.logger.error(f"Błąd porównywania obrazów: {str(e)}")
            print(f"❌ Błąd porównania: {str(e)}")
    
    def wyodrebnij_tekst_z_obrazu(self):
        """Wyodrębnij tekst z obrazu (OCR)"""
        try:
            print("📝 Wyodrębnianie tekstu z obrazu (OCR)\n")
            
            sciezka_obrazu = self.pobierz_sciezke_obrazu()
            if not sciezka_obrazu:
                return
            
            print(f"\n⏳ Analizuję tekst na obrazie...")
            print("🤖 Rozpoznawanie może potrwać chwilę...")
            
            wynik = self.ai_client.extract_text_from_image(sciezka_obrazu, language="polish")
            
            if wynik["success"]:
                print(f"\n📝 WYODRĘBNIONY TEKST")
                print("=" * 60)
                print(wynik["extracted_text"])
                print("=" * 60)
                
                # Zapisz do historii
                self.historia_analiz.append({
                    "timestamp": datetime.now().isoformat(),
                    "typ": "ocr",
                    "sciezka": sciezka_obrazu,
                    "tekst": wynik["extracted_text"]
                })
                
                print("\n✅ Wyodrębnianie tekstu zakończone!")
            else:
                print(f"\n❌ Błąd OCR: {wynik.get('error', 'Nieznany błąd')}")
                
        except Exception as e:
            self.logger.error(f"Błąd wyodrębniania tekstu: {str(e)}")
            print(f"❌ Błąd OCR: {str(e)}")
    
    def wyswietl_historie_analiz(self):
        """Wyświetl historię analiz"""
        if not self.historia_analiz:
            print("\n📋 Brak analiz w historii tej sesji.")
            return
        
        print(f"\n📋 HISTORIA ANALIZ ({len(self.historia_analiz)} elementów):")
        print("=" * 60)
        
        for i, analiza in enumerate(self.historia_analiz, 1):
            print(f"\n{i}. {analiza.get('typ', 'analiza').upper()}")
            print(f"   Czas: {analiza['timestamp'][:19]}")
            
            if analiza.get('typ') == 'porownanie':
                print(f"   Obrazy: {os.path.basename(analiza['obraz1'])} vs {os.path.basename(analiza['obraz2'])}")
            elif analiza.get('typ') == 'ocr':
                print(f"   Obraz: {os.path.basename(analiza['sciezka'])}")
                print(f"   Tekst: {analiza['tekst'][:50]}...")
            else:
                print(f"   Obraz: {os.path.basename(analiza['sciezka'])}")
                print(f"   Typ: {analiza.get('typ_analizy', 'N/A')}")
                print(f"   Wynik: {analiza['wynik'][:50]}...")
        
        print("=" * 60)
    
    def eksportuj_historie(self):
        """Eksportuj historię analiz do pliku"""
        if not self.historia_analiz:
            print("❌ Brak danych do eksportu.")
            return
        
        try:
            import json
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nazwa_pliku = f"historia_analiz_{timestamp}.json"
            
            katalog_eksportu = Path("../exports")
            katalog_eksportu.mkdir(exist_ok=True)
            
            sciezka_pliku = katalog_eksportu / nazwa_pliku
            
            dane_eksportu = {
                "timestamp_eksportu": datetime.now().isoformat(),
                "liczba_analiz": len(self.historia_analiz),
                "analizy": self.historia_analiz
            }
            
            with open(sciezka_pliku, 'w', encoding='utf-8') as f:
                json.dump(dane_eksportu, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Historia wyeksportowana do: {sciezka_pliku}")
            
        except Exception as e:
            print(f"❌ Eksport nie powiódł się: {str(e)}")
    
    def pokaz_pomoc(self):
        """Wyświetl pomoc i wskazówki"""
        tekst_pomocy = """
📚 POMOC - Rozpoznawanie Obrazów AI

🎯 GŁÓWNE FUNKCJE:
1. Analiza Obrazów - Szczegółowe rozpoznawanie zawartości obrazu
2. Porównanie Obrazów - Analiza różnic i podobieństw między dwoma obrazami
3. OCR (Rozpoznawanie Tekstu) - Wyodrębnianie tekstu z obrazów
4. Historia Analiz - Przegląd poprzednich analiz
5. Eksport Wyników - Zapisywanie rezultatów do pliku

🖼️  OBSŁUGIWANE FORMATY:
• JPEG (.jpg, .jpeg) - zalecany
• PNG (.png) - z przezroczystością
• GIF (.gif) - obrazy animowane
• BMP (.bmp) - format Windows
• WebP (.webp) - nowoczesny format

📁 ŹRÓDŁA OBRAZÓW:
• Pliki lokalne - ścieżka na dysku
• Adresy URL - linki do obrazów w internecie
• Maksymalny rozmiar: 20MB

🎯 RODZAJE ANALIZ:
• Kompleksowa - pełny opis obrazu
• Obiekty - lista przedmiotów na zdjęciu
• Scena - kontekst i sytuacja
• Tekst - OCR i rozpoznawanie napisów
• Artystyczna - analiza estetyczna

💡 WSKAZÓWKI:
• Używaj obrazów dobrej jakości dla lepszych wyników
• URL obrazów muszą być bezpośrednie (kończyć się .jpg, .png itp.)
• Duże obrazy są automatycznie zmniejszane
• Wyniki są zapisywane w historii sesji

⚠️  WAŻNE UWAGI:
• Analizy AI mogą zawierać błędy - zawsze weryfikuj wyniki
• Nie analizuj obrazów zawierających dane osobowe bez zgody
• Szanuj prawa autorskie przy analizowaniu obrazów z internetu
• Aplikacja wymaga połączenia z internetem dla OpenAI API

🔑 SKRÓTY KLAWISZOWE:
• Ctrl+C - Wyjście z aplikacji w dowolnym momencie
• Enter - Potwierdzenie domyślnych opcji
"""
        print(tekst_pomocy)
    
    def menu_glowne(self):
        """Główna pętla menu aplikacji"""
        while True:
            print("\n" + "─" * 50)
            print("🎯 MENU GŁÓWNE:")
            print("1. 🔍 Analizuj obraz")
            print("2. ⚖️  Porównaj dwa obrazy")
            print("3. 📝 Wyodrębnij tekst (OCR)")
            print("4. 📋 Historia analiz")
            print("5. 💾 Eksportuj historię")
            print("6. 📚 Pomoc i wskazówki")
            print("7. 🚪 Wyjście")
            
            wybor = input("\nWybierz opcję (1-7): ").strip()
            
            if wybor == "1":
                self.analizuj_pojedynczy_obraz()
            elif wybor == "2":
                self.porownaj_obrazy()
            elif wybor == "3":
                self.wyodrebnij_tekst_z_obrazu()
            elif wybor == "4":
                self.wyswietl_historie_analiz()
            elif wybor == "5":
                self.eksportuj_historie()
            elif wybor == "6":
                self.pokaz_pomoc()
            elif wybor == "7":
                print("\n👋 Dziękujemy za korzystanie z Rozpoznawania Obrazów AI!")
                print("💡 Pamiętaj o weryfikacji wyników analiz AI!")
                break
            else:
                print("❌ Nieprawidłowa opcja. Wybierz 1-7.")
    
    def uruchom(self):
        """Główny punkt wejścia aplikacji"""
        try:
            self.wyswietl_powitanie()
            
            if not self.skonfiguruj_srodowisko():
                return
            
            print("✅ Konfiguracja zakończona pomyślnie!")
            print("💡 Wskazówka: Używaj obrazów dobrej jakości dla lepszych wyników")
            
            self.menu_glowne()
            
        except KeyboardInterrupt:
            print("\n\n👋 Aplikacja zakończona przez użytkownika. Do widzenia!")
        except Exception as e:
            self.logger.error(f"Nieoczekiwany błąd aplikacji: {str(e)}")
            print(f"❌ Nieoczekiwany błąd: {str(e)}")

def main():
    """Funkcja punktu wejścia"""
    app = GeneratorRozpoznawaniaObrazow()
    app.uruchom()

if __name__ == "__main__":
    main()
