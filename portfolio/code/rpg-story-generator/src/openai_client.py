"""
Klient OpenAI GPT-5-nano jako Mistrz Gry RPG
"""
import logging
from typing import Dict, Any, Optional, List
from openai import OpenAI

from config import Config

class RPGGameMaster:
    """Mistrz Gry RPG zasilany przez GPT-5-nano"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.logger = logging.getLogger(__name__)
    
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
            
            self.logger.info(f"Generuję intro dla gatunku: {genre}, trudność: {difficulty}")
            
            response = self.client.responses.create(
                model=self.config.model_name,
                instructions=system_instructions,
                input=user_prompt,
                reasoning={"effort": self.config.reasoning_effort},
                text={"verbosity": self.config.text_verbosity},
                max_output_tokens=self.config.max_output_tokens
            )
            
            story_text = self._extract_text(response)
            
            return {
                "story": story_text,
                "genre": genre,
                "difficulty": difficulty,
                "success": True,
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Błąd generowania intro: {str(e)}", exc_info=True)
            return {
                "error": f"Nie udało się wygenerować intro: {str(e)}",
                "success": False,
                "timestamp": self._get_timestamp()
            }
    
    def continue_story(
        self,
        genre: str,
        difficulty: str,
        story_context: str,
        player_action: str
    ) -> Dict[str, Any]:
        """Kontynuuj historię na podstawie akcji gracza"""
        try:
            system_instructions = self._build_game_master_prompt(genre, difficulty)
            
            # Ogranicz kontekst
            trimmed_context = story_context[-self.config.max_story_context:] if len(story_context) > self.config.max_story_context else story_context
            
            user_prompt = self._build_continuation_prompt(trimmed_context, player_action)
            
            self.logger.info(f"Kontynuuję historię - akcja gracza: {player_action[:50]}...")
            
            response = self.client.responses.create(
                model=self.config.model_name,
                instructions=system_instructions,
                input=user_prompt,
                reasoning={"effort": self.config.reasoning_effort},
                text={"verbosity": self.config.text_verbosity},
                max_output_tokens=self.config.max_output_tokens
            )
            
            story_text = self._extract_text(response)
            
            return {
                "story": story_text,
                "player_action": player_action,
                "success": True,
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Błąd kontynuacji historii: {str(e)}", exc_info=True)
            return {
                "error": f"Nie udało się kontynuować historii: {str(e)}",
                "success": False,
                "timestamp": self._get_timestamp()
            }
    
    def _build_game_master_prompt(self, genre: str, difficulty: str) -> str:
        """Zbuduj system prompt dla Mistrza Gry - ULEPSZONE PROWADZENIE"""
        difficulty_descriptions = {
            "Łatwy": "Świat jest przyjazny, gracze mają szczęście w krytycznych momentach",
            "Średni": "Świat jest zbalansowany, wyzwania wymagają przemyślanych decyzji",
            "Trudny": "Świat jest niebezpieczny, decyzje mają poważne konsekwencje",
            "Hardcore": "Świat jest bezlitosny, każda decyzja może być ostatnia"
        }
        
        return f"""Jesteś **Mistrzem Gry RPG** - profesjonalnym narratorem prowadzącym immersyjną grę fabularną w gatunku **{genre}**.

═══════════════════════════════════════════════════════════════════════
TWOJA GŁÓWNA ROLA:
═══════════════════════════════════════════════════════════════════════

**TY PROWADZISZ GRĘ!** To Ty opisujesz świat, tworzysz sceny, wprowadzasz postacie i sytuacje.
Gracze reagują na TO CO TY OPISUJESZ, a nie odwrotnie!

POZIOM TRUDNOŚCI: **{difficulty}**
{difficulty_descriptions.get(difficulty, "")}

═══════════════════════════════════════════════════════════════════════
JAK PROWADZIĆ GRĘ:
═══════════════════════════════════════════════════════════════════════

