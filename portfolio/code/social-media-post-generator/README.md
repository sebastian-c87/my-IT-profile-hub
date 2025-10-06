<a align="center">

# 🚀 Generator Postów Social Media


> **Profesjonalne narzędzie do tworzenia treści zasilane OpenAI GPT-5**

</a>

Inteligentny generator treści społecznościowych wykorzystujący najnowsze możliwości OpenAI GPT-5-nano z Responses API. Aplikacja została zaprojektowana z myślą o polskich użytkownikach i obsługuje wszystkie popularne platformy społecznościowe.

---

## ✨ Kluczowe Funkcje

🎯 **Multi-platformowa optymalizacja**  
→ Twitter, LinkedIn, Facebook, Instagram z dedykowanymi ustawieniami

🎨 **Zróżnicowane style treści**  
→ Profesjonalny, Angażujący, Swobodny, Humorystyczny, Inspiracyjny

📊 **Inteligentna analiza wydajności**  
→ Przewidywanie zaangażowania i sugestie optymalizacji

🔤 **Zarządzanie limitami znaków**  
→ Automatyczna optymalizacja długości dla każdej platformy

🌍 **Web search integration**  
→ Aktualne informacje dla lepszej jakości treści

💾 **Historia i eksport**  
→ Zapisywanie sesji i eksport wyników do plików

---

## 🛠️ Wymagania Techniczne

**Python:** 3.8+ (zalecane: 3.12)  
**Kluczowe biblioteki:**
- openai >= 1.0.0
- python-dotenv >= 1.0.0  
- requests >= 2.28.0

**Wymagany:** Klucz API OpenAI z dostępem do GPT-5-nano

---

## ⚡ Szybki Start

### 1️⃣ Instalacja - Visual Studio Code

Sklonuj repozytorium i przejdź do folderu:
git clone <repo-url>
cd social-media-post-generator

Zainstaluj zależności:
pip install openai python-dotenv requests

Utwórz plik .env z kluczem API:
OPENAI_API_KEY=twój_klucz_api_tutaj

Uruchom aplikację:
python -m src.main

### 2️⃣ Użycie - Google Colab

Skopiuj plik colab_version.py do Google Colab

Uruchom komórkę z kodem - pakiety zostaną zainstalowane automatycznie

Użyj funkcji setup() do konfiguracji API

---

## 🎮 Instrukcja Użycia

### 💻 Tryb Visual Studio Code

Po uruchomieniu aplikacji dostępne są opcje:

**1. Generuj pojedynczy post** - Interaktywne tworzenie pojedynczego posta  
**2. Generuj posty wsadowo** - Tworzenie wielu postów naraz  
**3. Analizuj istniejący post** - Ocena potencjału zaangażowania  
**4. Zobacz historię sesji** - Przegląd wygenerowanych treści  
**5. Pomoc i wskazówki** - Szczegółowe informacje o funkcjach  

### 📱 Tryb Google Colab
```
Podstawowe funkcje (interfejs polski):  
setup()                                    # Konfiguracja API  
generuj_post("twój temat")                 # Pojedynczy post    
tryb_interaktywny()                        # Pełny interfejs  
generuj_wsadowo(["temat1", "temat2"])      # Wiele postów  
pokaz_historie()                           # Historia sesji  
eksportuj_posty()                          # Zapis do pliku  
```
```
Funkcje anglojęzyczne (aliasy):
generate_post(), interactive_mode(), batch_generate(), show_history(), export_posts() 
```


## 📋 Przykłady Użycia

### Przykład 1: Pojedynczy post
>temat = "Sztuczna inteligencja w 2025"  
>platforma = "linkedin"  
>styl = "professional"

```
post = generuj_post(temat, platforma, styl)
print(post)
```

### Przykład 2: Generowanie wsadowe
```>tematy = [
    "Najnowsze trendy w AI",
    "Automatyzacja procesów biznesowych", 
    "Przyszłość pracy zdalnej"
]

wyniki = generuj_wsadowo(tematy, "twitter", "engaging")
```
### Przykład 3: Analiza istniejącego posta
>existing_post = "Twój istniejący post tutaj..."
tryb_interaktywny()  # Wybierz opcję 3 - analiza


## 📁 Struktura Projektu
```
social-media-post-generator/  
├── src/  
│   ├── __init__.py              # Inicjalizacja pakietu  
│   ├── main.py                  # Główna aplikacja (polski interfejs)
│   ├── config.py                # Konfiguracja aplikacji  
│   └── openai_client.py         # Klient OpenAI z GPT-5-nano
├── .env                         # Klucze API (nie commitować!)
├── colab_version.py             # Wersja standalone dla Colab
├── requirements.txt             # Lista zależności
├── README.md                    # Ta dokumentacja
├── logs/                        # Automatycznie tworzone logi
└── exports/                     # Eksportowane pliki
```

