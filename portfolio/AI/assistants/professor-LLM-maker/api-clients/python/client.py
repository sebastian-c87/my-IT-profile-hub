"""
Klient API dla LLM Engineering Professor Assistant.

Obsługuje:
- OpenAI Responses API (gpt-5-nano) - domyślny, szybki
- Anthropic Batch API (Claude 4 Sonnet) - optymalizacja kosztów (50% taniej)
"""

import os
import time
import json
from typing import Dict, List, Optional, Union, Literal
from pathlib import Path

# Załaduj .env z głównego folderu repo
from dotenv import load_dotenv, find_dotenv

# OpenAI SDK (Responses API)
from openai import OpenAI

# Anthropic SDK (Batch API)
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request


# Automatyczne wczytanie .env z głównego folderu repo
# find_dotenv() szuka .env w folderach nadrzędnych
load_dotenv(find_dotenv(usecwd=True))


class LLMProfessorClient:
    """
    Klient dla LLM Engineering Professor Assistant.
    
    Przykład użycia:
        >>> client = LLMProfessorClient()
        >>> response = client.ask("Jak stworzyć tokenizer BPE?")
        >>> print(response["output"])
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        system_prompt_path: Optional[str] = None,
        default_provider: Literal["openai", "anthropic"] = "openai"
    ):
        """
        Inicjalizacja klienta.
        
        Args:
            openai_api_key: Klucz API OpenAI (domyślnie z env OPENAI_API_KEY)
            anthropic_api_key: Klucz API Anthropic (domyślnie z env ANTHROPIC_API_KEY)
            system_prompt_path: Ścieżka do pliku system.md
            default_provider: Domyślny provider ("openai" lub "anthropic")
        """
        # Pobierz klucze API (najpierw z argumentów, potem z env)
        _openai_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        _anthropic_key = anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
        
        # Walidacja kluczy
        if not _openai_key:
            print("⚠️  OPENAI_API_KEY nie jest ustawiony!")
            print("   Ustaw w .env lub przekaż do konstruktora.")
        
        if not _anthropic_key:
            print("⚠️  ANTHROPIC_API_KEY nie jest ustawiony!")
            print("   Potrzebny dla batch processing i Claude.")
        
        # OpenAI Client
        self.openai_client = OpenAI(api_key=_openai_key) if _openai_key else None
        
        # Anthropic Client
        self.anthropic_client = anthropic.Anthropic(api_key=_anthropic_key) if _anthropic_key else None
        
        # Załaduj system prompt
        self.system_prompt = self._load_system_prompt(system_prompt_path)
        
        self.default_provider = default_provider
    
    def _load_system_prompt(self, path: Optional[str] = None) -> str:
        """Załaduj system prompt z pliku system.md."""
        if path is None:
            # Domyślna ścieżka: ../../system.md (względem client.py)
            current_dir = Path(__file__).parent
            path = current_dir.parent.parent / "system.md"
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"✅ Załadowano system prompt z: {path}")
                return content
        except FileNotFoundError:
            print(f"⚠️  Warning: system.md nie znaleziony w {path}")
            print(f"   Używam fallback promptu.")
            return "Jesteś ekspertem w inżynierii modeli językowych (LLM)."
    
    def ask(
        self,
        question: str,
        detail_level: Literal["beginner", "intermediate", "advanced"] = "intermediate",
        provider: Optional[Literal["openai", "anthropic"]] = None,
        **kwargs
    ) -> Dict:
        """
        Zadaj pytanie profesorowi LLM.
        
        Args:
            question: Pytanie użytkownika
            detail_level: Poziom szczegółowości odpowiedzi
            provider: Provider do użycia (None = użyj default_provider)
            **kwargs: Dodatkowe parametry (reasoning_effort, verbosity, etc.)
        
        Returns:
            Dict z kluczami:
                - output: Główna odpowiedź tekstowa
                - metadata: Metadane (model, tokens, provider)
                - raw_response: Surowa odpowiedź z API
        """
        provider = provider or self.default_provider
        
        if provider == "openai":
            if not self.openai_client:
                raise ValueError("OpenAI client nie jest zainicjalizowany (brak API key)")
            return self._ask_openai(question, detail_level, **kwargs)
        elif provider == "anthropic":
            if not self.anthropic_client:
                raise ValueError("Anthropic client nie jest zainicjalizowany (brak API key)")
            return self._ask_anthropic_sync(question, detail_level, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _ask_openai(
        self,
        question: str,
        detail_level: str,
        reasoning_effort: str = "medium",
        verbosity: str = "medium",
        **kwargs
    ) -> Dict:
        """
        Zapytanie przez OpenAI Responses API (gpt-5-nano).
        
        Dokumentacja: https://platform.openai.com/docs/api-reference/responses
        """
        try:
            response = self.openai_client.responses.create(
                model="gpt-5-nano",
                instructions=self.system_prompt,
                input=f"""
## Pytanie o LLM Engineering
{question}

