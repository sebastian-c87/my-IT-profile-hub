"""
Klient OpenAI GPT-5-nano z web search dla analizy prawnej
"""
import logging
from typing import Dict, Any, Optional
from openai import OpenAI

from config import Config

class LegalAIClient:
    """Klient GPT-5-nano z możliwością wyszukiwania prawnego"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.logger = logging.getLogger(__name__)
    
    def analyze_legal_problem(
        self,
        problem_description: str,
        legal_domain: str
    ) -> Dict[str, Any]:
        """
        Analizuj problem prawny użytkownika
        
        Args:
            problem_description: Opis problemu użytkownika
            legal_domain: Wybrana dziedzina prawa
        
        Returns:
            Dict z analizą prawną
        """
        try:
            # Zbuduj system prompt
            system_instructions = self._build_legal_system_prompt(legal_domain)
            
            # Zbuduj user prompt
            user_prompt = self._build_user_prompt(problem_description, legal_domain)
            
            # Właściwa konfiguracja web_search tools
            tools_config = [{"type": "web_search"}] if self.config.enable_web_search else None
            
            self.logger.info(f"Analizuję problem z dziedziny: {legal_domain}")
            
            # Wywołaj GPT-5-nano z Responses API
            response = self.client.responses.create(
                model=self.config.model_name,
                instructions=system_instructions,
                input=user_prompt,
                tools=tools_config,
                reasoning={"effort": self.config.reasoning_effort},
                text={"verbosity": self.config.text_verbosity},
                max_output_tokens=self.config.max_output_tokens
            )
            
            # NAPRAWIONE: Właściwe pole output_text
            legal_analysis = ""
            
            # Sprawdź output_text (główne pole w Responses API)
            if hasattr(response, 'output_text') and response.output_text:
                legal_analysis = str(response.output_text).strip()
            
            # Jeśli NADAL puste - sprawdź alternatywne pola
            if not legal_analysis:
                self.logger.warning("output_text jest puste, sprawdzam alternatywne pola...")
                
                # Sprawdź output
                if hasattr(response, 'output') and response.output:
                    if isinstance(response.output, str):
                        legal_analysis = response.output.strip()
                    elif hasattr(response.output, 'text'):
                        legal_analysis = str(response.output.text).strip()
                
                # Sprawdź content
                if not legal_analysis and hasattr(response, 'content'):
                    if isinstance(response.content, str):
                        legal_analysis = response.content.strip()
                    elif isinstance(response.content, list):
                        text_parts = []
                        for item in response.content:
                            if isinstance(item, str):
                                text_parts.append(item)
                            elif hasattr(item, 'text'):
                                text_parts.append(str(item.text))
                        legal_analysis = ' '.join(text_parts).strip()
            
            # Jeśli NADAL puste - loguj szczegóły i zwróć informację
            if not legal_analysis:
                self.logger.error(f"Pusta odpowiedź od modelu!")
                self.logger.error(f"Response type: {type(response)}")
                self.logger.error(f"Response attributes: {dir(response)}")
                self.logger.error(f"Response repr: {repr(response)}")
                
                # Spróbuj wyciągnąć raw response
                if hasattr(response, 'model_dump'):
                    self.logger.error(f"Response dump: {response.model_dump()}")
                
                legal_analysis = """Przepraszamy, model GPT-5-nano nie zwrócił analizy prawnej.

Możliwe przyczyny:
- Problem z połączeniem lub limitem API
- Model wymaga innego formatowania zapytania
- Przekroczono limit tokenów

Proszę spróbować ponownie lub skontaktować się z prawnikiem bezpośrednio."""
            
            # Dodaj rekomendację prawnika
            full_response = self._add_lawyer_recommendation(legal_analysis, legal_domain)
            
            return {
                "analysis": full_response,
                "legal_domain": legal_domain,
                "web_search_used": self.config.enable_web_search,
                "success": True,
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Błąd analizy prawnej: {str(e)}", exc_info=True)
            return {
                "error": f"Analiza nie powiodła się: {str(e)}",
                "success": False,
                "timestamp": self._get_timestamp()
            }
    
    def _build_legal_system_prompt(self, legal_domain: str) -> str:
        """Zbuduj system prompt dla analizy prawnej"""
        return f"""Jesteś ekspertem prawnym specjalizującym się w polskim prawie, szczególnie w dziedzinie: {legal_domain}.

