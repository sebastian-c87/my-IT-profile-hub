"""
RPG Story Generator - Główna aplikacja
Interaktywna gra fabularna z AI jako Mistrzem Gry
"""
import os
import sys
import logging
from typing import Optional

from config import config
from openai_client import RPGGameMaster
from story_manager import StoryManager

# Konfiguracja logowania
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class RPGStoryGeneratorApp:
    """Główna aplikacja generatora historii RPG"""
    
    def __init__(self):
        self.game_master = RPGGameMaster(config)
        self.story_manager = StoryManager()
        self.logger = logging.getLogger(__name__)
        
        # Stan gry
        self.current_genre: Optional[str] = None
        self.current_difficulty: Optional[str] = None
        self.turn_counter: int = 0
        self.game_active: bool = False
    
    def run(self):
        """Uruchom aplikację"""
        self._display_welcome()
        
        while True:
            try:
                if not self.game_active:
                    choice = self._show_main_menu()
                    
                    if choice == "1":
                        self.start_new_game()
                    elif choice == "2":
                        self.load_game()
                    elif choice == "3":
                        self.show_saved_games()
                    elif choice == "4":
                        self.show_help()
                    elif choice == "5":
                        self._display_goodbye()
                        break
                    else:
                        print("❌ Nieprawidłowa opcja. Wybierz 1-5.")
                else:
                    # Gra aktywna - gracz wykonuje akcje
                    self.play_turn()
                
            except KeyboardInterrupt:
                print("\n\n👋 Gra zakończona przez użytkownika.")
                if self.game_active:
                    self._prompt_save_game()
                break
            except Exception as e:
                self.logger.error(f"Błąd aplikacji: {str(e)}", exc_info=True)
                print(f"\n❌ Wystąpił błąd: {str(e)}")
                input("\nNaciśnij Enter aby kontynuować...")
    
    def _display_welcome(self):
        """Wyświetl ekran powitalny"""
        print("\n" + "="*70)
        print("🎮  RPG STORY GENERATOR")
        print("Interaktywna gra fabularna zasilana przez GPT-5-nano")
        print("="*70)
        print("\n✨ Witaj w świecie nieograniczonych przygód!")
        print("🤖 Twój Mistrz Gry AI poprowadzi Cię przez epicką historię")
        print("🎲 Każda decyzja ma znaczenie - Twoje wybory kształtują fabułę")
        print("\n💡 Wskazówka: Opisuj swoje akcje szczegółowo dla lepszych rezultatów")
        print("="*70 + "\n")
    
    def _show_main_menu(self) -> str:
        """Pokaż menu główne"""
        print("\n" + "─"*70)
        print("🎯 MENU GŁÓWNE:")
        print("─"*70)
        print("1. 🆕 Nowa gra")
        print("2. 💾 Wczytaj grę")
        print("3. 📋 Zapisane gry")
        print("4. ❓ Pomoc")
        print("5. 🚪 Zakończ")
        print("─"*70)
        
        return input("\n🔢 Wybierz opcję (1-5): ").strip()
    
    def start_new_game(self):
        """Rozpocznij nową grę"""
        print("\n" + "="*70)
        print("🆕 NOWA GRA")
        print("="*70)
        
        # Wybór gatunku
        genre = self._select_genre()
        if not genre:
            return
        
        # Wybór trudności
        difficulty = self._select_difficulty()
        if not difficulty:
            return
        
        # Opis początkowej sytuacji
        print(f"\n📝 Wybrano: {genre} | Trudność: {difficulty}")
        print("\n💬 Opisz początkową sytuację Twojego bohatera:")
        print("   (np. 'Jestem rycerzem poszukującym zaginionego artefaktu')")
        print("   (naciśnij Enter aby zakończyć opis)")
        print()
        
        initial_scenario = input("   > ").strip()
        
        if not initial_scenario:
            print("❌ Nie podano opisu sytuacji!")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        # Generuj intro
        print("\n⏳ Mistrz Gry przygotowuje świat...")
        print("🎲 To może potrwać chwilę...")
        
        result = self.game_master.generate_story_intro(
            genre=genre,
            initial_scenario=initial_scenario,
            difficulty=difficulty
        )
        
        if result["success"]:
            # Rozpocznij sesję
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
            
            # Wyświetl intro
            print("\n" + "="*70)
            print("📖 TWOJA PRZYGODA ROZPOCZYNA SIĘ...")
            print("="*70)
            print()
            print(result["story"])
            print()
            print("="*70)
            print("\n✅ Gra rozpoczęta! Co chcesz zrobić?")
            input("\nNaciśnij Enter aby kontynuować...")
        else:
            print(f"\n❌ Błąd: {result.get('error', 'Nieznany błąd')}")
            input("\nNaciśnij Enter aby kontynuować...")
    
    def play_turn(self):
        """Zagraj turę - gracz wykonuje akcję"""
        print("\n" + "─"*70)
        print(f"⚔️ TURA {self.turn_counter + 1}")
        print("─"*70)
        
        # Menu akcji gracza
        print("\n🎲 TWÓJ RUCH:")
        print()
        print("  📌 Wybierz jedną z opcji zaproponowanych przez Mistrza Gry")
        print("     (wpisz numer opcji, np. '1', '2', '3'...)")
        print()
        print("  📝 LUB opisz swoją własną akcję")
        print("     (np. 'Podchodzę ostrożnie do okna i wyglądam na zewnątrz')")
        print()
        print("  ⚙️  Specjalne komendy:")
        print("     • 'menu' - otwórz menu gry")
        print("     • 'statystyki' - zobacz statystyki sesji")
        print("     • 'exit' - zakończ grę i wyjdź")
        print()
        print("─"*70)
        
        player_action = input("➤ Twoja akcja: ").strip()
        
        # Specjalne komendy
        if player_action.lower() == "exit":
            print("\n⚠️  Wychodzisz z gry...")
            if self._confirm_quit():
                self._prompt_save_game()
                self.game_active = False
            return
        elif player_action.lower() == "menu":
            self._show_game_menu()
            return
        elif player_action.lower() == "statystyki":
            self._show_stats()
            return
        elif not player_action:
            print("❌ Nie podano akcji!")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        # Kontynuuj historię
        print("\n⏳ Mistrz Gry rozważa Twoją akcję...")
        
        story_context = self.story_manager.get_story_context(max_turns=5)
        
        result = self.game_master.continue_story(
            genre=self.current_genre,
            difficulty=self.current_difficulty,
            story_context=story_context,
            player_action=player_action
        )
        
        if result["success"]:
            self.turn_counter += 1
            
            # Dodaj turę do historii
            self.story_manager.add_turn(
                turn_number=self.turn_counter,
                player_action=player_action,
                story_response=result["story"]
            )
            
            # Wyświetl odpowiedź Mistrza Gry
            print("\n" + "="*70)
            print("📜 MISTRZ GRY:")
            print("="*70)
            print()
            print(result["story"])
            print()
            print("="*70)
            
            input("\nNaciśnij Enter aby kontynuować...")
        else:
            print(f"\n❌ Błąd: {result.get('error', 'Nieznany błąd')}")
            input("\nNaciśnij Enter aby kontynuować...")
    
    def _show_game_menu(self):
        """Pokaż menu podczas gry"""
        while True:
            print("\n" + "─"*70)
            print("🎮 MENU GRY:")
            print("─"*70)
            print("1. ↩️  Powrót do gry")
            print("2. 💾 Zapisz grę")
            print("3. 📊 Statystyki sesji")
            print("4. 📖 Pełna historia")
            print("5. 🚪 Zakończ grę")
            print("─"*70)
            
            choice = input("\n🔢 Wybierz opcję (1-5): ").strip()
            
            if choice == "1":
                return
            elif choice == "2":
                self._save_game()
            elif choice == "3":
                self._show_stats()
            elif choice == "4":
                self._show_full_story()
            elif choice == "5":
                if self._confirm_quit():
                    self._prompt_save_game()
                    self.game_active = False
                    return
            else:
                print("❌ Nieprawidłowa opcja.")
    
    def _save_game(self):
        """Zapisz grę"""
        try:
            filepath = self.story_manager.save_session()
            print(f"\n✅ Gra zapisana: {filepath}")
        except Exception as e:
            print(f"\n❌ Błąd zapisu: {e}")
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def _show_stats(self):
        """Pokaż statystyki sesji"""
        stats = self.story_manager.get_session_stats()
        
        if not stats:
            print("\n❌ Brak statystyk.")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        print("\n" + "="*70)
        print("📊 STATYSTYKI SESJI")
        print("="*70)
        print(f"🎮 ID Sesji: {stats['session_id']}")
        print(f"🎭 Gatunek: {stats['genre']}")
        print(f"⚔️  Trudność: {stats['difficulty']}")
        print(f"🔢 Liczba tur: {stats['total_turns']}")
        print(f"📝 Całkowita liczba słów: {stats['total_words']}")
        print(f"⏰ Rozpoczęto: {stats['start_time'][:19]}")
        print("="*70)
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def _show_full_story(self):
        """Pokaż pełną historię"""
        full_story = self.story_manager.get_full_story()
        
        print("\n" + full_story)
        
        # Opcja zapisu do pliku
        save_txt = input("\n💾 Zapisać historię do pliku TXT? (T/n): ").strip().upper()
        if save_txt != "N":
            try:
                from datetime import datetime
                filename = f"historia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(full_story)
                
                print(f"✅ Historia zapisana: {filename}")
            except Exception as e:
                print(f"❌ Błąd zapisu: {e}")
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def _prompt_save_game(self):
        """Zapytaj czy zapisać grę przed wyjściem"""
        save = input("\n💾 Zapisać grę przed zakończeniem? (T/n): ").strip().upper()
        if save != "N":
            self._save_game()
    
    def _confirm_quit(self) -> bool:
        """Potwierdź zakończenie gry"""
        confirm = input("\n⚠️  Czy na pewno zakończyć grę? (t/N): ").strip().upper()
        return confirm == "T"
    
    def load_game(self):
        """Wczytaj zapisaną grę"""
        sessions = self.story_manager.list_saved_sessions()
        
        if not sessions:
            print("\n❌ Brak zapisanych gier!")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        print("\n" + "="*70)
        print("💾 ZAPISANE GRY")
        print("="*70)
        
        for idx, session in enumerate(sessions, 1):
            print(f"\n{idx}. {session['filename']}")
            print(f"   Gatunek: {session['genre']}")
            print(f"   Data: {session['start_time'][:19]}")
            print(f"   Tur: {session['turns']}")
        
        print("\n" + "─"*70)
        
        try:
            choice = input(f"\n🔢 Wybierz grę (1-{len(sessions)}, 0=anuluj): ").strip()
            choice_idx = int(choice) - 1
            
            if choice == "0":
                return
            
            if 0 <= choice_idx < len(sessions):
                session = sessions[choice_idx]
                filepath = self.story_manager.saves_dir / session['filename']
                
                print(f"\n⏳ Wczytuję grę...")
                self.story_manager.load_session(str(filepath))
                
                # Odtwórz stan gry
                self.current_genre = self.story_manager.current_session['genre']
                self.current_difficulty = self.story_manager.current_session['difficulty']
                self.turn_counter = len(self.story_manager.current_session['turns']) - 1
                self.game_active = True
                
                print(f"✅ Gra wczytana: {session['filename']}")
                print(f"🎮 Kontynuujesz od tury {self.turn_counter}")
                
                # Pokaż ostatni fragment historii
                if self.turn_counter > 0:
                    last_turn = self.story_manager.current_session['turns'][-1]
                    print("\n📖 Ostatnie wydarzenia:")
                    print("-"*70)
                    print(last_turn['story_response'][:500] + "...")
                    print("-"*70)
                
                input("\nNaciśnij Enter aby kontynuować...")
            else:
                print("❌ Nieprawidłowy wybór!")
        except ValueError:
            print("❌ Wprowadź numer!")
        except Exception as e:
            print(f"❌ Błąd wczytywania: {e}")
        
        input("\nNaciśnij Enter aby kontynuować...")
    
    def show_saved_games(self):
        """Pokaż listę zapisanych gier"""
        sessions = self.story_manager.list_saved_sessions()
        
        if not sessions:
            print("\n❌ Brak zapisanych gier!")
            input("\nNaciśnij Enter aby kontynuować...")
            return
        
        print("\n" + "="*70)
        print(f"📋 ZAPISANE GRY ({len(sessions)})")
        print("="*70)
        
        for idx, session in enumerate(sessions, 1):
            print(f"\n{idx}. **{session['filename']}**")
            print(f"   📁 ID: {session['session_id']}")
            print(f"   🎭 Gatunek: {session['genre']}")
            print(f"   ⏰ Data: {session['start_time'][:19]}")
            print(f"   🔢 Tur: {session['turns']}")
        
        print("\n" + "="*70)
        input("\nNaciśnij Enter aby kontynuować...")
    
    def show_help(self):
        """Pokaż pomoc"""
        print("\n" + "="*70)
        print("❓ POMOC - RPG STORY GENERATOR")
        print("="*70)
        
        help_text = """
**JAK GRAĆ:**

1. **Rozpocznij nową grę** - wybierz gatunek i trudność
2. **Opisz bohatera** - podaj początkową sytuację
3. **Czytaj historię** - Mistrz Gry opisze świat
4. **Podejmuj decyzje** - opisz co chce zrobić Twój bohater
5. **Obserwuj konsekwencje** - każda akcja ma znaczenie!

**GATUNKI:**
"""
        for genre in config.genres:
            help_text += f"  • {genre}\n"
        
        help_text += "\n**POZIOMY TRUDNOŚCI:**\n"
        for diff in config.difficulties:
            help_text += f"  • {diff}\n"
        
        help_text += """
**WSKAZÓWKI:**

✓ Opisuj akcje szczegółowo - im więcej detali, tym lepsza historia
✓ Bądź kreatywny - Mistrz Gry doceni nietypowe pomysły
✓ Rozmawiaj z postaciami - zadawaj pytania, negocjuj
✓ Eksploruj świat - odkrywaj nowe miejsca i tajemnice
✓ Pamiętaj o zapisywaniu - nigdy nie wiesz co się stanie!

**SPECJALNE KOMENDY (podczas gry):**

  • 'menu' - otwórz menu gry
  • 'statystyki' - zobacz statystyki sesji

**UWAGI:**

⚠️  Historia jest generowana w czasie rzeczywistym przez AI
⚠️  Każda gra jest unikalna - nie ma dwóch takich samych przygód
⚠️  Zapisz grę często - generowanie może zająć chwilę
"""
        
        print(help_text)
        print("="*70)
        input("\nNaciśnij Enter aby powrócić do menu...")
    
    def _select_genre(self) -> Optional[str]:
        """Wybór gatunku"""
        print("\n🎭 Wybierz gatunek gry:")
        print("─"*70)
        
        for idx, genre in enumerate(config.genres, 1):
            print(f"  {idx}. {genre}")
        
        print("─"*70)
        
        try:
            choice = input(f"\n🔢 Wybierz (1-{len(config.genres)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(config.genres):
                return config.genres[choice_idx]
            else:
                print("❌ Nieprawidłowy wybór!")
                return None
        except ValueError:
            print("❌ Wprowadź numer!")
            return None
    
    def _select_difficulty(self) -> Optional[str]:
        """Wybór trudności"""
        print("\n⚔️ Wybierz poziom trudności:")
        print("─"*70)
        
        for idx, diff in enumerate(config.difficulties, 1):
            print(f"  {idx}. {diff}")
        
        print("─"*70)
        
        try:
            choice = input(f"\n🔢 Wybierz (1-{len(config.difficulties)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(config.difficulties):
                return config.difficulties[choice_idx]
            else:
                print("❌ Nieprawidłowy wybór!")
                return None
        except ValueError:
            print("❌ Wprowadź numer!")
            return None
    
    def _display_goodbye(self):
        """Wyświetl komunikat pożegnalny"""
        print("\n" + "="*70)
        print("👋 DZIĘKUJEMY ZA GRĘ!")
        print("="*70)
        print("\n🎮 Mamy nadzieję że podobała Ci się przygoda!")
        print("🌟 Wróć wkrótce po nowe historie!")
        print("\n" + "="*70 + "\n")

# ═══════════════════════════════════════════════════════════════════════════
# GŁÓWNA FUNKCJA URUCHOMIENIA
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Główna funkcja aplikacji"""
    try:
        app = RPGStoryGeneratorApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Gra zakończona.")
    except Exception as e:
        print(f"\n❌ Krytyczny błąd aplikacji: {str(e)}")
        logging.error(f"Krytyczny błąd: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