## Poziom skomplikowania
{detail_level}
                """.strip(),
                tools=[{"type": "web_search"}],  # Native web search
                tool_choice="auto",
                reasoning={"effort": reasoning_effort},
                text={"verbosity": verbosity},
                max_output_tokens=kwargs.get("max_tokens", 16000),
                store=kwargs.get("store", True),  # Cache dla multi-turn
                **kwargs
            )
            
            return {
                "output": response.output_text,
                "metadata": {
                    "provider": "openai",
                    "model": "gpt-5-nano",
                    "response_id": response.id,
                    "created_at": response.created_at,
                    "reasoning_effort": reasoning_effort,
                    "verbosity": verbosity
                },
                "raw_response": response
            }
        
        except Exception as e:
            return {
                "output": None,
                "error": str(e),
                "metadata": {"provider": "openai", "model": "gpt-5-nano"}
            }
    
    def _ask_anthropic_sync(
        self,
        question: str,
        detail_level: str,
        **kwargs
    ) -> Dict:
        """
        Zapytanie przez Anthropic Messages API (synchroniczne).
        
        Uwaga: Dla optymalizacji kosztów użyj ask_batch() zamiast tej metody.
        """
        try:
            message = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=kwargs.get("max_tokens", 16000),
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
## Pytanie o LLM Engineering
{question}

## Poziom skomplikowania
{detail_level}
                        """.strip()
                    }
                ]
            )
            
            return {
                "output": message.content[0].text,
                "metadata": {
                    "provider": "anthropic",
                    "model": "claude-sonnet-4-20250514",
                    "message_id": message.id,
                    "usage": {
                        "input_tokens": message.usage.input_tokens,
                        "output_tokens": message.usage.output_tokens
                    }
                },
                "raw_response": message
            }
        
        except Exception as e:
            return {
                "output": None,
                "error": str(e),
                "metadata": {"provider": "anthropic", "model": "claude-sonnet-4-20250514"}
            }
    
    def ask_batch(
        self,
        questions: List[Dict[str, str]],
        polling_interval: int = 30,
        timeout: int = 3600
    ) -> List[Dict]:
        """
        Batch processing przez Anthropic Batch API (50% taniej!).
        
        Args:
            questions: Lista dict z kluczami 'question' i 'detail_level'
                Przykład: [{"question": "...", "detail_level": "intermediate"}]
            polling_interval: Interwał sprawdzania statusu (sekundy)
            timeout: Maksymalny czas oczekiwania (sekundy)
        
        Returns:
            Lista odpowiedzi w tej samej kolejności co questions
        
        Przykład:
            >>> questions = [
            ...     {"question": "Jak działa tokenizacja BPE?", "detail_level": "intermediate"},
            ...     {"question": "Czym jest RLHF?", "detail_level": "advanced"}
            ... ]
            >>> results = client.ask_batch(questions)
        """
        if not self.anthropic_client:
            raise ValueError("Anthropic client nie jest zainicjalizowany (brak API key)")
        
        print(f"📦 Tworzenie batch z {len(questions)} pytaniami...")
        
        # Przygotuj requesty
        requests = []
        for idx, q in enumerate(questions):
            question = q.get("question", "")
            detail_level = q.get("detail_level", "intermediate")
            
            requests.append(
                Request(
                    custom_id=f"question-{idx}",
                    params=MessageCreateParamsNonStreaming(
                        model="claude-sonnet-4-20250514",
                        max_tokens=16000,
                        system=self.system_prompt,
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
## Pytanie o LLM Engineering
{question}

## Poziom skomplikowania
{detail_level}
                                """.strip()
                            }
                        ]
                    )
                )
            )
        
        # Utwórz batch
        try:
            message_batch = self.anthropic_client.messages.batches.create(
                requests=requests
            )
            
            batch_id = message_batch.id
            print(f"✅ Batch utworzony: {batch_id}")
            print(f"⏳ Oczekiwanie na przetworzenie (max {timeout}s)...")
            
            # Polling statusu
            start_time = time.time()
            while time.time() - start_time < timeout:
                batch_status = self.anthropic_client.messages.batches.retrieve(batch_id)
                
                status = batch_status.processing_status
                counts = batch_status.request_counts
                
                print(f"   Status: {status} | Processing: {counts.processing}, "
                      f"Succeeded: {counts.succeeded}, Errored: {counts.errored}")
                
                if status == "ended":
                    print(f"✅ Batch zakończony!")
                    break
                
                time.sleep(polling_interval)
            else:
                raise TimeoutError(f"Batch nie zakończył się w ciągu {timeout}s")
            
            # Pobierz wyniki
            print(f"📥 Pobieranie wyników...")
            results_map = {}
            
            for result in self.anthropic_client.messages.batches.results(batch_id):
                custom_id = result.custom_id
                
                if result.result.type == "succeeded":
                    message = result.result.message
                    results_map[custom_id] = {
                        "output": message.content[0].text,
                        "metadata": {
                            "provider": "anthropic_batch",
                            "model": "claude-sonnet-4-20250514",
                            "custom_id": custom_id,
                            "usage": {
                                "input_tokens": message.usage.input_tokens,
                                "output_tokens": message.usage.output_tokens
                            }
                        },
                        "raw_response": message
                    }
                elif result.result.type == "errored":
                    results_map[custom_id] = {
                        "output": None,
                        "error": result.result.error.message,
                        "metadata": {"custom_id": custom_id}
                    }
                else:
                    results_map[custom_id] = {
                        "output": None,
                        "error": f"Result type: {result.result.type}",
                        "metadata": {"custom_id": custom_id}
                    }
            
            # Zwróć wyniki w kolejności pytań
            sorted_results = [
                results_map.get(f"question-{i}", {"output": None, "error": "Missing result"})
                for i in range(len(questions))
            ]
            
            print(f"✅ Pobrano {len(sorted_results)} wyników")
            return sorted_results
        
        except Exception as e:
            print(f"❌ Błąd batch processing: {e}")
            return [{"output": None, "error": str(e)} for _ in questions]
    
    def multi_turn_conversation(
        self,
        messages: List[str],
        provider: Literal["openai", "anthropic"] = "openai"
    ) -> List[Dict]:
        """
        Wieloetapowa konwersacja z profesorem.
        
        Args:
            messages: Lista pytań użytkownika
            provider: Provider do użycia
        
        Returns:
            Lista odpowiedzi dla każdego pytania
        """
        if provider == "openai":
            if not self.openai_client:
                raise ValueError("OpenAI client nie jest zainicjalizowany")
            return self._multi_turn_openai(messages)
        elif provider == "anthropic":
            if not self.anthropic_client:
                raise ValueError("Anthropic client nie jest zainicjalizowany")
            return self._multi_turn_anthropic(messages)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _multi_turn_openai(self, messages: List[str]) -> List[Dict]:
        """Multi-turn przez OpenAI z previous_response_id."""
        responses = []
        previous_response_id = None
        
        for msg in messages:
            response = self.openai_client.responses.create(
                model="gpt-5-nano",
                instructions=self.system_prompt if previous_response_id is None else None,
                input=msg,
                previous_response_id=previous_response_id,
                tools=[{"type": "web_search"}],
                reasoning={"effort": "medium"},
                store=True
            )
            
            responses.append({
                "output": response.output_text,
                "metadata": {"response_id": response.id}
            })
            
            previous_response_id = response.id
        
        return responses
    
    def _multi_turn_anthropic(self, messages: List[str]) -> List[Dict]:
        """Multi-turn przez Anthropic (ręczne zarządzanie kontekstem)."""
        responses = []
        conversation_history = []
        
        for msg in messages:
            conversation_history.append({"role": "user", "content": msg})
            
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                system=self.system_prompt,
                messages=conversation_history
            )
            
            assistant_msg = response.content[0].text
            conversation_history.append({"role": "assistant", "content": assistant_msg})
            
            responses.append({
                "output": assistant_msg,
                "metadata": {"message_id": response.id}
            })
        
        return responses

if __name__ == "__main__":
    """
    Quick test gdy uruchamiasz client.py bezpośrednio.
    
    Użycie:
        python client.py
    """
    print("="*80)
    print("🧪 LLM Engineering Professor Client - Quick Test")
    print("="*80)
    
    # Test inicjalizacji
    print("\n1️⃣  Testowanie inicjalizacji klienta...")
    client = LLMProfessorClient()
    
    # Sprawdź API keys
    print("\n2️⃣  Sprawdzanie klientów API:")
    print(f"   OpenAI client: {'✅ OK' if client.openai_client else '❌ Brak'}")
    print(f"   Anthropic client: {'✅ OK' if client.anthropic_client else '❌ Brak'}")
    
    # Sprawdź system prompt
    print("\n3️⃣  System prompt:")
    print(f"   Długość: {len(client.system_prompt)} znaków")
    print(f"   Podgląd: {client.system_prompt[:200]}...")
    
    # Proste pytanie testowe
    if client.openai_client:
        print("\n4️⃣  Test szybkiego zapytania (OpenAI)...")
        test_response = client.ask(
            question="Czym jest tokenizacja w NLP? (krótko)",
            detail_level="beginner"
        )
        
        if test_response.get("output"):
            output = test_response["output"]
            print(f"\n✅ Odpowiedź otrzymana ({len(output)} znaków)")
            print(f"\n📄 Podgląd odpowiedzi:\n")
            print(output[:500] + "..." if len(output) > 500 else output)
        else:
            print(f"\n❌ Błąd: {test_response.get('error')}")
    else:
        print("\n⚠️  Brak OpenAI API key - pomijam test zapytania")
    
    print("\n" + "="*80)
    print("✅ Quick test zakończony!")
    print("\n💡 Dla pełnego demo uruchom: python demo.py")
    print("="*80 + "\n")