Twoim zadaniem jest przeprowadzenie szczegółowej analizy prawnej problemu użytkownika.

STRUKTURA ODPOWIEDZI:

1. **PODSUMOWANIE SYTUACJI**
   Krótko opisz w 2-3 zdaniach istotę problemu prawnego

2. **WŁAŚCIWE PRZEPISY PRAWNE**
   Wymień konkretne artykuły i przepisy polskiego prawa które mają zastosowanie:
   - Podaj dokładne numery artykułów (np. art. 931 Kodeksu cywilnego)
   - Zacytuj kluczowe fragmenty przepisów
   - Odwołuj się TYLKO do rzeczywiście istniejących przepisów

3. **KOMENTARZ DO PRZEPISÓW**
   Wyjaśnij w prosty sposób:
   - Jak te przepisy odnoszą się do sytuacji użytkownika
   - Jakie prawa i obowiązki wynikają z tych przepisów
   - Jakie są możliwe interpretacje

4. **INSTRUKCJA DZIAŁANIA**
   Przedstaw krok po kroku co użytkownik powinien zrobić:
   - Krok 1: ...
   - Krok 2: ...
   - Krok 3: ...
   - itp.

WYMAGANIA:
- Używaj prostego, zrozumiałego języka
- Bądź konkretny i merytoryczny
- NIE wymyślaj przepisów - używaj tylko istniejących
- Zaznacz że to NIE jest porada prawna

WAŻNE: Musisz zwrócić kompletną analizę. NIE zostawiaj pustej odpowiedzi!"""
    
    def _build_user_prompt(self, problem_description: str, legal_domain: str) -> str:
        """Zbuduj prompt użytkownika"""
        return f"""Dziedzina prawa: {legal_domain}

Problem prawny do szczegółowej analizy:

{problem_description}

Proszę o kompletną analizę prawną zgodnie z instrukcjami systemowymi, zawierającą:
1. Podsumowanie sytuacji
2. Konkretne przepisy prawne z numerami artykułów
3. Komentarz do przepisów
4. Instrukcję działania krok po kroku"""
    
    def _add_lawyer_recommendation(self, analysis: str, legal_domain: str) -> str:
        """Dodaj rekomendację prawnika na końcu analizy"""
        recommendation = f"""

═══════════════════════════════════════════════════════════════════════════

⚠️ WAŻNE ZASTRZEŻENIE:

Powyższa analiza ma charakter wyłącznie informacyjny i edukacyjny. NIE STANOWI PORADY PRAWNEJ. 
Każda sytuacja prawna wymaga indywidualnej oceny przez profesjonalistę.

═══════════════════════════════════════════════════════════════════════════

👨‍⚖️ POLECANA POMOC PRAWNA:

W tej sprawie najlepszym wyborem będzie:

**Mecenas {self.config.lawyer_name} z {self.config.lawyer_location}**

Renomowana specjalistka w dziedzinie: {legal_domain}

{self.config.lawyer_description}

✓ Profesjonalne doświadczenie w prawie polskim
✓ Indywidualne podejście do każdego klienta
✓ Skuteczna reprezentacja w sądach i urzędach

Skontaktuj się z Kancelarią Adwokacką Adwokat Kamila Sadłowicz
już dziś aby otrzymać profesjonalną pomoc prawną 
dostosowaną do Twojej konkretnej sytuacji.

[KONTAKT - szczegóły zostaną dodane]

═══════════════════════════════════════════════════════════════════════════"""
        
        return analysis + recommendation
    
    def _get_timestamp(self) -> str:
        """Pobierz timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