## ⚙️ Konfiguracja

> ### Plik ".env"
OPENAI_API_KEY=sk-your-api-key-here  
LOG_LEVEL=INFO  
MAX_RETRIES=3  
TIMEOUT=30  

### Dostępne platformy
- **twitter** - Posty do 280 znaków z hashtagami
- **linkedin** - Profesjonalne treści biznesowe  
- **facebook** - Angażujące posty zachęcające do interakcji
- **instagram** - Treści wizualno-narracyjne z hashtagami
- **universal** - Uniwersalne posty wieloplatformowe

### Style treści
- **professional** - Biznesowy, autorytatywny ton
- **engaging** - Przyciągający, interaktywny styl
- **casual** - Przyjazny, rozmówkowy charakter  
- **humorous** - Lekki, zabawny ton
- **inspirational** - Motywujący, podnoszący na duchu

***

## 🔧 Rozwiązywanie Problemów

### Pusty post / Błąd generowania
✅ Sprawdź klucz API OpenAI  
✅ Upewnij się, że masz dostęp do GPT-5-nano  
✅ Sprawdź połączenie internetowe (web search)  
✅ Spróbuj prostszego tematu

### Błędy importu w Colab
✅ Uruchom ponownie komórkę z kodem  
✅ Sprawdź czy pakiety zostały zainstalowane  
✅ Użyj setup() przed innymi funkcjami

### Problemy z kodowaniem znaków
✅ Upewnij się, że używasz Python 3.8+  
✅ Sprawdź ustawienia kodowania terminala (UTF-8)

***

## 📈 Funkcje Zaawansowane

### Web Search Integration
Aplikacja automatycznie wyszukuje aktualne informacje w internecie dla lepszej jakości treści.

### Fallback System  
Trójpoziomowy system zapasowy zapewnia generowanie treści nawet przy problemach z API.

### Smart Character Management
Inteligentne przycinanie zachowujące hashtagi i strukturę posta.

### Performance Analysis
Szczegółowa analiza potencjału zaangażowania z konkretnymi sugestiami poprawy.

***

## 📝 Licencja

*MIT License* - możesz swobodnie używać, modyfikować i dystrybuować.

***

## 👨‍💻 Wsparcie

**Problemy techniczne:** Sprawdź sekcję "Rozwiązywanie Problemów"  
**Sugestie funkcji:** Utwórz issue w repozytorium  
**Dokumentacja API:** [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)

***

## 🔄 Historia Wersji

**v1.0.0** (Październik 2025)
- ✅ Pełna integracja z OpenAI GPT-5-nano  
- ✅ Polski interfejs użytkownika
- ✅ Web search integration
- ✅ Multi-platformowa optymalizacja
- ✅ Wersja standalone dla Google Colab
- ✅ System analizy wydajności

---

## ⚡ Pro Tips

🎯 **Tematy konkretne** generują lepsze wyniki niż ogólne  
📱 **Testuj różne style** dla różnych platform  
📊 **Używaj analizy** do optymalizacji treści  
💾 **Eksportuj wyniki** dla pracy zespołowej  
🔄 **Generuj wsadowo** dla efektywności czasowej

---

### 👨‍💻 Kontakt z Autorem

![Profile](https://img.shields.io/badge/👨‍🎓%20Computer%20Science%20Student-IT%20Enthusiast-blue?style=for-the-badge)
![Specialization](https://img.shields.io/badge/🛡️%20Specialist%20in-CyberSecurity%20|%20Python%20|%20AI-green?style=for-the-badge)

![Location](https://img.shields.io/badge/📍%20Location-Warszawa,%20Polska-red?style=for-the-badge)  
![Phone](https://img.shields.io/badge/📞_Whatsapp_&_Phone-%2B48%20539%20298%20079-orange?style=for-the-badge&logo=whatsapp)

[![GitHub](https://img.shields.io/badge/GitHub-sebastian--c87-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sebastian-c87)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sebastian%20Ciborowski-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/)  
[![Gmail](https://img.shields.io/badge/Gmail-Kontakt_bezpośredni-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ciborowski.s@gmail.com)  

**💬 Najszybsza odpowiedź:** GitHub Issues lub kontakt bezpośredni przez email

---

*Zbudowano z ❤️ dla polskiej społeczności social media*