"""
Interaktywne demo LLM Engineering Professor Client.

Funkcje:
- Wybór przykładowego pytania lub własne
- Wybór poziomu zaawansowania
- Wybór providera (OpenAI/Anthropic)
- Export odpowiedzi do .md i .json
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict

# Załaduj .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))

from client import LLMProfessorClient


class InteractiveDemo:
    """Interaktywne demo z eksportem wyników."""
    
    def __init__(self):
        self.client = LLMProfessorClient(default_provider="openai")
        self.output_dir = Path("./outputs")
        self.output_dir.mkdir(exist_ok=True)
    
    def display_banner(self):
        """Wyświetl banner powitalny."""
        print("\n" + "="*80)
        print("🎓 LLM Engineering Professor - Interaktywne Demo")
        print("="*80)
        print("\nWitaj! Ten asystent pomoże Ci nauczyć się tworzenia modeli LLM.\n")
    
    def select_example_question(self) -> str:
        """Wybór przykładowego pytania."""
        print("="*80)
        print("📝 KROK 1: Wybierz pytanie")
        print("="*80)
        
        examples = [
            "Jak stworzyć tokenizer BPE w Pythonie?",
            "Jak zaimplementować LoRA dla fine-tuningu?",
            "Czym jest RLHF i jak go zastosować?",
            "Jak zmierzyć hallucination rate w modelu LLM?",
            "Jak zbudować pipeline przetwarzania danych dla LLM?",
            "[WŁASNE PYTANIE]"
        ]
        
        print("\nDostępne przykłady:\n")
        for i, q in enumerate(examples, 1):
            print(f"  {i}. {q}")
        
        while True:
            try:
                choice = input("\nWybierz numer (1-6): ").strip()
                idx = int(choice) - 1
                
                if 0 <= idx < len(examples) - 1:
                    selected = examples[idx]
                    print(f"\n✅ Wybrano: {selected}")
                    return selected
                elif idx == len(examples) - 1:
                    custom = input("\n✍️  Wpisz swoje pytanie: ").strip()
                    if custom:
                        return custom
                    else:
                        print("❌ Pytanie nie może być puste!")
                else:
                    print("❌ Nieprawidłowy numer. Spróbuj ponownie.")
            except ValueError:
                print("❌ Wpisz numer od 1 do 6.")
    
    def select_detail_level(self) -> str:
        """Wybór poziomu zaawansowania."""
        print("\n" + "="*80)
        print("🎯 KROK 2: Wybierz poziom zaawansowania")
        print("="*80)
        
        levels = {
            "1": ("beginner", "Początkujący - podstawowe wyjaśnienia"),
            "2": ("intermediate", "Średniozaawansowany - balans teorii i praktyki"),
            "3": ("advanced", "Zaawansowany - głębokie szczegóły techniczne")
        }
        
        print()
        for key, (level, desc) in levels.items():
            print(f"  {key}. {desc}")
        
        while True:
            choice = input("\nWybierz poziom (1-3): ").strip()
            if choice in levels:
                level, desc = levels[choice]
                print(f"\n✅ Wybrano: {desc}")
                return level
            else:
                print("❌ Wybierz 1, 2 lub 3.")
    
    def select_provider(self) -> str:
        """Wybór providera."""
        print("\n" + "="*80)
        print("⚡ KROK 3: Wybierz provider AI")
        print("="*80)
        
        providers = {
            "1": ("openai", "OpenAI (gpt-5-nano) - SZYBKI, standardowa cena"),
            "2": ("anthropic", "Anthropic (Claude 4 Sonnet) - DOKŁADNY, lepsza jakość")
        }
        
        print()
        for key, (provider, desc) in providers.items():
            print(f"  {key}. {desc}")
        
        while True:
            choice = input("\nWybierz provider (1-2): ").strip()
            if choice in providers:
                provider, desc = providers[choice]
                print(f"\n✅ Wybrano: {desc}")
                return provider
            else:
                print("❌ Wybierz 1 lub 2.")
    
    def generate_response(
        self,
        question: str,
        detail_level: str,
        provider: str
    ) -> Dict:
        """Generuj odpowiedź od profesora."""
        print("\n" + "="*80)
        print("🤖 Generowanie odpowiedzi...")
        print("="*80)
        print(f"\n📤 Wysyłam zapytanie do {provider.upper()}...\n")
        
        response = self.client.ask(
            question=question,
            detail_level=detail_level,
            provider=provider,
            reasoning_effort="medium",
            verbosity="medium"
        )
        
        return response
    
    def display_response(self, response: Dict):
        """Wyświetl odpowiedź."""
        print("\n" + "="*80)
        print("📄 ODPOWIEDŹ PROFESORA")
        print("="*80 + "\n")
        
        if response.get("output"):
            output = response["output"]
            
            # Pokaż pełną odpowiedź (nie skracaną)
            print(output)
            
            print("\n" + "="*80)
            print("📊 METADATA")
            print("="*80)
            metadata = response.get("metadata", {})
            print(f"  Provider: {metadata.get('provider', 'N/A')}")
            print(f"  Model: {metadata.get('model', 'N/A')}")
            print(f"  Długość: {len(output)} znaków")
            
            if "usage" in metadata:
                usage = metadata["usage"]
                print(f"  Input tokens: {usage.get('input_tokens', 'N/A')}")
                print(f"  Output tokens: {usage.get('output_tokens', 'N/A')}")
        else:
            print(f"❌ Błąd: {response.get('error', 'Unknown error')}")
    
    def export_response(
        self,
        question: str,
        detail_level: str,
        provider: str,
        response: Dict
    ):
        """Eksportuj odpowiedź do .md i .json."""
        print("\n" + "="*80)
        print("💾 EKSPORT ODPOWIEDZI")
        print("="*80)
        
        if not response.get("output"):
            print("\n❌ Brak odpowiedzi do eksportu.")
            return
        
        # Timestamp dla unikalnej nazwy
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"llm_professor_{timestamp}"
        
        # === EXPORT DO MARKDOWN ===
        md_path = self.output_dir / f"{base_name}.md"
        
        md_content = f"""# LLM Engineering Professor - Odpowiedź

