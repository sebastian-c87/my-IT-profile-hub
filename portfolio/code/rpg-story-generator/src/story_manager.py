"""
Zarządzanie historią gry i zapisem sesji
"""
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class StoryManager:
    """Manager do zarządzania historią gry RPG"""
    
    def __init__(self):
        self.story_history: List[Dict[str, Any]] = []
        self.current_session: Optional[Dict[str, Any]] = None
        self.logger = logging.getLogger(__name__)
        
        # Upewnij się że folder saves/ istnieje
        self.saves_dir = Path("saves")
        self.saves_dir.mkdir(exist_ok=True)
    
    def start_new_session(
        self,
        genre: str,
        difficulty: str,
        initial_scenario: str,
        intro_story: str
    ):
        """Rozpocznij nową sesję gry"""
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "genre": genre,
            "difficulty": difficulty,
            "initial_scenario": initial_scenario,
            "start_time": datetime.now().isoformat(),
            "turns": []
        }
        
        # Dodaj intro jako pierwszy turn
        self.add_turn(
            turn_number=0,
            player_action="[ROZPOCZĘCIE GRY]",
            story_response=intro_story
        )
        
        self.logger.info(f"Rozpoczęto nową sesję: {self.current_session['session_id']}")
    
    def add_turn(self, turn_number: int, player_action: str, story_response: str):
        """Dodaj nową turę do historii"""
        if not self.current_session:
            self.logger.warning("Brak aktywnej sesji!")
            return
        
        turn = {
            "turn": turn_number,
            "timestamp": datetime.now().isoformat(),
            "player_action": player_action,
            "story_response": story_response
        }
        
        self.current_session["turns"].append(turn)
        self.story_history.append(turn)
    
    def get_story_context(self, max_turns: int = 5) -> str:
        """
        Pobierz kontekst ostatnich tur dla AI
        
        Args:
            max_turns: Maksymalna liczba ostatnich tur do uwzględnienia
        
        Returns:
            Sformatowany kontekst historii
        """
        if not self.current_session or not self.current_session["turns"]:
            return ""
        
        # Weź ostatnie N tur
        recent_turns = self.current_session["turns"][-max_turns:]
        
        context_parts = []
        for turn in recent_turns:
            if turn["turn"] == 0:
                context_parts.append(f"[INTRO]\n{turn['story_response']}\n")
            else:
                context_parts.append(
                    f"[TURA {turn['turn']}]\n"
                    f"Akcja gracza: {turn['player_action']}\n"
                    f"Historia: {turn['story_response']}\n"
                )
        
        return "\n".join(context_parts)
    
    def get_full_story(self) -> str:
        """Pobierz pełną historię sesji jako tekst"""
        if not self.current_session:
            return "Brak aktywnej sesji."
        
        story_parts = [
            "="*70,
            f"🎮 SESJA GRY RPG",
            "="*70,
            f"Gatunek: {self.current_session['genre']}",
            f"Trudność: {self.current_session['difficulty']}",
            f"Data rozpoczęcia: {self.current_session['start_time'][:19]}",
            f"Liczba tur: {len(self.current_session['turns'])}",
            "="*70,
            ""
        ]
        
        for turn in self.current_session["turns"]:
            if turn["turn"] == 0:
                story_parts.append("📖 WPROWADZENIE:")
                story_parts.append("")
                story_parts.append(turn["story_response"])
                story_parts.append("")
                story_parts.append("-"*70)
                story_parts.append("")
            else:
                story_parts.append(f"⚔️ TURA {turn['turn']}:")
                story_parts.append("")
                story_parts.append(f"🎲 Akcja gracza: {turn['player_action']}")
                story_parts.append("")
                story_parts.append(f"📜 Historia:")
                story_parts.append(turn["story_response"])
                story_parts.append("")
                story_parts.append("-"*70)
                story_parts.append("")
        
        return "\n".join(story_parts)
    
    def save_session(self, filename: Optional[str] = None) -> str:
        """
        Zapisz sesję do pliku JSON
        
        Args:
            filename: Opcjonalna nazwa pliku (domyślnie: session_id.json)
        
        Returns:
            Ścieżka do zapisanego pliku
        """
        if not self.current_session:
            raise ValueError("Brak aktywnej sesji do zapisu!")
        
        if filename is None:
            filename = f"session_{self.current_session['session_id']}.json"
        
        filepath = self.saves_dir / filename
        
        # Dodaj czas zakończenia
        save_data = self.current_session.copy()
        save_data["end_time"] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Sesja zapisana: {filepath}")
        return str(filepath)
    
    def load_session(self, filepath: str):
        """Wczytaj zapisaną sesję"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.current_session = json.load(f)
        
        # Odtwórz story_history
        self.story_history = self.current_session["turns"].copy()
        
        self.logger.info(f"Sesja wczytana: {filepath}")
    
    def list_saved_sessions(self) -> List[Dict[str, str]]:
        """Lista wszystkich zapisanych sesji"""
        sessions = []
        
        for filepath in self.saves_dir.glob("session_*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        "filename": filepath.name,
                        "session_id": data.get("session_id", "unknown"),
                        "genre": data.get("genre", "unknown"),
                        "start_time": data.get("start_time", "unknown"),
                        "turns": len(data.get("turns", []))
                    })
            except Exception as e:
                self.logger.warning(f"Błąd odczytu sesji {filepath}: {e}")
        
        return sorted(sessions, key=lambda x: x["start_time"], reverse=True)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Pobierz statystyki obecnej sesji"""
        if not self.current_session:
            return {}
        
        turns = self.current_session["turns"]
        
        total_words = sum(
            len(turn["story_response"].split()) 
            for turn in turns
        )
        
        return {
            "session_id": self.current_session["session_id"],
            "genre": self.current_session["genre"],
            "difficulty": self.current_session["difficulty"],
            "total_turns": len(turns),
            "total_words": total_words,
            "start_time": self.current_session["start_time"],
        }
