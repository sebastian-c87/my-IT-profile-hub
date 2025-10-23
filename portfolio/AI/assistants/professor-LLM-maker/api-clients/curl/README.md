# LLM Engineering Professor - cURL Examples

Przykłady użycia API przez **cURL** bez instalacji dodatkowych bibliotek.

## 📋 Wymagania

- **curl** - zainstalowany domyślnie na większości systemów
- **jq** - parser JSON do formatowania wyników

### Instalacja jq

**Linux:**
sudo apt install jq

**macOS:**
brew install jq

**Windows (Git Bash):**
choco install jq

## 🚀 Szybki start

### 1. Przygotuj klucze API

Utwórz plik `.env` w folderze `curl/`:

OPENAI_API_KEY=sk-proj-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-api-your-anthropic-key-here

### 2. Uruchom przykłady

**Interaktywne menu:**
bash examples.sh

**Konkretny przykład:**
bash examples.sh 1    # OpenAI - pojedyncze pytanie
bash examples.sh 2    # OpenAI - multi-turn
bash examples.sh 3    # Anthropic - pojedyncze pytanie
bash examples.sh 4    # Anthropic - batch processing
bash examples.sh 5    # Uruchom wszystkie

## 📚 Dostępne przykłady

### Przykład 1: OpenAI Responses API - Pojedyncze pytanie

Podstawowe zapytanie do GPT-5 Nano z web search.

**Użycie:**
bash examples.sh 1

**Co robi:**
- Ładuje system prompt z `../../system.md`
- Wysyła zapytanie: "Jak stworzyć tokenizer BPE w Pythonie?"
- Używa reasoning effort: medium, verbosity: medium
- Zapisuje pełną odpowiedź do `output_openai_TIMESTAMP.json`

### Przykład 2: OpenAI Responses API - Multi-turn

Kontynuacja konwersacji z użyciem `previous_response_id`.

**Użycie:**
bash examples.sh 2

**Co robi:**
- Pierwsze pytanie: "Co to jest tokenizacja w NLP?"
- Drugie pytanie: "Jakie są popularne algorytmy?" (z kontekstem pierwszej odpowiedzi)
- Pokazuje jak używać `previous_response_id` dla konwersacji

### Przykład 3: Anthropic Messages API - Pojedyncze pytanie

Zapytanie do Claude 4 Sonnet.

**Użycie:**
bash examples.sh 3

**Co robi:**
- Ładuje system prompt
- Wysyła zapytanie: "Czym jest RLHF i jak go zastosować?"
- Wyświetla użycie tokenów (input/output)
- Zapisuje odpowiedź do `output_anthropic_TIMESTAMP.json`

### Przykład 4: Anthropic Batch API - Przetwarzanie wsadowe

Batch processing - 50% taniej niż standardowe API!

**Użycie:**
bash examples.sh 4

**Co robi:**
- Tworzy batch z 3 pytaniami
- Monitoruje status przetwarzania (polling co 10s)
- Czeka na zakończenie (max 10 minut)
- Pobiera i wyświetla wyniki wszystkich pytań
- Zapisuje wyniki do `output_batch_TIMESTAMP.jsonl`

## 📁 Generowane pliki

Po uruchomieniu przykładów w folderze `curl/` pojawią się:

- `output_openai_20251010_014500.json` - odpowiedzi OpenAI
- `output_anthropic_20251010_014530.json` - odpowiedzi Anthropic
- `output_batch_20251010_014600.jsonl` - wyniki batch (format JSONL)

## 🔧 Ręczne wywołania API

### OpenAI Responses API

curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5-nano",
    "input": "Jak działa tokenizacja BPE?",
    "reasoning": {"effort": "medium"},
    "text": {"verbosity": "medium"},
    "max_output_tokens": 16000,
    "tools": [{"type": "web_search"}]
  }'

### Anthropic Messages API

curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 16000,
    "messages": [
      {
        "role": "user",
        "content": "Czym jest RLHF?"
      }
    ]
  }'

### Anthropic Batch API

**1. Utwórz batch:**

curl https://api.anthropic.com/v1/messages/batches \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "requests": [
      {
        "custom_id": "req-1",
        "params": {
          "model": "claude-sonnet-4-20250514",
          "max_tokens": 16000,
          "messages": [{"role": "user", "content": "Pytanie 1"}]
        }
      }
    ]
  }'

**2. Sprawdź status:**

curl https://api.anthropic.com/v1/messages/batches/{batch_id} \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"

**3. Pobierz wyniki:**

curl {results_url} \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"

## 💰 Koszty API

| Provider | Model | Tryb | Input (1M tokens) | Output (1M tokens) | Oszczędność |
|----------|-------|------|-------------------|-------------------|-------------|
| OpenAI | gpt-5-nano | Standard | $0.20 | $0.80 | - |
| Anthropic | Claude Sonnet 4 | Standard | $3.00 | $15.00 | - |
| Anthropic | Claude Sonnet 4 | **Batch** | **$1.50** | **$7.50** | **50%** |

### Kiedy użyć Batch API?

✅ Przetwarzanie dużych ilości danych
✅ Nie potrzebujesz natychmiastowych odpowiedzi
✅ Chcesz zaoszczędzić 50% kosztów
✅ Analizy, ewaluacje, bulk processing

❌ Nie używaj dla aplikacji czasu rzeczywistego
❌ Nie używaj gdy potrzebujesz odpowiedzi < 1 minuty

## 🐛 Troubleshooting

### Problem: `jq: command not found`

**Przyczyna:** `jq` nie jest zainstalowane

**Rozwiązanie:**

**Linux:**
sudo apt install jq

**macOS:**
brew install jq

**Windows:**
choco install jq

### Problem: `API key not set`

**Przyczyna:** Plik `.env` nie istnieje lub jest pusty

**Rozwiązanie:**

1. Sprawdź czy `.env` istnieje:
   ls -la .env

2. Sprawdź zawartość:
   cat .env

3. Upewnij się że zawiera:
   OPENAI_API_KEY=sk-proj-...
   ANTHROPIC_API_KEY=sk-ant-...

### Problem: `Permission denied`

**Przyczyna:** Brak uprawnień do wykonania skryptu

**Rozwiązanie:**
chmod +x examples.sh

### Problem: `system.md not found`

**Przyczyna:** Skrypt nie może znaleźć system prompt

**Rozwiązanie:**

Sprawdź czy plik istnieje:
ls -la ../../system.md

Jeśli nie istnieje, utwórz symlink:
ln -s ../../../../system.md ../../system.md

### Problem: Batch timeout

**Przyczyna:** Batch processing trwa > 10 minut

**Rozwiązanie:**

1. Zwiększ MAX_WAIT w skrypcie:
   MAX_WAIT=1800  # 30 minut

2. Lub sprawdź status ręcznie:
   curl https://api.anthropic.com/v1/messages/batches/{batch_id} \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01"

## 📖 Dokumentacja API

### OpenAI

- **Responses API:** https://platform.openai.com/docs/api-reference/responses
- **GPT-5 Guide:** https://platform.openai.com/docs/guides/gpt-5
- **Authentication:** https://platform.openai.com/docs/api-reference/authentication

### Anthropic

- **Messages API:** https://docs.anthropic.com/en/api/messages
- **Batch Processing:** https://docs.anthropic.com/en/api/batch-processing
- **Authentication:** https://docs.anthropic.com/en/api/getting-started

## 🔐 Bezpieczeństwo

### Ochrona kluczy API

**NIE COMMITUJE** pliku `.env` do repozytorium!

`.gitignore` zawiera:
*.env

### GitHub Actions

W GitHub Actions używaj **Secrets**:

