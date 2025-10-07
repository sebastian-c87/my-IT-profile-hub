"""
═══════════════════════════════════════════════════════════════════════════════
🖼️  IMAGE RECOGNITION AI - GOOGLE COLAB VERSION
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

3. 🖼️ UŻYCIE:
   • Wybierz opcję z menu (1-6)
   • Podaj URL obrazu LUB upload plik
   • Wybierz typ analizy
   • Poczekaj na wyniki!

4. 📥 UPLOAD OBRAZÓW:
   • Kliknij ikonę plików w lewym pasku
   • Przeciągnij i upuść obraz
   • Skopiuj nazwę pliku i wklej jako ścieżkę

═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import sys
import os
import json
import base64
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from io import BytesIO

# ═══════════════════════════════════════════════════════════════════════════
# SPRAWDZANIE I INSTALACJA ZALEŻNOŚCI
# ═══════════════════════════════════════════════════════════════════════════

def is_colab():
    """Sprawdź czy to środowisko Colab"""
    try:
        # Bezpieczny import dla Pylance
        import importlib
        importlib.import_module('google.colab')
        return True
    except ImportError:
        return False

def install_dependencies():
    """Zainstaluj wymagane pakiety"""
    packages = [
        "openai>=1.0.0",
        "pillow>=10.0.0", 
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
    from PIL import Image
    import requests
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
    print("💡 Uruchom ponownie komórkę lub sprawdź instalację pakietów")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# KLASA ANALIZY OBRAZÓW - GPT-5-MINI
# ═══════════════════════════════════════════════════════════════════════════

class ColabImageRecognitionAI:
    """Klient GPT-5-mini z Responses API dla analizy obrazów"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def encode_image_base64(self, image_input) -> Optional[str]:
        """Koduj obraz do base64"""
        try:
            # URL lub ścieżka pliku
            if isinstance(image_input, str):
                if image_input.startswith(('http://', 'https://')):
                    # Pobierz z URL
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(image_input, timeout=30, headers=headers)
                    response.raise_for_status()
                    image_data = response.content
                else:
                    # Wczytaj z pliku
                    with open(image_input, 'rb') as f:
                        image_data = f.read()
            else:
                # Już jest jako bytes
                image_data = image_input
            
            # Przetwórz obraz
            try:
                img = Image.open(BytesIO(image_data))
                
                # Konwertuj do RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Zmniejsz rozmiar (oszczędzanie tokenów)
                max_size = (1024, 1024)
                if img.width > max_size[0] or img.height > max_size[1]:
                    img.thumbnail(max_size, Image.LANCZOS)
                
                # Konwertuj z powrotem do bytes
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=75, optimize=True)
                image_data = buffer.getvalue()
                
            except Exception as e:
                print(f"⚠️  Ostrzeżenie przetwarzania obrazu: {e}")
            
            # Koduj do base64
            encoded = base64.b64encode(image_data).decode('utf-8')
            return encoded
            
        except Exception as e:
            print(f"❌ Błąd kodowania: {e}")
            return None
    
    def analyze_image(self, image_input, analysis_type: str = "comprehensive",
                     language: str = "polish") -> Dict[str, Any]:
        """Analizuj obraz używając GPT-5-mini z Responses API"""
        try:
            # Koduj obraz
            print("🔄 Przetwarzanie obrazu...")
            image_base64 = self.encode_image_base64(image_input)
            if not image_base64:
                return {"error": "Nie udało się zakodować obrazu", "success": False}
            
            # Buduj prompt
            prompt = self._build_prompt(analysis_type, language)
            
            print("🤖 Wysyłanie do GPT-5-mini...")
            
            # Wywołaj Responses API z prawidłowym formatem
            response = self.client.responses.create(
                model="gpt-5-mini",
                input=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        ]
                    }
                ],
                reasoning={"effort": "medium"},
                text={"verbosity": "high"},
                max_output_tokens=1200
            )
            
            return {
                "analysis": response.output_text.strip(),
                "analysis_type": analysis_type,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Analiza nie powiodła się: {str(e)}",
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def _build_prompt(self, analysis_type: str, language: str) -> str:
        """Buduj prompt analizy"""
        
        if language == "polish":
            prompts = {
                "comprehensive": "Przeanalizuj szczegółowo ten obraz. Opisz wszystkie widoczne elementy, scenę, obiekty, osoby, kolory, oświetlenie, teksty i nastrój. Podaj kompletną analizę.",
                "objects": "Zidentyfikuj i opisz WSZYSTKIE obiekty na tym obrazie. Dla każdego podaj: nazwę, położenie w kadrze, rozmiar, stan, kolor i materiał.",
                "scene": "Opisz szczegółowo scenę: gdzie to się dzieje, jaka sytuacja, co się dzieje, pora dnia/roku.",
                "text": "Znajdź i przepisz DOKŁADNIE wszystkie teksty, napisy, znaki i symbole widoczne na tym obrazie. Zachowaj formatowanie.",
                "artistic": "Wykonaj profesjonalną analizę artystyczną: styl fotograficzny, technika, kompozycja, światło, kolory, głębia ostrości, wartości estetyczne."
            }
        else:
            prompts = {
                "comprehensive": "Analyze this image in detail. Describe all visible elements, scene, objects, people, colors, lighting, text and mood. Provide complete analysis.",
                "objects": "Identify and describe ALL objects in this image. For each provide: name, position, size, condition, color and material.",
                "scene": "Describe the scene in detail: where is this, what situation, what's happening, time of day/year.",
                "text": "Find and transcribe EXACTLY all text, signs, symbols visible in this image. Preserve formatting.",
                "artistic": "Perform professional artistic analysis: photographic style, technique, composition, light, colors, depth of field, aesthetic values."
            }
        
        return prompts.get(analysis_type, prompts["comprehensive"])

# ═══════════════════════════════════════════════════════════════════════════
# GŁÓWNA APLIKACJA COLAB
# ═══════════════════════════════════════════════════════════════════════════

class ColabImageRecognitionApp:
    """Główna aplikacja dla Google Colab"""
    
    def __init__(self):
        self.ai_client = None
        self.analysis_history = []
        self.api_configured = False
    
    def setup(self):
        """Konfiguracja aplikacji"""
        print("\n" + "="*70)
        print("🖼️  IMAGE RECOGNITION AI - GOOGLE COLAB")
        print("Zasilane przez GPT-5-mini Vision")
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
        
        self.ai_client = ColabImageRecognitionAI(api_key)
        self.api_configured = True
        
        print("✅ Konfiguracja zakończona pomyślnie!")
        print("💡 Wskazówka: Używaj obrazów dobrej jakości dla lepszych wyników\n")
        
        # Automatycznie uruchom tryb interaktywny
        self.interactive_mode()
        
        return True
    
    def _get_api_key(self):
        """Pobierz klucz API - NAPRAWIONE importy"""
        api_key = None
        
        # Próba 1: Secrets w Colab (bezpieczny import)
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
            print("\n" + "─"*50)
            print("🎯 MENU GŁÓWNE:")
            print("1. 🔍 Analizuj obraz")
            print("2. 📝 Wyodrębnij tekst (OCR)")
            print("3. 🎨 Analiza artystyczna")
            print("4. 📋 Historia analiz")
            print("5. 💾 Eksportuj wyniki")
            print("6. 🚪 Zakończ")
            
            try:
                choice = input("\n🔢 Wybierz opcję (1-6): ").strip()
                
                if choice == "1":
                    self.analyze_single_image()
                elif choice == "2":
                    self.extract_text_mode()
                elif choice == "3":
                    self.artistic_analysis_mode()
                elif choice == "4":
                    self.show_history()
                elif choice == "5":
                    self.export_results()
                elif choice == "6":
                    print("\n👋 Dziękujemy za korzystanie z Image Recognition AI!")
                    break
                else:
                    print("❌ Nieprawidłowa opcja. Wybierz 1-6.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Sesja zakończona przez użytkownika.")
                break
            except Exception as e:
                print(f"❌ Błąd: {e}")
    
    def analyze_single_image(self):
        """Analizuj pojedynczy obraz"""
        print("\n" + "="*50)
        print("🔍 ANALIZA OBRAZU")
        print("="*50)
        
        image_input = self.get_image_input()
        if not image_input:
            return
        
        # Wybierz typ analizy
        print("\n📊 Typ analizy:")
        print("1. Kompleksowa (pełna analiza)")
        print("2. Obiekty (lista przedmiotów)")
        print("3. Scena (kontekst i sytuacja)")
        
        type_choice = input("Wybierz (1-3, Enter=1): ").strip() or "1"
        analysis_types = {"1": "comprehensive", "2": "objects", "3": "scene"}
        analysis_type = analysis_types.get(type_choice, "comprehensive")
        
        print(f"\n⏳ Analizuję obraz ({analysis_type})...")
        result = self.ai_client.analyze_image(image_input, analysis_type, "polish")
        
        if result["success"]:
            print("\n" + "="*50)
            print("🖼️  WYNIK ANALIZY:")
            print("="*50)
            print(result["analysis"])
            print("="*50)
            
            # Zapisz w historii
            self.analysis_history.append({
                "type": "analysis",
                "analysis_type": analysis_type,
                "input": str(image_input)[:50] + "...",
                "result": result["analysis"],
                "timestamp": result["timestamp"]
            })
            
            print("\n✅ Analiza zapisana w historii!")
        else:
            print(f"\n❌ Błąd: {result.get('error', 'Nieznany błąd')}")
    
    def extract_text_mode(self):
        """Wyodrębnij tekst z obrazu (OCR)"""
        print("\n" + "="*50)
        print("📝 WYODRĘBNIANIE TEKSTU (OCR)")
        print("="*50)
        
        image_input = self.get_image_input()
        if not image_input:
            return
        
        print("\n⏳ Rozpoznaję tekst...")
        result = self.ai_client.analyze_image(image_input, "text", "polish")
        
        if result["success"]:
            print("\n" + "="*50)
            print("📝 WYODRĘBNIONY TEKST:")
            print("="*50)
            print(result["analysis"])
            print("="*50)
            
            self.analysis_history.append({
                "type": "ocr",
                "input": str(image_input)[:50] + "...",
                "result": result["analysis"],
                "timestamp": result["timestamp"]
            })
            
            print("\n✅ Tekst wyodrębniony!")
        else:
            print(f"\n❌ Błąd OCR: {result.get('error', 'Nieznany błąd')}")
    
    def artistic_analysis_mode(self):
        """Analiza artystyczna obrazu"""
        print("\n" + "="*50)
        print("🎨 ANALIZA ARTYSTYCZNA")
        print("="*50)
        
        image_input = self.get_image_input()
        if not image_input:
            return
        
        print("\n⏳ Wykonuję analizę artystyczną...")
        result = self.ai_client.analyze_image(image_input, "artistic", "polish")
        
        if result["success"]:
            print("\n" + "="*50)
            print("🎨 ANALIZA ARTYSTYCZNA:")
            print("="*50)
            print(result["analysis"])
            print("="*50)
            
            self.analysis_history.append({
                "type": "artistic",
                "input": str(image_input)[:50] + "...",
                "result": result["analysis"],
                "timestamp": result["timestamp"]
            })
            
            print("\n✅ Analiza zapisana!")
        else:
            print(f"\n❌ Błąd: {result.get('error', 'Nieznany błąd')}")
    
    def get_image_input(self):
        """Pobierz obraz od użytkownika - NAPRAWIONE importy"""
        print("\n📂 Źródło obrazu:")
        print("1. URL (link do obrazu)")
        print("2. Upload pliku (przeciągnij do Files)")
        
        choice = input("Wybierz (1-2): ").strip()
        
        if choice == "1":
            url = input("🌐 Podaj URL obrazu: ").strip()
            if url and url.startswith(('http://', 'https://')):
                return url
            else:
                print("❌ Nieprawidłowy URL!")
                return None
                
        elif choice == "2":
            if is_colab():
                try:
                    # Bezpieczny import google.colab.files
                    import importlib
                    files_module = importlib.import_module('google.colab.files')
                    
                    print("\n📤 Upload pliku obrazu:")
                    uploaded = files_module.upload()
                    
                    if uploaded:
                        filename = list(uploaded.keys())[0]
                        print(f"✅ Uploaded: {filename}")
                        return filename
                    else:
                        print("❌ Brak uploaded pliku!")
                        return None
                        
                except Exception as e:
                    print(f"❌ Błąd uploadu: {e}")
                    return None
            else:
                # Lokalne środowisko
                file_path = input("📁 Podaj ścieżkę do pliku: ").strip().strip('"\'')
                if os.path.exists(file_path):
                    return file_path
                else:
                    print("❌ Plik nie istnieje!")
                    return None
        
        print("❌ Nieprawidłowy wybór!")
        return None
    
    def show_history(self):
        """Pokaż historię analiz"""
        if not self.analysis_history:
            print("\n📋 Brak analiz w historii tej sesji.")
            return
        
        print(f"\n📋 HISTORIA ANALIZ ({len(self.analysis_history)} elementów):")
        print("="*50)
        
        for i, item in enumerate(self.analysis_history, 1):
            print(f"\n{i}. {item['type'].upper()}")
            if 'analysis_type' in item:
                print(f"   Typ: {item['analysis_type']}")
            print(f"   Źródło: {item['input']}")
            print(f"   Wynik: {item['result'][:100]}...")
            print(f"   Czas: {item['timestamp'][:19]}")
        
        print("="*50)
    
    def export_results(self):
        """Eksportuj wyniki do JSON"""
        if not self.analysis_history:
            print("❌ Brak danych do eksportu.")
            return
        
        try:
            filename = f"image_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                "export_time": datetime.now().isoformat(),
                "total_analyses": len(self.analysis_history),
                "analyses": self.analysis_history
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Wyeksportowano do: {filename}")
            
            if is_colab():
                print("\n💡 Pobierz plik:")
                print("   1. Kliknij ikonę plików w lewym pasku")
                print("   2. Znajdź plik i kliknij ⋮ → Download")
                
        except Exception as e:
            print(f"❌ Eksport nie powiódł się: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# AUTOMATYCZNE URUCHOMIENIE
# ═══════════════════════════════════════════════════════════════════════════

# Inicjalizuj aplikację
app = ColabImageRecognitionApp()

# Publiczne funkcje dla szybkiego dostępu
def setup():
    """Uruchom aplikację (główna funkcja)"""
    return app.setup()

def analyze(image_input, analysis_type="comprehensive"):
    """Szybka analiza obrazu
    
    Args:
        image_input: URL lub ścieżka do pliku
        analysis_type: "comprehensive", "objects", "scene", "text", "artistic"
    """
    if not app.api_configured:
        print("❌ Najpierw uruchom setup()!")
        return None
    
    return app.ai_client.analyze_image(image_input, analysis_type, "polish")

def history():
    """Pokaż historię analiz"""
    app.show_history()

def export():
    """Eksportuj wyniki"""
    app.export_results()

# ═══════════════════════════════════════════════════════════════════════════
# WYŚWIETL INSTRUKCJE
# ═══════════════════════════════════════════════════════════════════════════

if is_colab():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                  🖼️  IMAGE RECOGNITION AI - COLAB                         ║
╚═══════════════════════════════════════════════════════════════════════════╝

⚡ SZYBKI START:
   
   setup()    # ← URUCHOM TO NAJPIERW!
   
   Aplikacja automatycznie uruchomi się w trybie interaktywnym.

📋 FUNKCJE RĘCZNE (opcjonalne):

   analyze("url_lub_plik")      # Szybka analiza
   analyze("url", "objects")    # Analiza obiektów
   history()                    # Pokaż historię
   export()                     # Eksportuj wyniki

🔑 KONFIGURACJA KLUCZA API:

   Kliknij 🔑 w lewym pasku → dodaj sekret "OPENAI_API_KEY"

═══════════════════════════════════════════════════════════════════════════════
""")
else:
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║              🖼️  IMAGE RECOGNITION AI - LOKALNE                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

📋 DOSTĘPNE FUNKCJE:

   setup()                      # Konfiguracja i uruchomienie
   analyze("path_or_url")       # Analiza obrazu
   history()                    # Historia
   export()                     # Eksport

═══════════════════════════════════════════════════════════════════════════════
""")
