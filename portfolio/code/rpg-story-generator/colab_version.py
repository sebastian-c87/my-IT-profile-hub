"""
═══════════════════════════════════════════════════════════════════════════════
🎮 RPG STORY GENERATOR - GOOGLE COLAB VERSION
═══════════════════════════════════════════════════════════════════════════════

INSTRUKCJA URUCHOMIENIA W GOOGLE COLAB:

1. 🔑 DODAJ KLUCZ API:
   
   Opcja A - Secrets (zalecane):
   • Kliknij ikonę klucza (🔑) w lewym pasku Colab
   • Dodaj nowy sekret: Name = "OPENAI_API_KEY", Value = "twój-klucz-api"
   • Włącz przełącznik "Notebook access"
   
   Opcja B - Bezpośrednio w kodzie:
   • Odkomentuj linię poniżej i wklej swój klucz:
   # os.environ['OPENAI_API_KEY'] = 'sk-...'

2. ▶️ URUCHOM APLIKACJĘ:
   
   setup()  # ← URUCHOM TO NAJPIERW!
   
   Aplikacja automatycznie uruchomi się w trybie interaktywnym.

3. 🎮 JAK GRAĆ:
   
   • Wybierz gatunek (Fantasy, Sci-Fi, Horror, etc.)
   • Wybierz poziom trudności
   • Opisz początkową sytuację bohatera
   • Mistrz Gry stworzy świat i wprowadzi Cię w przygodę!
   • Wybieraj opcje (wpisz numer) lub opisuj własne akcje
   • Historia rozwija się na podstawie Twoich decyzji!

4. 💾 ZAPISYWANIE:
   
   • Używaj komendy 'menu' podczas gry → 'Zapisz grę'
   • Pliki są dostępne w sekcji Files (📁) w lewym pasku
   • Możesz pobrać je klikając prawym → Download

═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

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
        "openai>=1.0.0"
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
    reasoning_effort: str = "high"
    text_verbosity: str = "high"
    max_output_tokens: int = 3000
    
    # Story Configuration
    max_story_context: int = 4000
    min_story_length: int = 300
    
    # Game Settings
    genres = (
        "Fantasy",
        "Sci-Fi",
        "Horror",
        "Postapokalipsa",
        "Cyberpunk",
        "Steampunk",
        "Noir",
        "Superhero"
    )
    
    difficulties = (
        "Łatwy",
        "Średni",
        "Trudny",
        "Hardcore"
    )

config = ColabConfig()

# ═══════════════════════════════════════════════════════════════════════════
# GAME MASTER - MISTRZ GRY AI
# ═══════════════════════════════════════════════════════════════════════════

class ColabRPGGameMaster:
    """Mistrz Gry RPG dla Colab"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def generate_story_intro(
        self,
        genre: str,
        initial_scenario: str,
        difficulty: str
    ) -> Dict[str, Any]:
        """Generuj wprowadzenie do gry"""
        try:
            system_instructions = self._build_game_master_prompt(genre, difficulty)
            user_prompt = self._build_intro_prompt(initial_scenario)
            
            self.logger.info(f"Generuję intro: {genre}, {difficulty}")
            
            response = self.client.responses.create(
                model=config.model_name,
                instructions=system_instructions,
                input=user_prompt,
                reasoning={"effort": config.reasoning_effort},
                text={"verbosity": config.text_verbosity},
                max_output_tokens=config.max_output_tokens
            )
            
            story_text = self._extract_text(response)
            
            return {
                "story": story_text,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Błąd intro: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def continue_story(
        self,
        genre: str,
        difficulty: str,
        story_context: str,
        player_action: str
    ) -> Dict[str, Any]:
        """Kontynuuj historię"""
        try:
            system_instructions = self._build_game_master_prompt(genre, difficulty)
            
            trimmed_context = story_context[-config.max_story_context:] if len(story_context) > config.max_story_context else story_context
            
            user_prompt = self._build_continuation_prompt(trimmed_context, player_action)
            
            response = self.client.responses.create(
                model=config.model_name,
                instructions=system_instructions,
                input=user_prompt,
                reasoning={"effort": config.reasoning_effort},
                text={"verbosity": config.text_verbosity},
                max_output_tokens=config.max_output_tokens
            )
            
            story_text = self._extract_text(response)
            
            return {
                "story": story_text,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Błąd kontynuacji: {str(e)}")
            return {
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def _build_game_master_prompt(self, genre: str, difficulty: str) -> str:
        """System prompt dla Mistrza Gry"""
        difficulty_descriptions = {
            "Łatwy": "Świat jest przyjazny, gracze mają szczęście",
            "Średni": "Świat jest zbalansowany, wyzwania wymagają przemyślenia",
            "Trudny": "Świat jest niebezpieczny, decyzje mają poważne konsekwencje",
            "Hardcore": "Świat jest bezlitosny, każda decyzja może być ostatnia"
        }
        
        return f"""Jesteś **Mistrzem Gry RPG** prowadzącym grę w gatunku **{genre}**.

POZIOM TRUDNOŚCI: **{difficulty}** - {difficulty_descriptions.get(difficulty, "")}

TY PROWADZISZ GRĘ! Opisujesz świat, tworzysz sceny, wprowadzasz postacie i sytuacje.

STRUKTURA ODPOWIEDZI:

1. **SZCZEGÓŁOWY OPIS SCENY** (gdzie są gracze, co widzą, słyszą, czują)
2. **POSTACIE I DIALOG** (NPC, ich wygląd, zachowanie, wypowiedzi)
3. **WYDARZENIE/KONFLIKT** (coś się dzieje - wyzwanie, zagadka, zagrożenie)
4. **OPCJE DZIAŁANIA** (3-4 konkretne możliwości + opcja własnej akcji)

STYL:
✓ Żywy, obrazowy język
✓ Wszystkie zmysły (wzrok, słuch, dotyk, zapach)
✓ Emocje i napięcie
✓ Dialogi postaci
✓ Minimum {config.min_story_length} słów

ZAKOŃCZ ZAWSZE:
**CO MOŻESZ ZROBIĆ:**
1) [opcja] - konsekwencje
2) [opcja] - konsekwencje
3) [opcja] - konsekwencje
4) Możesz też opisać własną akcję!

**Jak zamierzasz postąpić?**"""
    
    def _build_intro_prompt(self, initial_scenario: str) -> str:
        """Prompt dla wprowadzenia"""
        return f"""POCZĄTKOWA SYTUACJA:
{initial_scenario}

Stwórz EPICKIE WPROWADZENIE do gry RPG. Opisz:
1. Szczegółowe miejsce
2. Stan bohatera
3. Pierwsze wydarzenie
4. Konflikt/wyzwanie
5. Pierwszą postać NPC
6. 3-4 opcje działania

Zakończ listą opcji i pytaniem."""
    
    def _build_continuation_prompt(self, story_context: str, player_action: str) -> str:
        """Prompt dla kontynuacji"""
        return f"""HISTORIA:
{story_context}

AKCJA GRACZA:
{player_action}

Kontynuuj historię. Opisz:
1. Reakcję świata na akcję
2. Konsekwencje
3. Nową scenę
4. Nowe wydarzenie
5. Postacie NPC
6. 3-4 nowe opcje

Zakończ listą opcji i pytaniem."""
    
    def _extract_text(self, response) -> str:
        """Wyciągnij tekst z odpowiedzi"""
        if hasattr(response, 'output_text') and response.output_text:
            return str(response.output_text).strip()
        return "Błąd generowania historii. Spróbuj ponownie."

# ═══════════════════════════════════════════════════════════════════════════
# STORY MANAGER
# ═══════════════════════════════════════════════════════════════════════════

class ColabStoryManager:
    """Manager historii dla Colab"""
    
    def __init__(self):
        self.current_session: Optional[Dict[str, Any]] = None
    
    def start_new_session(self, genre: str, difficulty: str, initial_scenario: str, intro_story: str):
        """Rozpocznij nową sesję"""
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "genre": genre,
            "difficulty": difficulty,
            "initial_scenario": initial_scenario,
            "start_time": datetime.now().isoformat(),
            "turns": []
        }
        
        self.add_turn(0, "[ROZPOCZĘCIE GRY]", intro_story)
    
    def add_turn(self, turn_number: int, player_action: str, story_response: str):
        """Dodaj turę"""
        if not self.current_session:
            return
        
        self.current_session["turns"].append({
            "turn": turn_number,
            "timestamp": datetime.now().isoformat(),
            "player_action": player_action,
            "story_response": story_response
        })
    
    def get_story_context(self, max_turns: int = 5) -> str:
        """Pobierz kontekst ostatnich tur"""
        if not self.current_session:
            return ""
        
        recent_turns = self.current_session["turns"][-max_turns:]
        
        context_parts = []
        for turn in recent_turns:
            if turn["turn"] == 0:
                context_parts.append(f"[INTRO]\n{turn['story_response']}\n")
            else:
                context_parts.append(
                    f"[TURA {turn['turn']}]\n"
                    f"Akcja: {turn['player_action']}\n"
                    f"Historia: {turn['story_response']}\n"
                )
        
        return "\n".join(context_parts)
    
    def save_session(self) -> str:
        """Zapisz sesję do JSON"""
        if not self.current_session:
            raise ValueError("Brak sesji!")
        
        filename = f"rpg_session_{self.current_session['session_id']}.json"
        
        save_data = self.current_session.copy()
        save_data["end_time"] = datetime.now().isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return filename

# ═══════════════════════════════════════════════════════════════════════════
# GŁÓWNA APLIKACJA COLAB
# ═══════════════════════════════════════════════════════════════════════════

class ColabRPGApp:
    """Główna aplikacja RPG dla Colab"""
    
    def __init__(self):
        self.game_master = None
        self.story_manager = ColabStoryManager()
        self.api_configured = False
        
        self.current_genre = None
        self.current_difficulty = None
        self.turn_counter = 0
        self.game_active = False
    
    def setup(self):
        """Konfiguracja i uruchomienie"""
        print("\n" + "="*70)
        print("🎮 RPG STORY GENERATOR - GOOGLE COLAB")
        print("Interaktywna gra fabularna z AI jako Mistrzem Gry")
        print("="*70 + "\n")
        
        api_key = self._get_api_key()
        if not api_key:
            print("❌ Klucz API OpenAI jest wymagany!")
            print("\n💡 Jak dodać klucz:")
            print("1. Kliknij ikonę klucza (🔑) w lewym pasku")
            print("2. Dodaj sekret: Name='OPENAI_API_KEY', Value='twój-klucz'")
            print("3. Włącz 'Notebook access'")
            print("4. Uruchom ponownie setup()")
            return False
        
        self.game_master = ColabRPGGameMaster(api_key)
        self.api_configured = True
        
        print("✅ Konfiguracja zakończona!\n")
        
        # Automatyczne uruchomienie
        self.run()
        
        return True
    
    def _get_api_key(self):
        """Pobierz klucz API"""
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
        
        # Próba 3: Input
        print("🔑 Klucz API nie znaleziony")
        api_key = input("Wprowadź klucz OpenAI API (lub Enter aby anulować): ").strip()
        
        return api_key if api_key else None
    
    def run(self):
        """Główna pętla gry"""
        while True:
            try:
                if not self.game_active:
                    choice = self._show_main_menu()
                    
                    if choice == "1":
                        self.start_new_game()
                    elif choice == "2":
                        self.show_help()
                    elif choice == "3":
                        print("\n👋 Do zobaczenia!")
                        break
                else:
                    self.play_turn()
                    
            except KeyboardInterrupt:
                print("\n\n👋 Sesja zakończona.")
                break
            except Exception as e:
                print(f"❌ Błąd: {e}")
    
    def _show_main_menu(self) -> str:
        """Menu główne"""
        print("\n" + "─"*70)
        print("🎯 MENU:")
        print("─"*70)
        print("1. 🆕 Nowa gra")
        print("2. ❓ Pomoc")
        print("3. 🚪 Zakończ")
        print("─"*70)
        
        return input("\n🔢 Wybór (1-3): ").strip()
    
    def start_new_game(self):
        """Rozpocznij nową grę"""
        print("\n" + "="*70)
        print("🆕 NOWA GRA")
        print("="*70)
        
        # Gatunek
        genre = self._select_genre()
        if not genre:
            return
        
        # Trudność
        difficulty = self._select_difficulty()
        if not difficulty:
            return
        
        # Scenariusz
        print(f"\n📝 Gatunek: {genre} | Trudność: {difficulty}")
        print("\n💬 Opisz początkową sytuację bohatera:")
        initial_scenario = input("   > ").strip()
        
        if not initial_scenario:
            print("❌ Brak opisu!")
            return
        
        print("\n⏳ Mistrz Gry tworzy świat...")
        
        result = self.game_master.generate_story_intro(
            genre=genre,
            initial_scenario=initial_scenario,
            difficulty=difficulty
        )
        
        if result["success"]:
            self.story_manager.start_new_session(
                genre=genre,
                difficulty=difficulty,
                initial_scenario=initial_scenario,
                intro_story=result["story"]
            )
            
            self.current_genre = genre
            self.current_difficulty = difficulty
            self.turn_counter = 0
            self.game_active = True
            
            print("\n" + "="*70)
            print("📖 TWOJA PRZYGODA ROZPOCZYNA SIĘ...")
            print("="*70)
            print()
            print(result["story"])
            print()
            print("="*70)
            input("\nEnter aby kontynuować...")
        else:
            print(f"\n❌ Błąd: {result.get('error')}")
    
    def play_turn(self):
        """Zagraj turę"""
        print("\n" + "─"*70)
        print(f"⚔️ TURA {self.turn_counter + 1}")
        print("─"*70)
        
        print("\n🎲 TWÓJ RUCH:")
        print("  • Wpisz numer opcji (np. '1', '2')")
        print("  • LUB opisz własną akcję")
        print("  • 'save' - zapisz grę")
        print("  • 'exit' - zakończ")
        
        player_action = input("\n➤ Akcja: ").strip()
        
        if player_action.lower() == "exit":
            self.game_active = False
            return
        elif player_action.lower() == "save":
            try:
                filename = self.story_manager.save_session()
                print(f"\n✅ Zapisano: {filename}")
            except Exception as e:
                print(f"❌ Błąd: {e}")
            input("\nEnter...")
            return
        elif not player_action:
            print("❌ Brak akcji!")
            return
        
        # Parsowanie akcji
        action_text = player_action
        if player_action.isdigit():
            action_text = f"Wybieram opcję {player_action}"
            print(f"✅ Wybrano: {player_action}")
        
        print("\n⏳ Mistrz Gry myśli...")
        
        story_context = self.story_manager.get_story_context(max_turns=5)
        
        result = self.game_master.continue_story(
            genre=self.current_genre,
            difficulty=self.current_difficulty,
            story_context=story_context,
            player_action=action_text
        )
        
        if result["success"]:
            self.turn_counter += 1
            
            self.story_manager.add_turn(
                turn_number=self.turn_counter,
                player_action=action_text,
                story_response=result["story"]
            )
            
            print("\n" + "="*70)
            print("📜 MISTRZ GRY:")
            print("="*70)
            print()
            print(result["story"])
            print()
            print("="*70)
            
            input("\nEnter...")
        else:
            print(f"\n❌ Błąd: {result.get('error')}")
    
    def _select_genre(self) -> Optional[str]:
        """Wybór gatunku"""
        print("\n🎭 Gatunek:")
        for idx, genre in enumerate(config.genres, 1):
            print(f"  {idx}. {genre}")
        
        try:
            choice = int(input(f"\nWybór (1-{len(config.genres)}): ")) - 1
            if 0 <= choice < len(config.genres):
                return config.genres[choice]
        except:
            pass
        return None
    
    def _select_difficulty(self) -> Optional[str]:
        """Wybór trudności"""
        print("\n⚔️ Trudność:")
        for idx, diff in enumerate(config.difficulties, 1):
            print(f"  {idx}. {diff}")
        
        try:
            choice = int(input(f"\nWybór (1-{len(config.difficulties)}): ")) - 1
            if 0 <= choice < len(config.difficulties):
                return config.difficulties[choice]
        except:
            pass
        return None
    
    def show_help(self):
        """Pomoc"""
        print("\n" + "="*70)
        print("❓ POMOC")
        print("="*70)
        print("""
JAK GRAĆ:
1. Rozpocznij nową grę
2. Wybierz gatunek i trudność
3. Opisz bohatera
4. Czytaj historie Mistrza Gry
5. Wybieraj opcje (numery) lub opisuj akcje
6. Zapisuj grę komendą 'save'

GATUNKI: Fantasy, Sci-Fi, Horror, Postapokalipsa, Cyberpunk, etc.
TRUDNOŚCI: Łatwy, Średni, Trudny, Hardcore

WSKAZÓWKI:
✓ Opisuj akcje szczegółowo
✓ Bądź kreatywny
✓ Rozmawiaj z postaciami
✓ Eksploruj świat
✓ Zapisuj często!
""")
        input("\nEnter...")

# ═══════════════════════════════════════════════════════════════════════════
# AUTOMATYCZNE URUCHOMIENIE
# ═══════════════════════════════════════════════════════════════════════════

app = ColabRPGApp()

def setup():
    """Uruchom grę (główna funkcja)"""
    return app.setup()

# ═══════════════════════════════════════════════════════════════════════════
# INSTRUKCJE WYŚWIETLANE
# ═══════════════════════════════════════════════════════════════════════════

if is_colab():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║              🎮 RPG STORY GENERATOR - COLAB                              ║
╚═══════════════════════════════════════════════════════════════════════════╝

⚡ SZYBKI START:
   
   setup()    # ← URUCHOM TO!
   
   Gra automatycznie się rozpocznie.

🔑 KONFIGURACJA KLUCZA:
   Kliknij 🔑 w lewym pasku → dodaj "OPENAI_API_KEY"

═══════════════════════════════════════════════════════════════════════════════
""")
else:
    print("📋 Uruchom: setup()")