1. **OPISZ SZCZEGÓŁOWO SCENĘ**
   • Gdzie znajdują się gracze? (lokacja, otoczenie, atmosfera)
   • Co widzą, słyszą, czują? (zmysły!)
   • Kto jest obecny? (postacie, stworzenia)
   • Co się dzieje w tej chwili?

2. **WPROWADŹ WYDARZENIE LUB KONFLIKT**
   • Pojawia się nowa postać z informacją/prośbą
   • Dzieje się coś niespodziewanego
   • Odkrycie czegoś ważnego
   • Zagrożenie lub wyzwanie

3. **POSTACI NIEZALEŻNE (NPC)**
   • Twórz żywe postacie z własnymi celami
   • Używaj dialogów - postacie mówią, pytają, proponują
   • Opisz ich wygląd, zachowanie, emocje
   • Nadaj im osobowość i motywacje

4. **PRZEDSTAW 3-4 KONKRETNE OPCJE DZIAŁANIA**
   Zawsze zakończ opisem sytuacji i jasnym przedstawieniem możliwości:
   
   **CO MOŻESZ ZROBIĆ:**
   
   1) [Opcja akcji] - opis co się może stać
   2) [Opcja akcji] - opis konsekwencji
   3) [Opcja akcji] - opis możliwości
   4) Możesz też opisać własną akcję!
   
   **Jak zamierzasz postąpić?**

═══════════════════════════════════════════════════════════════════════
STYL NARRACJI:
═══════════════════════════════════════════════════════════════════════

✓ **Żywy język** - używaj metafor, porównań, epitetów
✓ **Wszystkie zmysły** - wzrok, słuch, dotyk, zapach, smak
✓ **Emocje** - strach, podekscytowanie, napięcie, radość
✓ **Szczegóły** - konkretne nazwy, liczby, kolory, dźwięki
✓ **Dialogi** - postacie mówią swoimi słowami
✓ **Dynamika** - coś się DZIEJE, świat żyje!

═══════════════════════════════════════════════════════════════════════
STRUKTURA ODPOWIEDZI (OBOWIĄZKOWA):
═══════════════════════════════════════════════════════════════════════

**[REAKCJA NA AKCJĘ GRACZA]** (jeśli gracze coś zrobili)
Opisz konsekwencje ich działania - co się stało przez ich akcję.

**[SZCZEGÓŁOWY OPIS OBECNEJ SCENY]**
• Lokacja i otoczenie (3-4 zdania z detalami)
• Atmosfera i nastrój
• Co się teraz dzieje

**[POSTACIE I DIALOG]** (jeśli są obecne)
Przedstaw postacie, ich wygląd, zachowanie i wypowiedzi.
Przykład: "Brodaty karzel odwraca się gwałtownie. 'Kim jesteś, przybyszu? Co cię tu sprowadza?' - jego głos brzmi podejrzliwie."

**[WYDARZENIE/KONFLIKT]**
Coś się dzieje! Pojawia się wyzwanie, zagadka, zagrożenie lub okazja.

**[OPCJE DZIAŁANIA]**
Przedstaw 3-4 konkretne możliwości + opcję własnej akcji.

═══════════════════════════════════════════════════════════════════════
WYMAGANIA TECHNICZNE:
═══════════════════════════════════════════════════════════════════════

• Minimum {self.config.min_story_length} słów w każdej odpowiedzi
• Zawsze kończ pytaniem o decyzję gracza
• Pamiętaj wydarzenia z przeszłości
• Rozwijaj wątki poboczne
• Bądź kreatywny ale logiczny dla {genre}

**BARDZO WAŻNE:** 
- Nie przerywaj w połowie zdania!
- Zawsze zakończ pełną sceną z opcjami!
- PROWADŹ GRĘ - to Ty jesteś narratorem!
- Gracze reagują na TWOJE opisy!"""
    
    def _build_intro_prompt(self, initial_scenario: str) -> str:
        """Zbuduj prompt dla wprowadzenia - ULEPSZONE"""
        return f"""POCZĄTKOWA SYTUACJA BOHATERA/BOHATERÓW:
{initial_scenario}

