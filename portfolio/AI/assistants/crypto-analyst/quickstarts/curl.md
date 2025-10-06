# cURL Examples

> Bezpośrednie wywołania API przez Bash scripting.

**Instalacja:** cd api-clients/curl && chmod +x examples.sh

**Opis Asystenta:** Profesjonalny asystent AI do analizy kryptowalut oferujący multi-provider support (OpenAI GPT-5, Anthropic Claude). Dostarcza actionable insights dla decision making w tradingu, portfolio management i risk assessment z wykorzystaniem aktualnych danych rynkowych.

**Przykład użycia:**
```bash
#!/bin/bash
source .env

curl -X POST "https://api.openai.com/v1/responses" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5-nano",
    "input": "'$(cat system.md)'\n\nAnaliza Solana (SOL) - identyfikacja optymalnych punktów wejścia na podstawie wskaźników technicznych i momentum rynkowego.",
    "reasoning": {"effort": "medium"},
    "text": {"verbosity": "medium"},
    "tools": [{"type": "web_search"}],
    "max_output_tokens": 16000
  }' | jq -r '.output_text' > analysis_output.md
```
**Funkcje:** Batch analysis (analiza wielu crypto), Custom queries (spersonalizowane zapytania), Model comparison (OpenAI vs Claude), Output formatting (JSON, Markdown). Oczekiwane efekty: szczegółowe pliki analityczne zapisywane lokalnie z timestamps, strukturyzowane dane JSON oraz czytelne raporty Markdown.
