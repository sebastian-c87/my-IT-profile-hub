"""
Social Media Post Generator - Google Colab Version  
Standalone version optimized for Google Colab environment
Auto-interactive mode for better Colab experience
"""

import subprocess
import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

def is_colab_environment():
    """Check if running in Google Colab environment"""
    try:
        # Check for Colab-specific modules without importing them
        return 'google.colab' in sys.modules or 'COLAB_GPU' in os.environ
    except:
        return False

def install_if_colab():
    """Install packages only if in Colab environment"""
    if is_colab_environment():
        print("📦 Google Colab wykryto - Instalowanie wymaganych pakietów...")
        try:
            packages = ["openai>=1.0.0", "requests>=2.28.0"]
            for package in packages:
                print(f"Instalowanie {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("✅ Wszystkie pakiety zainstalowane!")
        except Exception as e:
            print(f"⚠️ Ostrzeżenie instalacji pakietów: {e}")
    else:
        print("💻 Środowisko lokalne wykryte")

# Install packages if needed
install_if_colab()

# Now import OpenAI
try:
    from openai import OpenAI
except ImportError:
    print("❌ Pakiet OpenAI nie znaleziony. Zainstaluj go: pip install openai")
    sys.exit(1)

class ColabSocialMediaAI:
    """Colab-optimized GPT-5-nano client with Polish language support"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
    
    def generate_post(self, topic: str, platform: str = "universal", 
                     style: str = "engaging", max_length: int = 300,
                     language: str = "polish") -> str:
        """Generate social media post using GPT-5-nano in Polish with better error handling"""
        try:
            # Language settings
            if language == "polish":
                lang_instruction = "Napisz post w języku polskim"
                tone_desc = "naturalnym, polskim stylem"
            else:
                lang_instruction = "Write the post in English"
                tone_desc = "natural English style"
            
            # Platform specifications
            platform_specs = {
                "twitter": "post na Twitter (max 280 znaków) z hashtagami",
                "linkedin": "profesjonalny post na LinkedIn z biznesowym fokusem",
                "facebook": "angażujący post na Facebook zachęcający do interakcji",
                "instagram": "post na Instagram z naciskiem na wizualizację i hashtagi",
                "universal": "uniwersalny post w social media"
            }
            
            spec = platform_specs.get(platform, platform_specs["universal"])
            
            # Simplified prompt for better reliability
            system_instructions = f"""{lang_instruction}. Stwórz {style} {spec}.
            
            Wymagania:
            - Maksymalnie {max_length} znaków
            - Ton {style} w {tone_desc}
            - Dołącz 2-3 emotikony
            - Dodaj 1-2 hashtagi
            - Zakończ pytaniem lub wezwaniem do działania
            
            Zwróć TYLKO treść posta."""
            
            user_input = f"Temat: {topic}"
            
            print(f"🔄 Próba 1: Generowanie z web search...")
            
            # First attempt - with web search
            try:
                response = self.client.responses.create(
                    model="gpt-5-nano",
                    input=user_input,
                    instructions=system_instructions,
                    tools=[{"type": "web_search"}],
                    reasoning={"effort": "low"},
                    text={"verbosity": "low"},
                    max_output_tokens=200,  # NAPRAWIONE: zmniejszone z 15000 na 200
                    timeout=30
                )
                
                # NAPRAWIONE: usunięte nawiasy () z output_text
                generated_content = response.output_text.strip()
                
                if generated_content and len(generated_content) > 10:
                    print("✅ Sukces z web search")
                    return self._validate_and_clean_content(generated_content, max_length, topic, language)
                else:
                    print("⚠️ Pusta odpowiedź z web search, próbuje bez...")
                    
            except Exception as e:
                print(f"⚠️ Web search nie powiódł się: {str(e)}")
                print("🔄 Próba 2: Generowanie bez web search...")
            
            # Second attempt - without web search
            try:
                response = self.client.responses.create(
                    model="gpt-5-nano",
                    input=user_input,
                    instructions=system_instructions,
                    reasoning={"effort": "low"},
                    text={"verbosity": "low"},
                    max_output_tokens=150,
                    timeout=20
                )
                
                generated_content = response.output_text.strip()
                
                if generated_content and len(generated_content) > 10:
                    print("✅ Sukces bez web search")
                    return self._validate_and_clean_content(generated_content, max_length, topic, language)
                else:
                    print("⚠️ Pusta odpowiedź, próbuje uproszczony prompt...")
                    
            except Exception as e:
                print(f"⚠️ Standardowa generacja nie powiodła się: {str(e)}")
                print("🔄 Próba 3: Uproszczony prompt...")
            
            # Third attempt - simplified prompt
            try:
                simple_prompt = f"Napisz krótki post na {platform} o temacie: {topic}. Styl: {style}. Max {max_length} znaków. Dodaj hashtag."
                
                response = self.client.responses.create(
                    model="gpt-5-nano",
                    input=simple_prompt,
                    reasoning={"effort": "low"},
                    text={"verbosity": "low"},
                    max_output_tokens=100,
                    timeout=15
                )
                
                generated_content = response.output_text.strip()
                
                if generated_content and len(generated_content) > 5:
                    print("✅ Sukces z uproszczonym promptem")
                    return self._validate_and_clean_content(generated_content, max_length, topic, language)
                    
            except Exception as e:
                print(f"⚠️ Uproszczony prompt nie powiódł się: {str(e)}")
                print("🔄 Użycie fallback template...")
            
            # Final fallback - template
            return self._create_fallback_post(topic, platform, style, language)
            
        except Exception as e:
            print(f"❌ Krytyczny błąd: {str(e)}")
            return self._create_fallback_post(topic, platform, style, language)
    
    def _validate_and_clean_content(self, content: str, max_length: int, topic: str, language: str) -> str:
        """Validate and clean generated content"""
        if len(content) > max_length:
            if '#' in content:
                # Try to preserve hashtags
                parts = content.rsplit('#', 1)
                if len(parts[0].strip()) <= max_length - 15:
                    content = parts[0].strip() + ' #' + parts[1].split()[0]
                else:
                    content = content[:max_length-3] + "..."
            else:
                content = content[:max_length-3] + "..."
        
        return content
    
    def _create_fallback_post(self, topic: str, platform: str, style: str, language: str) -> str:
        """Create fallback post when API fails"""
        print("🔄 Używam template fallback...")
        
        if language == "polish":
            if style == "professional":
                return f"💼 {topic} - kluczowy temat w dzisiejszej branży. Jakie są Wasze doświadczenia? #{topic.replace(' ', '')[:10].lower()}"
            elif style == "humorous":
                return f"😄 Kiedy ktoś mówi o {topic}... czy to tylko ja, czy wszyscy robimy tę samą minę? 🤔 #{topic.replace(' ', '')[:10].lower()}"
            elif style == "casual":
                return f"💭 {topic} to naprawdę ciekawy temat! Kto ma jakieś przemyślenia na ten temat? #{topic.replace(' ', '')[:10].lower()}"
            else:  # engaging
                return f"🚀 {topic} - co o tym myślicie? Podzielcie się swoimi opiniami! #{topic.replace(' ', '')[:10].lower()}"
        else:
            if style == "professional":
                return f"💼 {topic} - a key topic in today's industry. What are your experiences? #{topic.replace(' ', '')[:10].lower()}"
            elif style == "humorous":
                return f"😄 When someone mentions {topic}... is it just me or does everyone make that face? 🤔 #{topic.replace(' ', '')[:10].lower()}"
            elif style == "casual":
                return f"💭 {topic} is really interesting! Anyone have thoughts on this? #{topic.replace(' ', '')[:10].lower()}"
            else:  # engaging
                return f"🚀 {topic} - what do you think? Share your opinions! #{topic.replace(' ', '')[:10].lower()}"

class ColabSocialMediaGenerator:
    """Main Colab application class with Polish interface"""
    
    def __init__(self):
        self.ai_client = None
        self.posts_generated = []
        self.language = "polish"
        self.api_configured = False
    
    def setup(self):
        """Setup for Colab environment"""
        print("\n🚀 Konfiguracja Generatora Postów Social Media")
        print("=" * 60)
        
        # Get API key using safe method
        api_key = self._get_api_key_safely()
        
        if not api_key:
            print("❌ Klucz API jest wymagany!")
            return False
        
        self.ai_client = ColabSocialMediaAI(api_key)
        self.api_configured = True
        print("✅ Konfiguracja zakończona pomyślnie!")
        
        # Auto-start interactive mode in Colab
        if is_colab_environment():
            print("\n🎯 Automatyczne uruchomienie trybu interaktywnego...")
            self.auto_interactive_colab()
        
        return True
    
    def _get_api_key_safely(self):
        """Safely get API key without import errors"""
        api_key = None
        
        # Try Colab secrets only if in Colab environment
        if is_colab_environment():
            try:
                # NAPRAWIONE: bezpieczny import google.colab
                import importlib
                colab_userdata = importlib.import_module('google.colab.userdata')
                api_key = colab_userdata.get('OPENAI_API_KEY')
                print("✅ Klucz API wczytany z sekretów Colab")
            except Exception as e:
                print(f"⚠️ Nie można wczytać z sekretów Colab: {e}")
                pass
        
        # Fallback to manual input
        if not api_key:
            api_key = input("🔑 Wprowadź swój klucz API OpenAI: ").strip()
        
        return api_key
    
    def auto_interactive_colab(self):
        """Auto-interactive mode specifically for Colab"""
        print("\n" + "="*50)
        print("🎮 INTERAKTYWNY GENERATOR POSTÓW")
        print("="*50)
        
        while True:
            print("\n📋 OPCJE:")
            print("1. 📝 Generuj pojedynczy post")
            print("2. 📚 Generuj wiele postów")
            print("3. 📋 Pokaż historię")
            print("4. 💾 Eksportuj posty")
            print("5. 🚪 Zakończ")
            
            try:
                wybor = input("\n🔢 Wybierz opcję (1-5): ").strip()
                
                if wybor == "1":
                    self.quick_single_generation()
                elif wybor == "2":
                    self.quick_batch_generation()
                elif wybor == "3":
                    self.show_history()
                elif wybor == "4":
                    self.export_to_json()
                elif wybor == "5":
                    print("👋 Dziękujemy za korzystanie z generatora!")
                    break
                else:
                    print("❌ Nieprawidłowa opcja. Wybierz 1-5.")
                    
            except KeyboardInterrupt:
                print("\n👋 Sesja zakończona przez użytkownika.")
                break
            except Exception as e:
                print(f"❌ Błąd: {str(e)}")
    
    def quick_single_generation(self):
        """Quick single post generation for Colab"""
        print("\n📝 SZYBKIE GENEROWANIE POSTA")
        print("-" * 30)
        
        # Quick topic input
        temat = input("📌 Podaj temat: ").strip()
        if not temat:
            print("❌ Temat jest wymagany!")
            return
        
        # Quick platform selection
        print("\n🌐 Platformy: 1-Twitter, 2-LinkedIn, 3-Facebook, 4-Instagram, 5-Uniwersalny")
        platform_choice = input("Wybierz (1-5, domyślnie 5): ").strip() or "5"
        
        platforms = {"1": "twitter", "2": "linkedin", "3": "facebook", "4": "instagram", "5": "universal"}
        platform = platforms.get(platform_choice, "universal")
        
        # Quick style selection
        print("\n🎨 Style: 1-Profesjonalny, 2-Angażujący, 3-Swobodny, 4-Humorystyczny")
        style_choice = input("Wybierz (1-4, domyślnie 2): ").strip() or "2"
        
        styles = {"1": "professional", "2": "engaging", "3": "casual", "4": "humorous"}
        style = styles.get(style_choice, "engaging")
        
        # Generate
        print(f"\n⏳ Generuję post na {platform}...")
        post = self.ai_client.generate_post(temat, platform, style, language="polish")
        
        # Display result
        print(f"\n📱 WYGENEROWANY POST:")
        print("="*40)
        print(post)
        print("="*40)
        print(f"📊 Znaków: {len(post)}")
        
        # Save to history
        self.posts_generated.append({
            "temat": temat,
            "platform": platform,
            "style": style,
            "content": post,
            "character_count": len(post),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        print("✅ Post zapisany w historii!")
    
    def quick_batch_generation(self):
        """Quick batch generation for Colab"""
        print("\n📚 GENEROWANIE WIELU POSTÓW")
        print("-" * 30)
        
        # Input topics
        tematy_input = input("📝 Podaj tematy oddzielone przecinkami: ").strip()
        if not tematy_input:
            print("❌ Brak tematów!")
            return
        
        tematy = [t.strip() for t in tematy_input.split(",") if t.strip()]
        
        if len(tematy) > 5:
            potwierdz = input(f"⚠️ {len(tematy)} tematów może zająć chwilę. Kontynuować? (t/N): ")
            if not potwierdz.lower().startswith('t'):
                return
        
        # Quick settings
        platform = "universal"
        style = "engaging"
        
        print(f"\n⏳ Generuję {len(tematy)} postów...")
        
        wyniki = []
        for i, temat in enumerate(tematy, 1):
            print(f"📝 Post {i}/{len(tematy)}: {temat[:20]}...")
            
            post = self.ai_client.generate_post(temat, platform, style, language="polish")
            
            wynik = {
                "temat": temat,
                "content": post,
                "character_count": len(post)
            }
            wyniki.append(wynik)
            
            print(f"✅ Gotowe ({len(post)} znaków)")
        
        # Display results
        print(f"\n📱 WYNIKI ({len(wyniki)} postów):")
        print("="*50)
        
        for i, wynik in enumerate(wyniki, 1):
            print(f"\n📝 POST {i}: {wynik['temat']}")
            print("-"*30)
            print(wynik['content'])
            print(f"📊 Znaków: {wynik['character_count']}")
        
        print("="*50)
        
        # Save all to history
        for wynik in wyniki:
            self.posts_generated.append({
                **wynik,
                "platform": platform,
                "style": style,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        print(f"✅ Wszystkie {len(wyniki)} postów zapisane w historii!")
    
    def show_history(self):
        """Display generated posts history in Polish"""
        if not self.posts_generated:
            print("\n📋 Brak wygenerowanych postów w tej sesji.")
            return
        
        print(f"\n📋 HISTORIA SESJI ({len(self.posts_generated)} postów):")
        print("=" * 50)
        
        for i, post in enumerate(self.posts_generated, 1):
            print(f"\n{i}. 📝 {post['temat']}")
            print(f"   Platform: {post.get('platform', 'N/A')} | Styl: {post.get('style', 'N/A')}")
            print(f"   Treść: {post['content'][:50]}...")
            print(f"   Znaków: {post.get('character_count', 0)}")
            if 'timestamp' in post:
                print(f"   Czas: {post['timestamp']}")
        
        print("=" * 50)
    
    def export_to_json(self):
        """Export posts to JSON format"""
        if not self.posts_generated:
            print("❌ Brak postów do eksportu.")
            return None
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_posts": len(self.posts_generated),
            "posts": self.posts_generated
        }
        
        filename = f"posty_social_media_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Wyeksportowano {len(self.posts_generated)} postów do {filename}")
        
        # In Colab, also display download link
        if is_colab_environment():
            print("📥 Plik został zapisany. Użyj Files panel po lewej stronie aby go pobrać.")
        
        return filename

# Initialize the generator
generator = ColabSocialMediaGenerator()

# Public functions for Colab users (Polish interface)
def setup():
    """Konfiguracja generatora - GŁÓWNA FUNKCJA STARTOWA"""
    return generator.setup()

def generuj_post(temat, platforma="universal", styl="engaging", max_znakow=300):
    """Szybka funkcja generowania"""
    if not generator.api_configured:
        print("❌ Proszę najpierw uruchomić setup()!")
        return None
    
    return generator.ai_client.generate_post(temat, platforma, styl, max_znakow)

def tryb_interaktywny():
    """Uruchom tryb interaktywny"""
    if not generator.api_configured:
        print("❌ Proszę najpierw uruchomić setup()!")
        return
    
    generator.auto_interactive_colab()

def generuj_wsadowo(tematy, platforma="universal", styl="engaging"):
    """Generuj wiele postów na raz"""
    if not generator.api_configured:
        print("❌ Proszę najpierw uruchomić setup()!")
        return None
    
    if isinstance(tematy, str):
        tematy = [t.strip() for t in tematy.split(',')]
    
    wyniki = []
    for temat in tematy:
        post = generator.ai_client.generate_post(temat, platforma, styl, language="polish")
        wyniki.append({"temat": temat, "content": post})
    
    return wyniki

def pokaz_historie():
    """Pokaż historię sesji"""
    generator.show_history()

def eksportuj_posty():
    """Eksportuj posty do pliku"""
    return generator.export_to_json()

# English aliases for compatibility
generate_post = generuj_post
interactive_mode = tryb_interaktywny
batch_generate = generuj_wsadowo
show_history = pokaz_historie
export_posts = eksportuj_posty

# Display different instructions based on environment
if is_colab_environment():
    print("""
🚀 GENERATOR POSTÓW SOCIAL MEDIA - COLAB GOTOWY!

⚡ SZYBKI START:
   setup()    # <- URUCHOM TO NAJPIERW!

💡 Ta wersja automatycznie uruchomi tryb interaktywny po konfiguracji.
🎮 Będziesz mógł generować posty przez intuicyjne menu.

📋 RĘCZNE FUNKCJE (opcjonalne):
2. generuj_post("twój temat")                       # Pojedynczy post
3. generuj_wsadowo(["temat1", "temat2"])           # Wiele postów
4. pokaz_historie()                                # Historia sesji
5. eksportuj_posty()                               # Zapis do pliku
""")
else:
    print("""
🚀 GENERATOR POSTÓW SOCIAL MEDIA - GOTOWY!

📋 INSTRUKCJA UŻYCIA:
1. setup()                                          # Konfiguracja API
2. generuj_post("twój temat")                       # Pojedynczy post
3. tryb_interaktywny()                              # Interfejs interaktywny
4. generuj_wsadowo(["temat1", "temat2"])           # Wiele postów
5. pokaz_historie()                                # Wyświetl wygenerowane posty
6. eksportuj_posty()                               # Zapisz do pliku

💡 PRZYKŁAD:
   setup()
   post = generuj_post("Legia Warszawa Liga Konferencji", "twitter", "swobodny")
   print(post)

🌍 DOSTĘPNE TAKŻE W JĘZYKU ANGIELSKIM:
   generate_post(), interactive_mode(), batch_generate(), show_history(), export_posts()
""")