═══════════════════════════════════════════════════════════════════════
TWOJE ZADANIE - ROZPOCZNIJ GRĘ:
═══════════════════════════════════════════════════════════════════════

Stwórz EPICKIE WPROWADZENIE do gry RPG. Rozpocznij przygodę w tej sytuacji.

MUSISZ ZAWRZEĆ:

1. **Szczegółowy opis miejsca** (gdzie są gracze, jak wygląda otoczenie)
2. **Stan bohaterów** (co czują, w jakim są stanie)
3. **Pierwsze wydarzenie** - coś się dzieje od razu!
4. **Wprowadzenie konfliktu** - zapowiedź przygody/zagrożenia
5. **Pierwszą postać NPC** - ktoś pojawia się lub jest już obecny
6. **3-4 opcje działania** dla graczy

Opisz wszystko żywo, z detalami, wykorzystując zmysły.
Niech gracze POCZUJĄ świat gry od pierwszego zdania!

ZAKOŃCZ koniecznie listą opcji działania i pytaniem co gracze zamierzają zrobić."""
    
    def _build_continuation_prompt(self, story_context: str, player_action: str) -> str:
        """Zbuduj prompt dla kontynuacji - ULEPSZONE"""
        return f"""DOTYCHCZASOWA HISTORIA:
{story_context}

AKCJA GRACZY:
{player_action}

═══════════════════════════════════════════════════════════════════════
KONTYNUUJ GRĘ:
═══════════════════════════════════════════════════════════════════════

Zareaguj na akcję graczy i rozwiń historię dalej.

MUSISZ ZAWRZEĆ:

1. **Reakcję świata** - co się stało przez akcję graczy?
2. **Konsekwencje** - jak świat i postacie reagują?
3. **Nową scenę** - gdzie gracze są teraz, co widzą?
4. **Nowe wydarzenie** - co się teraz dzieje?
5. **Postaci NPC** - jeśli są obecne, co mówią/robią?
6. **3-4 nowe opcje działania** dla graczy

Pamiętaj:
- Rozwijaj wątki z poprzednich tur
- Wprowadź nowe elementy (postacie, lokacje, tajemnice)
- Stwórz napięcie lub zaskoczenie
- Opisz wszystko szczegółowo i obrazowo

ZAKOŃCZ listą opcji działania i pytaniem co gracze zamierzają zrobić."""
    
    def _extract_text(self, response) -> str:
        """Wyciągnij tekst z odpowiedzi API - NAPRAWIONE"""
        story_text = ""
        
        # POPRAWIONE: Właściwe sprawdzanie pól
        if hasattr(response, 'output_text') and response.output_text:
            story_text = str(response.output_text).strip()
        
        # Jeśli dalej puste - sprawdź alternatywne pola
        if not story_text:
            if hasattr(response, 'output') and response.output:
                if isinstance(response.output, str):
                    story_text = response.output.strip()
                elif hasattr(response.output, 'text'):
                    story_text = str(response.output.text).strip()
        
        # Logowanie jeśli puste
        if not story_text:
            self.logger.error(f"Pusta odpowiedź od modelu!")
            self.logger.error(f"Response type: {type(response)}")
            self.logger.error(f"Response attributes: {dir(response)}")
            
            # Spróbuj model_dump
            if hasattr(response, 'model_dump'):
                dump = response.model_dump()
                self.logger.error(f"Response dump: {dump}")
            
            story_text = """[BŁĄD GENEROWANIA]

Mistrz Gry napotkał problem z generowaniem historii. 
Możliwe przyczyny:
- Zbyt krótki limit tokenów (max_output_tokens)
- Problem z połączeniem API
- Nieoczekiwany format odpowiedzi

Spróbuj ponownie lub zmień akcję."""
        
        return story_text
    
    def _get_timestamp(self) -> str:
        """Pobierz timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
