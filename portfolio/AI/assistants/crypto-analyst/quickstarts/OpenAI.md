# OpenAI GPT-5 Integration

> Konfiguracja i optymalizacja OpenAI Responses API wymaga własnego klucza API od OpenAI. Do wygenerowania na [platform.openai.com](platform.openai.com)

**Instalacja:** export OPENAI_API_KEY="sk-proj-your-key-here"

**Opis Asystenta:** Wykorzystuje najnowszą architekturę GPT-5 z web search capabilities do analizy kryptowalut w czasie rzeczywistym. Model zoptymalizowany pod kątem finansowych analiz z enhanced reasoning i access do aktualnych danych rynkowych, newsów i on-chain metrics.

**Przykład użycia:**
```python
import openai

client = openai.OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="Przeprowadź analizę rynkową dla Cardano (ADA) z uwzględnieniem nadchodzących aktualizacji protokołu i wpływu na cenę.",
    reasoning={"effort": "medium"},
    text={"verbosity": "medium"},
    tools=[{"type": "web_search"}],
    max_output_tokens=16000,
    store=True
)

print(response.output_text)

```

**Funkcje:** GPT-5 Nano (szybkie analizy), GPT-5 Mini (głębokie analizy), Web search (aktualne dane), Reasoning modes (minimal/medium/high). Oczekiwane efekty: precyzyjne analizy z real-time data, comprehensive market insights, structured recommendations z confidence levels i detailed risk warnings.
