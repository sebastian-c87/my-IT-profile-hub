# Cryptocurrency Market Analyst - cURL API Examples

Prosty bash script demonstrujący wywołania OpenAI Responses API (GPT-5) i Anthropic Messages API (Claude) dla analizy rynków kryptowalut.

## Wymagania

### Zainstalowane narzędzia:
- Git Bash (Windows) lub Terminal (Linux/macOS)
- curl - do wywołań HTTP API
- jq - do parsowania JSON

### Sprawdź czy masz zainstalowane:
curl --version
jq --version

### Instalacja brakujących narzędzi:
Windows (Git Bash): jq pobierz z https://stedolan.github.io/jq/download/
Linux: sudo apt-get install curl jq
macOS: brew install curl jq

## Konfiguracja

### 1. Utwórz plik .env w folderze curl:
OPENAI_API_KEY=sk-proj-twój_klucz_openai
ANTHROPIC_API_KEY=sk-ant-twój_klucz_anthropic

### 2. Nadaj uprawnienia:
chmod +x examples.sh

## Użycie

### Uruchomienie:
./examples.sh

### Dostępne opcje:
1. Test OpenAI API - Test połączenia z GPT-5
2. Test Anthropic API - Test połączenia z Claude
3. Batch Analysis - Analiza wielu kryptowalut
4. Custom OpenAI Analysis - Wybierz kryptowalutę i typ analizy
5. Custom Claude Analysis - Analiza z Claude
6. Compare Models - Porównanie OpenAI vs Claude
7. System Information - Informacje o konfiguracji

## Pliki wyjściowe

Script tworzy folder outputs/ z plikami:
- openai_response_TIMESTAMP.json
- OpenAI_Analysis_TIMESTAMP.md
- anthropic_response_TIMESTAMP.json
- Claude_Analysis_TIMESTAMP.md
- batch_info_TIMESTAMP.json

## Przykładowe wywołania API

### OpenAI Responses API:
curl -X POST "https://api.openai.com/v1/responses" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $OPENAI_API_KEY" \
-d '{"model": "gpt-5-nano", "input": "Przeprowadź analizę Bitcoin", "reasoning": {"effort": "medium"}, "text": {"verbosity": "medium"}, "max_output_tokens": 16000, "tools": [{"type": "web_search"}]}'

### Anthropic Messages API:
curl -X POST "https://api.anthropic.com/v1/messages" \
-H "Content-Type: application/json" \
-H "x-api-key: $ANTHROPIC_API_KEY" \
-H "anthropic-version: 2023-06-01" \
-d '{"model": "claude-3-5-haiku-20241022", "max_tokens": 16000, "messages": [{"role": "user", "content": "Analizuj Ethereum"}]}'

## Rozwiązywanie problemów

### Częste błędy:

Permission denied: chmod +x examples.sh
command not found jq: Zainstaluj jq z https://stedolan.github.io/jq/download/
API key not found: Sprawdź plik .env (cat .env)
Shebang error Windows: dos2unix examples.sh
Pusty output: cat outputs/openai_response_*.json | jq .

### Debug mode:
bash -x examples.sh

## Interpretacja wyników

### Sukces:
✅ OpenAI API call successful
✅ Full response saved to: ./outputs/openai_response_TIMESTAMP.json
ℹ️ Response ID: resp_07ddb9c9924a025d0068e01d8d6c9481
ℹ️ Model used: gpt-5-nano-2025-08-07
ℹ️ Output length: 2847 characters

### Problem z API:
❌ Failed to make API call to OpenAI
❌ OpenAI API Error: Invalid API key

### Analiza plików JSON:
jq '.error' outputs/openai_response_*.json
jq '.output_text' outputs/openai_response_*.json

## Struktura plików

curl/
├── examples.sh - Główny script
├── .env - Klucze API (utwórz ręcznie)
├── README.md - Ta dokumentacja
└── outputs/ - Folder z wynikami (auto-tworzony)

## Szybki start

1. Przejdź do folderu curl
2. Utwórz plik .env z kluczami API
3. Nadaj uprawnienia: chmod +x examples.sh
4. Uruchom: ./examples.sh
5. Wybierz opcję 1 lub 2 do testów

## Wsparcie

- Błędy API: Sprawdź klucze API w .env
- Błędy bash: Użyj bash -x examples.sh
- Błędy JSON: Użyj jq do sprawdzenia odpowiedzi
- Problemy z curl: Dodaj -v do curl

Script testowany na Git Bash (Windows), Linux Bash, i macOS Terminal
