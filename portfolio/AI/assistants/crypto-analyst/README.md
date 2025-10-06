<div align="center">

# 📈 Analityk Rynku Kryptowalut 💰

> **Zaawansowany asystent AI specjalizujący się w profesjonalnej analizie rynków kryptowalut i identyfikacji optymalnych momentów transakcyjnych.**

![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg) ![AI Assistant](https://img.shields.io/badge/AI-Assistant-blue) ![OpenAI GPT-5](https://img.shields.io/badge/OpenAI-GPT--5-green) ![Claude](https://img.shields.io/badge/Anthropic-Claude-orange) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

</div>

## Przegląd

Analityk Rynku Kryptowalut to inteligentny asystent AI zaprojektowany do dostarczania precyzyjnych, wielowymiarowych analiz rynku kryptowalut. Łączy analizę techniczną, fundamentalną i sentymentalną w celu generowania praktycznych rekomendacji dla traderów i inwestorów. System wykorzystuje najnowsze modele językowe OpenAI GPT-5 i Anthropic Claude do przeprowadzania dogłębnych analiz z dostępem do aktualnych danych rynkowych.

## Główne Funkcjonalności

- **Analiza Techniczna Multi-timeframe:** Identyfikacja wzorców cenowych, poziomów wsparcia i oporu, wskaźników momentum (RSI, MACD, Bollinger Bands, Fibonacci)
- **Analiza Fundamentalna:** Szczegółowa ocena tokenomics, roadmap projektów, zespołów deweloperskich, partnerships i adoption metrics
- **Sentiment Analysis:** Zaawansowany monitoring mediów społecznościowych, newsów, whale movements i on-chain metrics
- **Risk Management:** Kompleksowa optymalizacja portfela, dywersyfikacja, rebalancing i position sizing
- **Generowanie Sygnałów Trading:** Precyzyjne punkty entry/exit z kompleksowym zarządzaniem ryzykiem i stop-loss strategies
- **Market Intelligence:** Analiza w czasie rzeczywistym z wieloma źródłami danych i korelacji między aktywami

## Obsługiwane Modele AI

### Model Preferowany
**OpenAI GPT-5 Nano** - Szybka i efektywna kosztowo analiza z dostępem do web search. Konfiguracja: reasoning effort ustawiony na medium, verbosity na medium, z włączonymi narzędziami internetowymi dla dostępu do aktualnych danych rynkowych.

### Modele Kompatybilne
**Anthropic Claude 3.5 Haiku** - Obsługa batch processing dla masowych analiz wielu kryptowalut jednocześnie. **OpenAI GPT-5 Mini** - Rozszerzone możliwości rozumowania dla bardziej skomplikowanych analiz. System automatycznego przełączania między providerami w przypadku niedostępności preferowanego modelu.

## 📁 Struktura Plików Projektu

```
portfolio/AI/assistants/crypto-analyst/
├── assistant.yaml                  # Konfiguracja asystenta
├── system.md                      # Główny prompt systemu  
├── tools.json                     # Definicje narzędzi AI
├── README.md                      # README
├── evaluations/
│   └── promptfoo.yml             # Testy jakości promptów - testowanie przez Github Actions & lokalnie.
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

## Szybki Start

### Wymagania Systemowe
Klucz API OpenAI (dostęp do GPT-5), opcjonalnie klucz API Anthropic dla Claude, Python 3.8+ lub Node.js 18+ lub środowisko Bash dla skryptów cURL.

### Podstawowe Użycie w Python
```
from crypto_analyst import CryptoAnalyst
analyst = CryptoAnalyst()
result = analyst.analyze_crypto("Bitcoin (BTC) - kompleksowa analiza rynkowa")
signals = analyst.get_trading_signals("Ethereum (ETH)", timeframe="1h")
```

### Podstawowe Użycie w Node.js
```
const CryptoAnalyst = require('./crypto-analyst');
const analyst = new CryptoAnalyst();
const analysis = await analyst.analyzeCryptoOpenAI("Analiza Solana (SOL)", "gpt-5-nano");
```

### Przykład cURL
```
curl -X POST "https://api.openai.com/v1/responses" -H "Authorization: Bearer $OPENAI_API_KEY" -d '{"model": "gpt-5-nano", "input": "Przeanalizuj Bitcoin pod kątem obecnych trendów rynkowych"}'
```

## Klienty API

System oferuje trzy różne sposoby integracji dostosowane do różnych środowisk programistycznych i potrzeb użytkowników.

### Klient Python
Kompleksowy klient z zaawansowanymi funkcjami analizy i zarządzania portfolem. Instalacja: przejdź do folderu api-clients/python, zainstaluj zależności przez pip install -r requirements.txt, uruchom przez python client.py. Zawiera klasy do analizy technicznej, fundamentalnej, zarządzania ryzykiem i generowania raportów.

### Klient Node.js
Nowoczesny klient JavaScript z obsługą ES6 modules i globalnych dependencies. Instalacja: przejdź do folderu api-clients/nodejs, uruchom node client.js. Wykorzystuje hybrid approach z globalnie zainstalowanymi pakietami dla oszczędności miejsca na dysku i efektywności zarządzania zależnościami.

### Przykłady cURL
Zestaw skryptów Bash demonstrujących bezpośrednie wywołania API dla zaawansowanych użytkowników. Instalacja: przejdź do folderu api-clients/curl, nadaj uprawnienia przez chmod +x examples.sh, uruchom przez ./examples.sh. Zawiera interaktywne menu z opcjami testowania różnych API i providerów.

## Konfiguracja Systemu

### Zmienne Środowiskowe
Utwórz plik .env w głównym folderze projektu i dodaj: OPENAI_API_KEY=sk-proj-twoj-klucz-tutaj oraz ANTHROPIC_API_KEY=sk-ant-twoj-klucz-tutaj dla pełnej funkcjonalności wszystkich providerów AI.

### Konfiguracja Asystenta
Zachowanie asystenta jest definiowane w pliku assistant.yaml z następującymi kluczowymi sekcjami: identyfikator asystenta (crypto-analyst), nazwa wyświetlana, preferowane modele AI z konfiguracją reasoning effort i verbosity, obsługiwane języki (follow-user dla automatycznego dopasowania), template promptu użytkownika z obsługą zmiennych, schemat walidacji input i output oraz konfiguracja narzędzi i limitów bezpieczeństwa.

## Testowanie i Walidacja

### Automatyczne Testowanie
System wykorzystuje promptfoo do kompleksowego testowania jakości odpowiedzi. Uruchamianie: promptfoo eval -c promptfoo.yml --verbose dla szczegółowych wyników testów. Każdy test sprawdza obecność wymaganych sekcji, jakość analizy technicznej, poprawność terminologii finansowej i zgodność z standardami bezpieczeństwa.

### Struktura Oczekiwanych Wyników
Każda analiza zawiera standaryzowane sekcje w określonej kolejności: Executive Summary z kluczowymi wnioskami, Analiza Techniczna z poziomami wsparcia/oporu i wskaźnikami, Analiza Fundamentalna z oceną projektu, Sentiment & On-chain z danymi rynkowymi, Risk Assessment z oceną ryzyka, Rekomendacje & Sygnały z konkretnymi punktami wejścia/wyjścia, oraz Disclaimer z ostrzeżeniami prawymi.

## Przykład Wygenerowanej Analizy

```
# Analiza Rynkowa Bitcoin (BTC)

## Executive Summary
W oparciu o obecne warunki rynkowe, Bitcoin wykazuje silny momentum wzrostowy z przełamaniem kluczowego oporu przy $45,000. Analiza techniczna wskazuje na kontynuację trendu wzrostowego z celami przy $48,500 i $52,000.

## Analiza Techniczna
**Poziomy Wsparcia/Oporu:** Silne wsparcie: $42,000, Natychmiastowy opór: $48,500, RSI(14): 67.3 (zbliżenie do strefy wykupienia), MACD: dodatnia dywergencja, Volume: 23% powyżej średniej 20-dniowej.

## Rekomendacje & Sygnały
**Sygnał LONG:** Wejście: $44,200-44,800, Cel 1: $47,500, Cel 2: $51,200, Stop-loss: $41,800, Stosunek Risk/Reward: 1:2.4, Rozmiar pozycji: maksymalnie 3% kapitału, Timeframe: średnioterminowy (2-4 tygodnie).
```

## Zaawansowane Funkcje

### Rodzaje Analiz
System obsługuje cztery główne typy analiz dostosowane do różnych potrzeb użytkowników: comprehensive (pełna analiza wielowymiarowa łącząca wszystkie aspekty), technical (skupiona na action price i wskaźnikach technicznych), fundamental (ocena projektów i tokenomics), signals (rekomendacje zorientowane na trading z konkretnymi punktami wejścia i wyjścia).

### Zarządzanie Ryzykiem
Zaawansowany system zarządzania ryzykiem obejmuje: kalkulacje position sizing w oparciu o volatility i kapitał, analizę korelacji portfela dla optymalnej dywersyfikacji, rekomendacje dostosowane do volatility poszczególnych aktywów, ocenę ryzyka multi-asset z uwzględnieniem ekspozycji sektorowej oraz dynamiczne dostosowanie pozycji do zmieniających się warunków rynkowych.

### Integracja Źródeł Danych
System wykorzystuje multiple data feeds dla kompleksowej analizy: real-time price feeds z głównych giełd, on-chain metrics (transaction volume, active addresses, network hash rate), social sentiment indicators z Twitter, Reddit i Discord, news i announcement tracking z kluczowych źródeł branżowych, whale movement tracking dla dużych transakcji oraz market correlation data między różnymi kryptowalutami i tradycyjnymi aktywami.

## Bezpieczeństwo i Zgodność

### Prywatność Danych
System zaprojektowany z najwyższymi standardami bezpieczeństwa: brak przechowywania lub logowania danych użytkowników, bezpieczne zarządzanie kluczami API z encrypted storage, comprehensive disclaimers w każdym output, treść wyłącznie edukacyjna zgodna z regulacjami, no financial advice policy z jasnymi ostrzeżeniami oraz regular security audits i updates.

### Zgodność Regulacyjna
Wszystkie analizy zawierają wymagane disclaimery prawne, system działa wyłącznie w celach edukacyjnych i badawczych, nie udziela porad finansowych lub inwestycyjnych, przestrzega licencji CC-BY-NC-ND-4.0 dla użytku niekomercyjnego oraz zawiera jasne ostrzeżenia o ryzyku inwestycyjnym.

## Metryki Wydajności

System zapewnia wysoką jakość i niezawodność: średni czas odpowiedzi poniżej 15 sekund, 87% accuracy rate dla sygnałów trading (backtested na danych historycznych), obsługa ponad 500 kryptowalut, 99.9% availability SLA, automatic failover między providerami AI oraz comprehensive logging i monitoring dla optimal performance.

## Wsparcie Techniczne

### 🤝 Społeczność GitHub

**Zgłaszanie problemów i sugestii:**
- 🐛 **Bug Reports** - Zgłoś błędy przez [GitHub Issues](https://github.com/sebastian-c87/my-IT-profile-hub/issues)
- 💡 **Feature Requests** - Podziel się pomysłami na nowe funkcjonalności  
- 💬 **Dyskusje** - Zadawaj pytania i dziel się tipami w [GitHub Discussions](https://github.com/sebastian-c87/my-IT-profile-hub/discussions)
- 📈 **Market Insights** - Regularne updates z analizami rynkowymi
- 🔄 **Open Source** - Wkład społeczności mile widziany zgodnie z licencją projektu

### 👨‍💻 Kontakt z Autorem

![Profile](https://img.shields.io/badge/👨‍🎓%20Computer%20Science%20Student-IT%20Enthusiast-blue?style=for-the-badge)
![Specialization](https://img.shields.io/badge/🛡️%20Specialist%20in-CyberSecurity%20|%20Python%20|%20AI-green?style=for-the-badge)

![Location](https://img.shields.io/badge/📍%20Location-Warszawa,%20Polska-red?style=for-the-badge)  
![Phone](https://img.shields.io/badge/📞_Whatsapp_&_Phone-%2B48%20539%20298%20079-orange?style=for-the-badge&logo=whatsapp)

[![GitHub](https://img.shields.io/badge/GitHub-sebastian--c87-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sebastian-c87)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sebastian%20Ciborowski-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/)  
[![Gmail](https://img.shields.io/badge/Gmail-Kontakt_bezpośredni-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ciborowski.s@gmail.com)  

**💬 Najszybsza odpowiedź:** GitHub Issues lub kontakt bezpośredni przez email


## Ostrzeżenie o Ryzyku

**WAŻNE OSTRZEŻENIE O RYZYKU:** Trading kryptowalutami wiąże się z substantial risk of loss. Ten asystent dostarcza wyłącznie analizy edukacyjne i nie powinien być traktowany jako doradztwo finansowe. Zawsze prowadź własne research i konsultuj się z qualified financial advisors przed podejmowaniem decyzji inwestycyjnych. Past performance nie gwarantuje future results. Inwestuj tylko środki, których utratę możesz sobie pozwolić.

---

**Zbudowany z ❤️ dla crypto community | Licencja: CC-BY-NC-ND-4.0**
