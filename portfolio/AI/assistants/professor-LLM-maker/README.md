<div align="center">

# 🎓 LLM Engineering Professor

### *Twój mentor w świecie budowy Large Language Models*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=for-the-badge&logo=node.js&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--5-412991?style=for-the-badge&logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude--4-191919?style=for-the-badge&logo=anthropic&logoColor=white)

![License](https://img.shields.io/badge/License-CC--BY--NC--ND--4.0-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange?style=flat-square)

---

**Kompleksowy asystent AI do nauki projektowania, trenowania i wdrażania dużych modeli językowych**

 [📚 Opis projektu](#-o-projekcie) • [🚀 Quickstart](#-quickstart) • [🎯 API Clients](#-api-clients) • [💡 Przykłady](#-przykłady-użycia) • [🤝 Author](#-kontakt)

</div>

---

## 📖 Spis treści

- [O Projekcie](#-o-projekcie)
- [Funkcje](#-funkcje)
- [Struktura projektu](#-struktura-projektu)
- [Quickstart](#-quickstart)
- [API Clients](#-api-clients)
- [Przykłady użycia](#-przykłady-użycia)
- [Koszty API](#-koszty-api)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Licencja](#-licencja)
- [Kontakt](#-kontakt)

---

## 🎯 O projekcie

**LLM Engineering Professor** to zaawansowany asystent AI stworzony dla osób uczących się projektowania i budowy Large Language Models. Projekt łączy:

✨ **Edukację** - szczegółowe wyjaśnienia konceptów i best practices  
🔧 **Praktykę** - gotowy kod Python, Node.js i cURL  
🚀 **Produkcję** - integracje z OpenAI GPT-5 i Anthropic Claude 4  
📊 **Ewaluację** - benchmarki, metryki, monitoring  

### Czego nauczysz się z tym projektem?

| Kategoria | Tematy |
|-----------|--------|
| 🏗️ **Architektura** | Decoder-only vs encoder-decoder, rozmiar modeli, tokenizacja (BPE, Unigram) |
| 📊 **Dane** | Pozyskiwanie, czyszczenie, deduplikacja, etykietowanie, Data Cards |
| 🎓 **Trening** | AdamW, mixed precision (FP16/BF16), paralelizacja (DP/TP/PP/FSDP) |
| 🔄 **Alignment** | RLHF, RLAIF, DPO, Constitutional AI |
| 📈 **Ewaluacja** | Perplexity, BLEU, hallucination rate, safety benchmarks |
| 🛡️ **Bezpieczeństwo** | PII filtering, jailbreak prevention, red-teaming, governance |
| 🚀 **MLOps** | vLLM, TensorRT-LLM, quantization (8-bit/4-bit), LoRA/QLoRA |

---

## 🎁 Funkcje

### 🤖 Wsparcie wielu modeli AI

- **OpenAI GPT-5** (nano/mini/full) - najnowszy model z reasoning capabilities
- **Anthropic Claude 4 Sonnet** - doskonała jakość i context window 200k tokens
- **Batch processing** - 50% tańsze przetwarzanie wsadowe (Anthropic)

### 🔧 Multi-language support

| Język | Status | Klient |
|-------|--------|--------|
| 🐍 **Python** | ✅ Gotowy | `api-clients/python/` |
| 🟢 **Node.js** | ✅ Gotowy | `api-clients/nodejs/` |
| 📡 **cURL** | ✅ Gotowy | `api-clients/curl/` |

### 🎨 Interaktywne demo

- **Python**: Kolorowe CLI z exportem do Markdown/JSON
- **Node.js**: Eleganckie menu z wyborem providera i poziomu zaawansowania
- **cURL**: Skrypty Bash z automatycznym polling (batch API)

### 📦 Generowane outputy

Wszystkie klienty automatycznie eksportują odpowiedzi do:

- **Markdown** (.md) - czytelny format z metadanymi
- **JSON** (.json) - surowe dane z API do dalszej analizy
- **TXT** (.txt) - prosty tekst bez formatowania

---

## 📁 Struktura projektu

    professor-LLM-maker/
    ├── 📄 system.md                    # System prompt (Role, Skills, Reasoning)
    ├── 📄 README.md                    # Ten plik
    ├── 📄 assistant.yaml               # Ustawienia asystenta + wymagania output
    ├── 📄 tools.json                   # Tools
    ├── 🔒 .env                         # Klucze API (poza repozytorium)
    ├── evaluations/promptfoo.yml       # Test zgodności promptu przez Github Actions
    └── api-clients/
        ├── 🐍 python/
        │   ├── client.py               # Klient Python (OOP)
        │   ├── demo.py                 # Interaktywne demo
        │   ├── requirements.txt        # Zależności
        │   └── outputs/                # Auto-generowane pliki
        ├── 🟢 nodejs/
        │   ├── client.js               # Klient Node.js (ES6 modules)
        │   ├── demo.js                 # Interaktywne demo
        │   ├── package.json            # Konfiguracja npm
        │   ├── node_modules/           # Symlink do globalnego
        │   └── outputs/                # Auto-generowane pliki
        └── 📡 curl/
            ├── examples.sh             # Skrypty Bash z przykładami
            ├── .env                    # Lokalna kopia kluczy API
            └── outputs/                # Auto-generowane pliki

---

## 🚀 Quickstart

### Krok 1: Klonuj repozytorium

    git clone https://github.com/twoj-username/professor-LLM-maker.git
    cd professor-LLM-maker

### Krok 2: Konfiguracja kluczy API

Utwórz plik `.env` w głównym folderze:

    OPENAI_API_KEY=sk-proj-your-key-here
    ANTHROPIC_API_KEY=sk-ant-api-your-key-here

**⚠️ Uwaga:** `.env` dodane do `.gitignore` żeby go publicznie nie udostępnić!  
**⚠️ Github:** klucze API dodane przez `secrets` w ustawieniach repozytorium.

### Krok 3: Wybierz klienta

#### 🐍 Python

    cd api-clients/python
    pip install -r requirements.txt
    
    python demo.py

#### 🟢 Node.js

    cd api-clients/nodejs
    npm install
    
    node demo.js

#### 📡 cURL

    cd api-clients/curl
    bash examples.sh

---

## 🔌 API Clients

### 🐍 Python Client

**Funkcje:**
- ✅ OpenAI Responses API (GPT-5)
- ✅ Anthropic Messages API (Claude 4)
- ✅ Export do Markdown/JSON

**Przykład użycia (zgodnie z Responses API):**

    from openai import OpenAI
    
    client = OpenAI()
    
    # Załaduj system prompt z system.md
    with open('system.md', 'r', encoding='utf-8') as f:
        instructions = f.read()
    
    # Wywołanie Responses API
    response = client.responses.create(
        model="gpt-5-nano",
        instructions=instructions,        # ← system.md jako instructions
        input="Jak działa tokenizacja BPE?",
        tools=[{"type": "web_search"}],   # ← Native web search
        reasoning={"effort": "medium"},   # ← minimal/low/medium/high
        text={"verbosity": "medium"},     # ← low/medium/high
        max_output_tokens=16000,
        store=True                        # ← Cache dla multi-turn
    )
    
    print(response.output_text)

**Kluczowe parametry:**
- `instructions` - pełny system prompt (system.md)
- `input` - pytanie użytkownika
- `reasoning.effort` - `minimal`/`low`/`medium`/`high` (kontrola myślenia)
- `text.verbosity` - `low`/`medium`/`high` (długość odpowiedzi)
- `tools` - native tools: web_search, file_search, code_interpreter
- `store=True` - automatyczny cache między requestami

📖 **[Przykłady Python →](api-clients/python/)**

---

### 🟢 Node.js Client

**Funkcje:**
- ✅ OpenAI Responses API
- ✅ Anthropic Messages API
- ✅ Multi-turn conversations

**Przykład użycia (zgodnie z Responses API):**

    import OpenAI from 'openai';
    import fs from 'fs/promises';
    
    const client = new OpenAI();
    
    // Załaduj system.md
    const instructions = await fs.readFile('system.md', 'utf-8');
    
    // Wywołanie Responses API
    const response = await client.responses.create({
        model: 'gpt-5-nano',
        instructions: instructions,        // ← system.md
        input: 'Jak działa tokenizacja BPE?',
        tools: [{ type: 'web_search' }],   // ← Native tools
        reasoning: { effort: 'medium' },
        text: { verbosity: 'medium' },
        max_output_tokens: 16000,
        store: true
    });
    
    console.log(response.output_text);

**Multi-turn (z kontekstem poprzedniej odpowiedzi):**

    // Pierwsze pytanie
    const response1 = await client.responses.create({
        model: 'gpt-5-nano',
        input: 'Co to jest tokenizacja?',
        store: true
    });
    
    // Drugie pytanie - model pamięta poprzednią odpowiedź
    const response2 = await client.responses.create({
        model: 'gpt-5-nano',
        input: 'Jakie są popularne algorytmy?',
        previous_response_id: response1.id,  // ← Kontekst!
        store: true
    });

📖 **[Przykłady Node.js →](api-clients/nodejs/)**

---

### 📡 cURL Examples

**Funkcje:**
- ✅ Zero dependencies (curl + jq)
- ✅ OpenAI Responses API
- ✅ Anthropic Batch API

**Przykład użycia (zgodnie z Responses API):**

    # Załaduj klucze API
    source .env
    
    # Załaduj system.md
    INSTRUCTIONS=$(cat ../../system.md)
    
    # Wywołanie Responses API
    curl https://api.openai.com/v1/responses \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d "{
        \"model\": \"gpt-5-nano\",
        \"instructions\": \"$INSTRUCTIONS\",
        \"input\": \"Jak działa tokenizacja BPE?\",
        \"tools\": [{\"type\": \"web_search\"}],
        \"reasoning\": {\"effort\": \"medium\"},
        \"text\": {\"verbosity\": \"medium\"},
        \"max_output_tokens\": 16000,
        \"store\": true
      }"

**Lub użyj gotowego skryptu:**

    cd api-clients/curl
    bash examples.sh 1    # OpenAI single query

📖 **[Pełna dokumentacja cURL →](api-clients/curl/README.md)**

---

## 💡 Przykłady użycia

### Przykład 1: Podstawowe zapytanie

**Python (czysty Responses API):**

    from openai import OpenAI
    
    client = OpenAI()
    
    response = client.responses.create(
        model="gpt-5-nano",
        instructions=open('system.md').read(),
        input="Czym jest RLHF?",
        reasoning={"effort": "low"},      # Szybsza odpowiedź
        text={"verbosity": "low"}         # Zwięźle
    )
    
    print(response.output_text)

**Node.js (czysty Responses API):**

    import OpenAI from 'openai';
    
    const client = new OpenAI();
    
    const response = await client.responses.create({
        model: 'gpt-5-nano',
        instructions: await fs.readFile('system.md', 'utf-8'),
        input: 'Czym jest RLHF?',
        reasoning: { effort: 'low' },
        text: { verbosity: 'low' }
    });
    
    console.log(response.output_text);

**cURL:**

    curl https://api.openai.com/v1/responses \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d '{
        "model": "gpt-5-nano",
        "instructions": "...zawartość system.md...",
        "input": "Czym jest RLHF?",
        "reasoning": {"effort": "low"},
        "text": {"verbosity": "low"}
      }'

---

### Przykład 2: Kontrola reasoning effort

**Różne poziomy myślenia:**

    # MINIMAL - najszybsze (~2s)
    response = client.responses.create(
        model="gpt-5-nano",
        input="Jak działa BPE?",
        reasoning={"effort": "minimal"}
    )
    
    # LOW - szybkie (~3s)
    response = client.responses.create(
        model="gpt-5-nano",
        input="Jak działa BPE?",
        reasoning={"effort": "low"}
    )
    
    # MEDIUM - standardowe (~5s)
    response = client.responses.create(
        model="gpt-5-nano",
        input="Jak działa BPE?",
        reasoning={"effort": "medium"}
    )
    
    # HIGH - głębokie myślenie (~10s)
    response = client.responses.create(
        model="gpt-5-nano",
        input="Jak działa BPE?",
        reasoning={"effort": "high"}
    )

| Effort | Czas | Użyj gdy |
|--------|------|----------|
| `minimal` | ~2s | Proste pytania, prototypowanie |
| `low` | ~3s | Standardowe pytania |
| `medium` | ~5s | **Default** - balans jakość/prędkość |
| `high` | ~10s | Złożone problemy, najwyższa jakość |

---

### Przykład 3: Multi-turn conversation

**Python:**

    # Pierwsza odpowiedź
    r1 = client.responses.create(
        model="gpt-5-nano",
        input="Co to jest tokenizacja?",
        store=True  # ← Włącz cache
    )
    
    # Druga odpowiedź - z kontekstem
    r2 = client.responses.create(
        model="gpt-5-nano",
        input="Jakie są algorytmy?",
        previous_response_id=r1.id,  # ← Model pamięta!
        store=True
    )

**Node.js:**

    const r1 = await client.responses.create({
        model: 'gpt-5-nano',
        input: 'Co to jest tokenizacja?',
        store: true
    });
    
    const r2 = await client.responses.create({
        model: 'gpt-5-nano',
        input: 'Jakie są algorytmy?',
        previous_response_id: r1.id,
        store: true
    });

**Jak działa `store=True`:**
- Model zapisuje reasoning tokens
- Kolejne requesty mają pełny kontekst
- Wyższa jakość odpowiedzi
- **Brak dodatkowych kosztów** za cache

---

### Przykład 4: Native tools (web_search)

**Python:**

    response = client.responses.create(
        model="gpt-5-nano",
        input="Jakie są najnowsze benchmarki dla GPT-5?",
        tools=[{"type": "web_search"}]  # ← Model przeszuka internet
    )

**Dostępne native tools:**
- `web_search` - wyszukiwanie w internecie
- `file_search` - przeszukiwanie uploadowanych plików
- `code_interpreter` - wykonywanie kodu Python
- `computer_use` - interakcja z GUI (eksperymentalne)

---

### Przykład 5: Batch processing (Anthropic - 50% taniej)

**Python:**

    import anthropic
    
    client = anthropic.Anthropic()
    
    # Utwórz batch
    batch = client.messages.batches.create(
        requests=[
            {
                "custom_id": "q1",
                "params": {
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 16000,
                    "system": open('system.md').read(),
                    "messages": [{"role": "user", "content": "Jak działa BPE?"}]
                }
            },
            {
                "custom_id": "q2",
                "params": {
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 16000,
                    "system": open('system.md').read(),
                    "messages": [{"role": "user", "content": "Czym jest RLHF?"}]
                }
            }
        ]
    )
    
    # Monitoruj status
    while batch.processing_status != "ended":
        batch = client.messages.batches.retrieve(batch.id)
        time.sleep(10)
    
    # Pobierz wyniki
    results = client.messages.batches.results(batch.id)

**Oszczędności:** 50% kosztów przy tej samej jakości!

---

## 💰 Koszty API

| Provider | Model | Tryb | Input (1M tokens) | Output (1M tokens) | Oszczędność |
|----------|-------|------|-------------------|-------------------|-------------|
| 🟦 **OpenAI** | GPT-5 Nano | Standard | $0.05 | $0.40 | - |
| 🟦 **OpenAI** | GPT-5 Mini | Standard | $0.25 | $2.00 | - |
| 🟦 **OpenAI** | GPT-5 | Standard | $1.25 | $10.00 | - |
| 🟣 **Anthropic** | Claude Sonnet 4 | Standard | $3.00 | $15.00 | - |
| 🟣 **Anthropic** | Claude Sonnet 4 | **Batch** | **$1.50** | **$7.50** | **-50%** 🎉 |

### Przykładowe koszty (10 000 tokenów input + 5 000 tokenów output):

- **GPT-5 Nano:** $0.0005 + $0.002 = **$0.0025**
- **Claude 4 (standard):** $0.03 + $0.075 = **$0.105**
- **Claude 4 (batch):** $0.015 + $0.0375 = **$0.0525** (Standard - 50%)

**💡 Tip:** Używaj batch API dla zadań niewymagających natychmiastowej odpowiedzi!

---

## 🗺️ Roadmap

### ✅ Wersja 1.0 (Obecna)

- ✅ Python client z async/await
- ✅ Node.js client z ES6 modules
- ✅ cURL examples z batch processing
- ✅ Interaktywne demo dla wszystkich klientów
- ✅ Export do Markdown/JSON/TXT

### 🚧 Wersja 1.1 (W przyszłości)

- 🔲 Streaming responses (real-time output)
- 🔲 RAG integration (vector stores)
- 🔲 Fine-tuning examples
- 🔲 Cost tracking dashboard

### 🔮 Wersja 2.0 (Planowane)

- 🔲 Web UI (React + FastAPI)
- 🔲 Multi-agent orchestration
- 🔲 Evaluation benchmarks
- 🔲 Docker containerization
- 🔲 GitHub Actions CI/CD

**🗳️ Masz pomysł?** [Otwórz Issue →](https://github.com/twoj-username/professor-LLM-maker/issues)

---

## 🤝 Contributing

Przyjmuję pull requesty! 🎉

### Wytyczne

✅ **Do:**
- Pisz czytelny kod z komentarzami
- Aktualizuj dokumentację
- Testuj przed commitowaniem
- Używaj semantic commit messages

❌ **Nie:**
- Nie commituj kluczy API (`.env`)
- Nie commituj `node_modules/`
- Nie łam istniejącej funkcjonalności

---

## 📜 Licencja

**CC-BY-NC-ND-4.0** - Creative Commons Attribution-NonCommercial-NoDerivatives 4.0

📖 **Oznacza to:**

✅ **Możesz:**
- Używać projektu do celów edukacyjnych
- Klonować i modyfikować lokalnie
- Dzielić się linkiem do repozytorium

❌ **Nie możesz:**
- Używać komercyjnie bez pozwolenia
- Publikować zmodyfikowanych wersji
- Usuwać informacji o autorze

---

## 📧 Kontakt


### Author: **Sebastian Ciborowski**
![Profile](https://img.shields.io/badge/👨‍🎓%20Computer%20Science%20Student-IT%20Enthusiast-blue?style=for-the-badge)
![Specialization](https://img.shields.io/badge/🛡️%20Specialist%20in-CyberSecurity%20|%20Python%20|%20AI-green?style=for-the-badge)

---

![Location](https://img.shields.io/badge/📍%20Location-Warszawa,%20Polska-red?style=for-the-badge)  
![Phone](https://img.shields.io/badge/📞_Whatsapp_&_Phone-%2B48%20539%20298%20079-orange?style=for-the-badge&logo=whatsapp)

---

[![GitHub](https://img.shields.io/badge/GitHub-sebastian--c87-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sebastian-c87)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sebastian%20Ciborowski-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/)  
[![Gmail](https://img.shields.io/badge/Gmail-Kontakt_bezpośredni-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ciborowski.s@gmail.com)

---
<div align="center">

### 🐛 Znalazłeś bug?

**[Otwórz Issue →](https://github.com/sebastian-c87/professor-LLM-maker/issues/new)**

### 💬 Pytania lub współpraca?

**Skontaktuj się przez [LinkedIn](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/) lub [Email](mailto:ciborowski.s@gmail.com)**

---



### ⭐ Jeśli ten projekt Ci pomógł, zostaw gwiazdkę na GitHub!

---

<br>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--5-412991?style=flat-square&logo=openai&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude--4-191919?style=flat-square&logo=anthropic&logoColor=white)

**[⬆️ Powrót na górę](#-llm-engineering-professor)**

</div>