1. Przejdź do: Settings → Secrets and variables → Actions
2. Dodaj:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`

3. W workflow używaj:

   env:
     OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
     ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

## 📊 Przykładowy output

### OpenAI Responses API

✅ Załadowano .env (2 zmiennych)
================================================================
PRZYKŁAD 1: OpenAI Responses API - Pojedyncze pytanie
================================================================

📤 Wysyłam zapytanie do OpenAI (gpt-5-nano)...
   Pytanie: Jak stworzyć tokenizer BPE w Pythonie?

✅ Odpowiedź otrzymana!

📄 Podgląd odpowiedzi (pierwsze 500 znaków):

## Executive Summary
Byte-Pair Encoding (BPE) to algorytm tokenizacji wykorzystywany...

📊 Metadata:
   Model: gpt-5-nano
   Response ID: resp_abc123...
   Długość: 15234 znaków

💾 Pełna odpowiedź zapisana do: output_openai_20251010_014500.json

### Anthropic Batch API

📦 Tworzenie batch z 3 pytaniami...

✅ Batch utworzony: msgbatch_abc123...

⏳ Oczekiwanie na przetworzenie (sprawdzam co 10s)...

   Status: in_progress | Processing: 3, Succeeded: 0
   Status: in_progress | Processing: 2, Succeeded: 1
   Status: in_progress | Processing: 1, Succeeded: 2
   Status: ended | Processing: 0, Succeeded: 3

✅ Batch zakończony!

📥 Pobieranie wyników...

📊 Wyniki batch:

✅ question-1:
Tokenizacja BPE (Byte-Pair Encoding) to algorytm...
...

💾 Pełne wyniki zapisane do: output_batch_20251010_014600.jsonl

## 🎯 Wskazówki

### Optymalizacja kosztów

1. **Używaj Batch API** dla bulk operations (50% taniej)
2. **Kontroluj długość odpowiedzi:** `max_output_tokens`
3. **Wybieraj odpowiedni model:**
   - `gpt-5-nano` - najtańszy, szybki
   - `claude-sonnet-4` - droższy, lepsza jakość

### Optymalizacja prędkości

**OpenAI:**
"reasoning": {"effort": "low"},
"text": {"verbosity": "low"}

**Anthropic:**
Użyj Batch API tylko gdy nie potrzebujesz natychmiastowej odpowiedzi

### Debugging

Dodaj `-v` do curl dla szczegółów:

curl -v https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  ...

## 📝 Licencja

License - **CC-BY-NC-ND-4.0**
Author - **Sebastian C.**

## 🤝 Contributing

Pull requesty mile widziane!

1. Fork repozytorium
2. Utwórz branch: `git checkout -b feature/nowa-funkcja`
3. Commit: `git commit -m 'Dodaj nową funkcję'`
4. Push: `git push origin feature/nowa-funkcja`
5. Otwórz Pull Request

## 📧 Kontakt

![Profile](https://img.shields.io/badge/👨‍🎓%20Computer%20Science%20Student-IT%20Enthusiast-blue?style=for-the-badge)
![Specialization](https://img.shields.io/badge/🛡️%20Specialist%20in-CyberSecurity%20|%20Python%20|%20AI-green?style=for-the-badge)

![Location](https://img.shields.io/badge/📍%20Location-Warszawa,%20Polska-red?style=for-the-badge)  
![Phone](https://img.shields.io/badge/📞_Whatsapp_&_Phone-%2B48%20539%20298%20079-orange?style=for-the-badge&logo=whatsapp)

[![GitHub](https://img.shields.io/badge/GitHub-sebastian--c87-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sebastian-c87)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sebastian%20Ciborowski-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/)  
[![Gmail](https://img.shields.io/badge/Gmail-Kontakt_bezpośredni-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ciborowski.s@gmail.com)  

**💬 Najszybsza odpowiedź:** GitHub Issues lub kontakt bezpośredni przez email
