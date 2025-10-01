# 🤖 Python Full-Stack Developer - AI Assistant

> **Zaawansowany asystent AI do generowania kompletnych aplikacji web Python**

[![AI Agent CI](https://img.shields.io/badge/Github-Actions-red?logo=github)](https://github.com/sebastian-c87/my-IT-profile-hub/actions/workflows/ai-ci.yml)
[![License: CC-BY-NC-ND-4.0](https://img.shields.io/badge/License-CC--BY--NC--ND--4.0-blue.svg?logo=readme&logoColor=white)](LICENSE)
[![OpenAI GPT-5](https://img.shields.io/badge/OpenAI-GPT--5-green?logo=openai)](https://platform.openai.com/)
[![Anthropic Claude](https://img.shields.io/badge/Anthropic-Claude--3.5-orange.svg?logo=claude&logoColor=white)](https://claude.ai/)

## 📋 Opis Projektu

**Python Full-Stack Developer Assistant** to zaawansowany system **prompt engineering** wykorzystujący najnowsze modele AI do automatycznego generowania kompletnych aplikacji web. System łączy **GPT-5-nano** (OpenAI Responses API) z **Claude-3-5-Haiku** (Anthropic Batch API), oferując optymalizację kosztów i najwyższą jakość kodu.

### ✨ Kluczowe Funkcje

- 🏗️ **Kompletne aplikacje** - od architektury po deployment
- 💰 **Optymalizacja kosztów** - GPT-5 + Claude 
- 🌐 **Obsługa dwujęzyczna** - Polski i Angielski
- 🔧 **Trzy przykładowe sposoby użycia** - Python, Node.js, cURL
- ✅ **Automatyczne testy** - GitHub Actions + promptfoo
- 📚 **Szczegółowa dokumentacja** - quickstart guides i przykłady

### 🛠️ Generowane Technologie

**Backend:** FastAPI, Flask, Django • SQLAlchemy, MongoDB • Redis, Celery • JWT Authentication

**Frontend:** React, Vue.js • TypeScript • Tailwind CSS, Bootstrap • Redux, Pinia

**DevOps:** Docker, docker-compose • CI/CD pipelines • Environment config • Database migrations

**API:** REST API design • OpenAPI documentation • External integrations • Error handling

## 📁 Struktura Plików Projektu

```
portfolio/AI/assistants/python-fullstack-dev/
├── assistant.yaml                  # Konfiguracja asystenta
├── system.md                      # Główny prompt systemu  
├── tools.json                     # Definicje narzędzi AI
├── README.md                      # Dokumentacja projektu
├── evaluations/
│   └── promptfoo.yml             # Testy jakości promptów
├── api-clients/
│   ├── .env                      # Klucze API (nie commitowane)
│   ├── python/
│   │   ├── client.py             # Python SDK
│   │   ├── demo.py               # Przykłady użycia Python
│   │   ├── __init__.py
│   │   └── requirements.txt      # Zależności Python
│   ├── nodejs/
│   │   ├── client.js             # Node.js ES6 client  
│   │   ├── demo.js               # Przykłady użycia Node.js
│   │   └── package.json          # Zależności npm
│   └── curl/
│       └── examples.sh           # Interactive cURL scripts
└── quickstart/                   # Szybkie przewodniki *.MD
```

## Wykorzystywane plik w strukturze (repo level):
```
.github/workflows/
└── ai-ci.yml                     # GitHub Actions workflow

portfolio/AI/_templates/
└── agent.spec.schema.json        # JSON Schema walidacji
```

## 🚀 Szybki Start

### Wymagania Systemowe
- **Python 3.12+**
- **Node.js 18+**
- **OpenAI API Key** (GPT-5 access)
- **Anthropic API Key** (opcjonalnie)

### Instalacja

- git clone https://github.com/sebastian-c87/my-IT-profile-hub.git
- cd my-IT-profile-hub/portfolio/AI/assistants/python-fullstack-dev


### Konfiguracja API keys

- echo "OPENAI_API_KEY=sk-your-key" > api-clients/.env
- echo "ANTHROPIC_API_KEY=sk-ant-your-key" >> api-clients/.env


### Użycie - Python SDK

cd api-clients/python
pip install openai anthropic python-dotenv
python demo.py


### Użycie - Node.js SDK

cd api-clients/nodejs
npm install openai @anthropic-ai/sdk dotenv fs-extra
node demo.js


### Użycie - cURL Scripts

cd api-clients/curl
export OPENAI_API_KEY="sk-your-key"
chmod +x examples.sh && ./examples.sh


## 📊 Przykładowe Rezultaty

### Input

```
Pomysł: "E-commerce platform z płatnościami Stripe"  
Wymagania: "FastAPI, React, PostgreSQL, Docker"
```


### Output (16,000+ znaków)
- 🏗️ **Architektura aplikacji** - diagramy, technologie, schemat bazy danych
- 📁 **Struktura projektu** - kompletna organizacja plików i folderów
- ⚙️ **Backend implementation** - FastAPI + SQLAlchemy + Pydantic models
- 🎨 **Frontend implementation** - React + TypeScript + Tailwind CSS
- 🔗 **API Integration** - Stripe payments + comprehensive error handling
- 🚀 **Setup & Deployment** - Docker, environment, database migrations

## 🔧 Zaawansowana Konfiguracja

### Strategia Kosztów

**Hierarchia providerów (najtańszy → najdroższy)**  
- OpenAI GPT-5-nano # $0.02/16k chars, ~2s response
- Claude-3-5-Haiku # $0.01/16k chars, ~30s response (batch)


### Customizacja Modeli

```
models:
preferred:
- provider: openai
model: gpt-5-nano
compatible:
- provider: anthropic
model: claude-3-5-haiku-20241022
```


## 🧪 Testowanie i Jakość

### GitHub Actions Workflow
- ✅ **Schema validation** - walidacja `assistant.yaml` przeciwko JSON Schema
- ✅ **Prompt testing** - 6 scenariuszy testowych z promptfoo
- ✅ **Quality assurance** - automatyczna ocena jakości odpowiedzi
- ✅ **CI/CD integration** - testy przy każdym push i pull request

### Lokalne Testowanie

**GitHub Actions lokalnie (Windows)**  
choco install act-cli
act -W .github/workflows/ai-ci.yml --secret OPENAI_API_KEY=your-key

**Prompt testing**  
cd evaluations && npx promptfoo eval -c promptfoo.yml


## 📈 Metryki Wydajności

| **Provider** | **Model** | **Czas odpowiedzi** | **Koszt (~16k)** | **Jakość** |
|--------------|-----------|-------------------|------------------|------------|
| OpenAI | GPT-5-nano | ~2 sekundy | $0.02 | ⭐⭐⭐⭐ |
| Anthropic | Claude-3-5-Haiku | ~30 sekund* | $0.01 | ⭐⭐⭐⭐⭐ |

> *\* Claude Batch API - asynchroniczne przetwarzanie z 50% zniżką*

## 🛡️ Bezpieczeństwo

- 🔐 **API Keys** zabezpieczone w `.env` (nie commitowane do repo)
- 🚫 **Zero data retention** - `store: false` w każdym API call
- ✅ **Input validation** - comprehensive sanitization i validation
- 📝 **Audit logging** - pełne logi w GitHub Actions workflows

## 🤝 Kontrybuty i Rozwój

### Zgłaszanie Issues
Używaj [**GitHub Issues**](https://github.com/sebastian-c87/my-IT-profile-hub/issues) z następującymi informacjami:
- **Dokładny opis** problemu z error messages
- **Kroki reprodukcji** - step-by-step guide
- **Environment info** - OS, Python/Node.js versions
- **Input/Output examples** - co wysłałeś vs co otrzymałeś

### Development Workflow
1. **Fork repository** i stwórz feature branch
2. **Edytuj prompts** w `system.md` zgodnie z best practices
3. **Testuj lokalnie** z promptfoo: `npx promptfoo eval`
4. **Uruchom ACT** - lokalne testy GitHub Actions
5. **Submit Pull Request** z detailed description

## 📄 Licencja

**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International**

- ✅ **Użycie osobiste i edukacyjne** - bez ograniczeń
- ✅ **Sharing i distribution** - z proper attribution
- ❌ **Użycie komercyjne** - wymaga explicit permission
- ❌ **Derivative works** - no modifications allowed

## 👨‍💻 Autor

**Sebastian C.** - *Prompt Engineer & Full-Stack Developer* - IT student CyberSecurity Specialist

- 📧 **Kontakt:** [GitHub Profile](https://github.com/sebastian-c87)
- 💼 **LinkedIn:** [Professional Profile](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/)
- 🌐 **Portfolio:** [Complete IT Profile Hub](https://github.com/sebastian-c87/my-IT-profile-hub)

## 🔗 Przydatne Linki

- [**OpenAI Responses API**](https://platform.openai.com/docs/api-reference/responses) - Official documentation
- [**Anthropic Claude API**](https://docs.anthropic.com/en/api/messages-batches) - Batch processing docs
- [**Promptfoo Framework**](https://promptfoo.dev/) - LLM testing and evaluation
- [**GitHub Actions Guide**](https://docs.github.com/actions) - CI/CD automation

---

<div align="center">

**⭐ Jeśli projekt okazał się przydatny, zostaw gwiazdkę na GitHub!**

*Built your app with ❤️ using GPT-5-nano and Claude-3.5-Haiku*

</div>