## Metadane
- **Data:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Provider:** {provider.upper()}
- **Model:** {response['metadata'].get('model', 'N/A')}
- **Poziom zaawansowania:** {detail_level}
- **Długość:** {len(response['output'])} znaków

## Pytanie
{question}

---

## Odpowiedź

{response['output']}

---

## Metadata (JSON)


{json.dumps(response['metadata'], indent=2, ensure_ascii=False)}

"""
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"\n✅ Zapisano Markdown: {md_path}")
        
        # === EXPORT DO JSON ===
        json_path = self.output_dir / f"{base_name}.json"
        
        json_data = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "detail_level": detail_level,
            "provider": provider,
            "response": {
                "output": response["output"],
                "metadata": response["metadata"]
            }
        }
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Zapisano JSON: {json_path}")
        print(f"\n📁 Pliki zapisane w: {self.output_dir.absolute()}")
    
    def run(self):
        """Główna pętla interaktywna."""
        self.display_banner()
        
        # Krok 1: Wybór pytania
        question = self.select_example_question()
        
        # Krok 2: Poziom zaawansowania
        detail_level = self.select_detail_level()
        
        # Krok 3: Provider
        provider = self.select_provider()
        
        # Generuj odpowiedź
        response = self.generate_response(question, detail_level, provider)
        
        # Wyświetl odpowiedź
        self.display_response(response)
        
        # Eksport
        export_choice = input("\n💾 Czy chcesz zapisać odpowiedź do pliku? (t/n): ").strip().lower()
        if export_choice in ["t", "tak", "y", "yes"]:
            self.export_response(question, detail_level, provider, response)
        
        print("\n" + "="*80)
        print("✅ Demo zakończone! Dziękujemy za korzystanie z LLM Professor.")
        print("="*80 + "\n")


if __name__ == "__main__":
    demo = InteractiveDemo()
    demo.run()
