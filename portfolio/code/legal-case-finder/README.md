
---

<div align="center">

# ⚖️ Legal Case Finder

### **Inteligentny asystent prawny zasilany przez GPT-5-nano z wyszukiwaniem internetowym**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge)![open](https://img.shields.io/badge/OpenAI-GPT--5--mini-412991?style=for-the-badge)![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)![colab](https://img.shields.io/badge/Google-Colab-F9AB00?style=for-the-badge)

**Profesjonalne narzędzie do analizy problemów prawnych w oparciu o polskie prawo**

[Funkcje](#-funkcje) -  [Instalacja](#-instalacja) -  [Użycie](#-użycie) -  [API Reference](#-api-reference) -  [Kontakt](#-autorzy)

</div>

---

## 📋 Spis treści

- [O projekcie](#-o-projekcie)
- [Funkcje](#-funkcje)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Konfiguracja](#-konfiguracja)
- [Użycie](#-użycie)
- [Google Colab](#-google-colab)
- [Architektura](#-architektura)
- [Dziedziny prawa](#-dziedziny-prawa)
- [SAOS Integration](#-saos-integration)
- [Przykłady](#-przykłady)
- [API Reference](#-api-reference)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Kontakt](#-autorzy)

***

## 🎯 O projekcie

**Legal Case Finder** to zaawansowany asystent prawny wykorzystujący moc **OpenAI GPT-5-nano** z natywnym wyszukiwaniem internetowym. Aplikacja oferuje szczegółową analizę problemów prawnych w oparciu o aktualne przepisy polskiego prawa, orzecznictwo sądów i praktykę prawniczą.

### 🌟 Dlaczego Legal Case Finder?

- **🚀 Najnowsza technologia** - wykorzystuje GPT-5-nano z Responses API i web search
- **⚖️ Prawo polskie** - specjalizacja w przepisach obowiązujących w Polsce
- **🔍 Wyszukiwanie internetowe** - automatyczne przeszukiwanie aktualnych przepisów i orzeczeń
- **📚 11 dziedzin prawa** - od prawa karnego po AI i własność intelektualną
- **🏛️ Integracja z SAOS** - dostęp do oficjalnych orzeczeń sądowych z systemu Ministerstwa Sprawiedliwości
- **💻 Dwa tryby** - aplikacja desktopowa i wersja Google Colab
- **💾 Eksport wyników** - zapisywanie analiz w formatach TXT i JSON
- **🔒 Bezpieczeństwo** - właściwe zarządzanie kluczami API

---

## ✨ Funkcje

### 🔍 Analiza kompleksowa problemu prawnego

Szczegółowa analiza obejmująca:
- **Podsumowanie sytuacji** - zrozumienie istoty problemu
- **Konkretne przepisy prawne** - dokładne numery artykułów z polskiego prawa
- **Komentarz do przepisów** - wyjaśnienie w prostym języku
- **Instrukcja działania** - krok po kroku co robić w danej sytuacji

### ⚖️ Wyszukiwanie orzeczeń SAOS

Integracja z oficjalnym systemem SAOS (System Analizy Orzeczeń Sądowych):
- Wyszukiwanie orzeczeń Sądu Najwyższego
- Orzeczenia sądów powszechnych
- Orzeczenia sądów administracyjnych
- Pełne informacje: sygnatura, data, sąd, sędziowie, fragment treści

### 💾 Zarządzanie wynikami

- **Eksport do TXT** - czytelny format tekstowy
- **Eksport do JSON** - strukturalne dane do dalszej obróbki
- **Historia analiz** - śledzenie wszystkich przeprowadzonych analiz
- **Popup z rekomendacją** - profesjonalne okno systemowe z kontaktem do prawnika

### 🌐 Wyszukiwanie internetowe

System automatycznie przeszukuje internet w poszukiwaniu:
- Aktualnych przepisów prawnych
- Orzeczeń i wyroków sądowych
- Komentarzy prawniczych i interpretacji
- Zmian w prawie i nowych regulacji

***

## 🔧 Wymagania

### Wymagania systemowe

- **Python**: 3.8 lub nowszy
- **System operacyjny**: Windows, macOS, Linux
- **RAM**: Minimum 4GB (zalecane 8GB)
- **Połączenie internetowe**: Wymagane do komunikacji z OpenAI API i wyszukiwania

### Wymagane pakiety

- **openai** >= 1.0.0 - Oficjalny klient OpenAI Python
- **requests** >= 2.31.0 - Obsługa HTTP dla SAOS API
- **python-dotenv** >= 1.0.0 - Zarządzanie zmiennymi środowiskowymi
- **tkinter** - Wbudowane w Python (interfejs okien systemowych)

### Klucz API

Wymagany klucz API OpenAI z dostępem do modeli GPT-5. Uzyskaj go na: https://platform.openai.com/api-keys

***

## 📦 Instalacja

### Metoda 1: Klonowanie repozytorium

    git clone https://github.com/yourusername/legal-case-finder.git
    cd legal-case-finder

### Metoda 2: Pobieranie jako ZIP

Pobierz i rozpakuj archiwum ZIP z GitHub, następnie przejdź do katalogu projektu.

### Instalacja zależności

    pip install -r requirements.txt

Lub instalacja ręczna:

    pip install openai>=1.0.0 requests>=2.31.0 python-dotenv>=1.0.0

***

## ⚙️ Konfiguracja

### 1. Utwórz plik .env

W głównym katalogu projektu utwórz plik `.env` i dodaj swój klucz API:

    OPENAI_API_KEY=sk-your-api-key-here

### 2. Dostosuj konfigurację (opcjonalne)

Edytuj plik `src/config.py` aby dostosować parametry:

**Model Configuration:**
- **model_name** - model OpenAI (domyślnie: gpt-5-nano)
- **reasoning_effort** - poziom rozumowania (domyślnie: medium)
- **max_output_tokens** - maksymalna długość odpowiedzi (domyślnie: 20000)

**Lawyer Information:**
- **lawyer_name** - imię i nazwisko prawnika
- **lawyer_location** - lokalizacja kancelarii
- **lawyer_description** - opis profesjonalisty

### 3. Weryfikacja instalacji

    cd src
    python main.py

Jeśli wszystko działa poprawnie, zobaczysz menu główne aplikacji.

***

## 🚀 Użycie

### Uruchomienie aplikacji lokalnej

    cd src
    python main.py

### Podstawowy przepływ pracy

**Krok 1:** Wybierz opcję "1. Analiza problemu prawnego"

**Krok 2:** Wybierz dziedzinę prawa (1-11)

**Krok 3:** Opisz swój problem prawny (zakończ Enter)

**Krok 4:** Poczekaj na szczegółową analizę (20-60 sekund)

**Krok 5:** Przeczytaj wyniki z konkretnymi przepisami i instrukcją

**Krok 6:** Zapisz analizę wybierając opcję "3. Pobierz analizę"

### Menu główne

**1. 🔍 Analiza problemu prawnego**
- Główna funkcja aplikacji
- Automatyczne wyszukiwanie w internecie
- Szczegółowa analiza z przepisami

**2. ⚖️ Przeglądaj orzeczenia sądowe (SAOS)**
- Dostęp do oficjalnych orzeczeń
- Filtrowanie po typie sądu
- Pełne informacje o orzeczeniach

**3. 💾 Pobierz analizę**
- Zapis do pliku TXT
- Opcjonalny eksport do JSON
- Pełna dokumentacja problemu i analizy

**4. ❓ Pomoc i informacje o dziedzinach prawa**
- Instrukcja użytkowania
- Szczegółowe opisy dziedzin prawa
- Wskazówki i najlepsze praktyki

**5. 🚪 Zakończ**
- Popup z informacją o prawnika
- Profesjonalne okno systemowe
- Kontakt do specjalisty

***

## 🔬 Google Colab

### Uruchomienie w Colab

**Krok 1:** Otwórz nowy notebook w Google Colab

**Krok 2:** Dodaj klucz API jako Secret
- Kliknij ikonę klucza 🔑 w lewym pasku
- Name: `OPENAI_API_KEY`
- Value: Twój klucz API OpenAI
- Włącz "Notebook access"

**Krok 3:** Wklej cały kod z pliku `colab_version.py`

**Krok 4:** Uruchom komórkę i wywołaj `setup()`

### Funkcje Colab

**setup()** - Główna funkcja uruchamiająca aplikację w trybie interaktywnym

**analyze(problem, domain)** - Szybka analiza bez menu

    analyze("Spór o granicę działki z sąsiadem", "Prawo nieruchomości")

### Uproszczone menu Colab

1. 🔍 Analiza problemu prawnego
2. 💾 Pobierz analizę
3. ❓ Pomoc i informacje
4. 🚪 Zakończ

(SAOS niedostępny w Colab - wymaga lokalnego środowiska)

### Pobieranie wyników z Colab

1. Kliknij ikonę plików 📁 w lewym pasku
2. Znajdź plik `analiza_prawna_*.txt`
3. Kliknij prawym przyciskiem → Download

***

## 🏗️ Architektura

### Struktura projektu

    legal-case-finder/
    ├── src/
    │   ├── __init__.py          # Inicjalizacja pakietu
    │   ├── main.py              # Główna aplikacja desktopowa
    │   ├── openai_client.py     # Klient GPT-5-nano
    │   ├── saos_client.py       # Klient SAOS API
    │   └── config.py            # Konfiguracja aplikacji
    ├── colab_version.py         # Wersja dla Google Colab
    ├── requirements.txt         # Zależności Python
    ├── .env.example            # Przykład konfiguracji
    ├── README.md               # Dokumentacja
    └── LICENSE                 # Licencja MIT

### Komponenty systemu

**OpenAI Client**
- Komunikacja z GPT-5-nano przez Responses API
- Natywne web search dla aktualnych przepisów
- Strukturalna analiza prawna z przepisami

**SAOS Client**
- Integracja z oficjalnym API Ministerstwa Sprawiedliwości
- Wyszukiwanie orzeczeń wszystkich polskich sądów
- Parsowanie i formatowanie wyników

**Config Manager**
- Zarządzanie konfiguracją aplikacji
- Zmienne środowiskowe (.env)
- Informacje o polecanym prawniku

**Main Application**
- Interface użytkownika w konsoli
- Zarządzanie przepływem aplikacji
- Popup okna systemowe przy zakończeniu

***

## 📚 Dziedziny prawa

Aplikacja wspiera **11 dziedzin prawa polskiego**:

### 1. ⚖️ Prawo karne
Przestępstwa, wykroczenia, odpowiedzialność karna, kary, postępowanie karne, ściganie

### 2. 📜 Prawo cywilne
Umowy, własność, zobowiązania, odszkodowania, roszczenia cywilne, dochodzenie roszczeń

### 3. 👨‍👩‍👧 Prawo rodzinne
Małżeństwo, rozwód, separacja, alimenty, władza rodzicielska, opieka nad dziećmi

### 4. 💼 Prawo pracy
Umowy o pracę, wynagrodzenie, urlopy, zwolnienia, mobbing, dyskryminacja w pracy

### 5. 🏺 Prawo spadkowe
Spadki, testamenty, dziedziczenie ustawowe, zachowek, dział spadku, odrzucenie spadku

### 6. 🏢 Prawo gospodarcze
Działalność gospodarcza, spółki, upadłość, restrukturyzacja, konkurencja

### 7. 🏛️ Prawo administracyjne
Decyzje administracyjne, samorząd, budownictwo, środowisko, skargi do sądów administracyjnych

### 8. 💰 Prawo podatkowe
Podatki (VAT, PIT, CIT), deklaracje, kontrole skarbowe, interpretacje podatkowe

### 9. 🏠 Prawo nieruchomości
Kupno, sprzedaż, najem, dzierżawa, własność, księgi wieczyste, służebności

### 10. 🛒 Prawo konsumenckie
Ochrona konsumentów, reklamacje, zwroty, umowy konsumenckie, nieuczciwe praktyki

### 11. 🤖 Prawo własności intelektualnej i AI
Prawa autorskie, patenty, znaki towarowe, AI, ochrona danych, RODO, cyfryzacja

***

## 🏛️ SAOS Integration

### Czym jest SAOS?

**SAOS** (System Analizy Orzeczeń Sądowych) to oficjalny, publiczny i darmowy system udostępniony przez Ministerstwo Sprawiedliwości RP zawierający orzeczenia polskich sądów.

### Dostępne typy sądów

- **Sąd Najwyższy** - najwyższe orzeczenia precedensowe
- **Sądy powszechne** - rejonowe, okręgowe, apelacyjne
- **Sądy administracyjne** - wojewódzkie i NSA

### Informacje w orzeczeniach

Każde orzeczenie zawiera:
- **Sygnatura sprawy** - unikalny identyfikator
- **Data wyroku** - kiedy zapadło orzeczenie
- **Nazwa sądu** - który sąd wydał wyrok
- **Sędziowie** - skład orzekający
- **Fragment treści** - podgląd uzasadnienia
- **Link do pełnego orzeczenia** - na stronie SAOS

### Parametry wyszukiwania

- Słowa kluczowe (wyszukiwanie w całym tekście)
- Typ sądu (filtrowanie)
- Liczba wyników (1-100)
- Sortowanie (domyślnie: od najnowszych)

### Przykłady użycia

**Wyszukiwanie ogólne:**

    Słowa kluczowe: "alimenty na dziecko"
    Typ sądu: Wszystkie
    Wyniki: 5 najnowszych orzeczeń

**Wyszukiwanie specjalistyczne:**

    Słowa kluczowe: "nieważność małżeństwa"
    Typ sądu: Sąd Najwyższy
    Wyniki: Precedensowe orzeczenia SN

***

## 💡 Przykłady

### Przykład 1: Analiza problemu spadkowego

**Input:** "Podział majątku po dziadku, który był w separacji z babcią. Mieli dwa mieszkania z czego na oba zapracowała babcia, ale po rozstaniu dziadek mieszkał w jednym babcia w drugim. Babcia ma wydziedziczoną córkę, ale zrobiła to dopiero po śmierci dziadka, więc córka ma prawo do spadku po dziadku. Ja jako pełnoletni wnuk żyjący z babcią i z testamentem babci zapisanym na siebie jakie mam prawa do spadku po dziadku?"

**Output:**
- Szczegółowa analiza sytuacji prawnej
- Konkretne artykuły Kodeksu cywilnego (art. 991, 992, 993, 1008-1010 KC)
- Uchwała Sądu Najwyższego III CZP 23/19
- Wyjaśnienie zachowku i wydziedziczenia
- Instrukcja działania krok po kroku
- Rekomendacja prawnika specjalisty

### Przykład 2: Wyszukiwanie orzeczeń o rozwodzie

**Input:** "rozwód z orzeczeniem o winie"

**Output:**
- 5 aktualnych orzeczeń sądów
- Sygnatury spraw i daty
- Składy orzekające
- Fragmenty uzasadnień
- Linki do pełnych tekstów na SAOS

### Przykład 3: Prawo pracy - mobbing

**Input:** "Pracodawca systematycznie obniża mi wynagrodzenie i pomija przy awansach mimo dobrych wyników"

**Output:**
- Analiza pod kątem mobbingu (art. 94³ Kodeksu pracy)
- Przepisy o ochronie pracownika
- Możliwości prawne (pozew, inspekcja pracy)
- Terminy i procedury
- Dokumentacja potrzebna do sprawy

***

## 📚 API Reference

### ColabLegalAIClient

**Inicjalizacja:**

    client = ColabLegalAIClient(api_key="your-api-key")

**Główna metoda - analyze_legal_problem:**

    analyze_legal_problem(problem_description: str, legal_domain: str) -> Dict[str, Any]

**Parametry:**
- **problem_description** (str): Szczegółowy opis problemu prawnego
- **legal_domain** (str): Wybrana dziedzina prawa (np. "Prawo spadkowe")

**Zwraca:**

    {
        "analysis": "Szczegółowa analiza prawna...",
        "legal_domain": "Prawo spadkowe",
        "success": True,
        "timestamp": "2025-10-08T01:30:00.000000"
    }

### SAOSClient

**Inicjalizacja:**

    saos_client = SAOSClient()

**Główna metoda - search_judgments:**

    search_judgments(query: str, page_size: int = 5, court_type: Optional[str] = None) -> List[Dict[str, Any]]

**Parametry:**
- **query** (str): Słowa kluczowe do wyszukania
- **page_size** (int): Liczba wyników (1-100, domyślnie 5)
- **court_type** (Optional[str]): Typ sądu ("SUPREME", "COMMON", "ADMINISTRATIVE", None=wszystkie)

**Zwraca:**

    [
        {
            "case_number": "IV Ka 665/24",
            "date": "2025-09-20",
            "court_name": "Sąd Okręgowy w Piotrkowie Trybunalskim",
            "judges": "Jan Kowalski, Anna Nowak",
            "text_preview": "Fragment uzasadnienia...",
            "url": "https://www.saos.org.pl/judgments/523792"
        },
        ...
    ]

**Pomocnicza metoda - format_judgment_display:**

    format_judgment_display(judgment: Dict[str, Any]) -> str

Formatuje orzeczenie do eleganckie wyświetlenia w konsoli z ramką.

***

## 🐛 Rozwiązywanie problemów

### Problem: "Invalid API key"

**Rozwiązanie:** Sprawdź czy klucz API jest poprawny i aktywny w pliku .env lub Colab Secrets

### Problem: "Rate limit exceeded"

**Rozwiązanie:** Poczekaj chwilę przed kolejnym zapytaniem. GPT-5-nano ma limity requestów. Możesz zwiększyć limity w swoim koncie OpenAI.

### Problem: "Pusta analiza prawna"

**Przyczyna:** max_output_tokens ustawione za nisko

**Rozwiązanie:** Zwiększ max_output_tokens w config.py (zalecane: 20000)

### Problem: "SAOS 404 Not Found"

**Przyczyna:** Niepoprawny endpoint API

**Rozwiązanie:** Sprawdź czy używasz właściwego endpointu: https://www.saos.org.pl/api/search/judgments

### Problem: "Popup nie wyświetla się na pierwszym planie"

**Rozwiązanie:** Kod zawiera `root.attributes('-topmost', True)` - upewnij się że ta linijka jest w metodzie `_display_goodbye()`

### Problem: "ModuleNotFoundError: No module named 'tkinter'"

**Przyczyna:** Brak tkinter (rzadkie na Windows/Mac, częste na niektórych Linuxach)

**Rozwiązanie Ubuntu/Debian:**

    sudo apt-get install python3-tk

**Rozwiązanie Fedora:**

    sudo dnf install python3-tkinter

***

## 🤝 Contributing

Zapraszamy do współpracy! Każdy wkład jest cenny.

### Jak pomóc?

**1. Fork projektu**

**2. Stwórz branch dla swojej funkcji:**

    git checkout -b feature/AmazingFeature

**3. Commit zmian:**

    git commit -m 'Add some AmazingFeature'

**4. Push do brancha:**

    git push origin feature/AmazingFeature

**5. Otwórz Pull Request**

### Wytyczne

- Zachowaj spójność stylu kodu (PEP 8)
- Dodaj testy dla nowych funkcji
- Zaktualizuj dokumentację
- Opisz zmiany w Pull Request
- Testuj na Python 3.8, 3.9, 3.10, 3.11, 3.12

### Obszary do rozwoju

- 📖 Dodatkowe dziedziny prawa
- 🌍 Wsparcie dla innych krajów (prawo niemieckie, czeskie, etc.)
- 🎨 GUI aplikacja (PyQt/Tkinter)
- 🔍 Lepsza analiza NLP przepisów
- 📊 Wizualizacja wyników

---

## 📄 License

Ten projekt jest licencjonowany na licencji **MIT License** - zobacz plik LICENSE po szczegóły.

**MIT License** oznacza że możesz:
- ✅ Używać komercyjnie
- ✅ Modyfikować kod
- ✅ Dystrybuować
- ✅ Używać prywatnie

**Z zastrzeżeniem:**
- ⚠️ Dołączenia informacji o licencji i prawach autorskich
- ⚠️ Brak gwarancji

***

## 👥 Autorzy

**Sebastian** - *Initial work* - [GitHub Profile](https://github.com/sebastian-c87)

**Mecenas Kamila Sadłowicz** - *Konsultacje prawne* - Warszawa

Zobacz też listę contributors którzy uczestniczyli w projekcie.

***

### 👨‍💻 Kontakt z Autorem

![Profile](https://img.shields.io/badge/👨‍🎓%20Computer%20Science%20Student-IT%20Enthusiast-blue?style=for-the-badge)  
![Specialization](https://img.shields.io/badge/🛡️%20Specialist%20in-CyberSecurity%20|%20Python%20|%20AI-green?style=for-the-badge)

![Location](https://img.shields.io/badge/📍%20Location-Warszawa,%20Polska-red?style=for-the-badge)  
![Phone](https://img.shields.io/badge/📞_Whatsapp_&_Phone-%2B48%20539%20298%20079-orange?style=for-the-badge&logo=whatsapp)

[![GitHub](https://img.shields.io/badge/GitHub-sebastian--c87-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sebastian-c87)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sebastian%20Ciborowski-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/)  
[![Gmail](https://img.shields.io/badge/Gmail-Kontakt_bezpośredni-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ciborowski.s@gmail.com) 
### 💼 Konsultacje prawne

**Mecenas Kamila Sadłowicz**  
📍 Warszawa, Polska  
⚖️ Specjalizacja: Wszystkie dziedziny prawa polskiego

✓ Doświadczony adwokat z indywidualnym podejściem  
✓ Maksymalne zaangażowanie w każdą sprawę  
✓ Profesjonalna reprezentacja w sądach i urzędach  
✓ Skuteczna ochrona interesów klientów

*[KONTAKT - szczegóły zostaną dodane]*

***

## ⚠️ Zastrzeżenia prawne

**WAŻNE:** Legal Case Finder to narzędzie **informacyjne i edukacyjne**. 

**NIE STANOWI:**
- Porady prawnej
- Zastępstwa profesjonalnego prawnika
- Gwarancji skuteczności w postępowaniu
- Oficjalnej interpretacji przepisów

**ZAWSZE:**
- Konsultuj ważne sprawy z adwokatem/radcą prawnym
- Weryfikuj aktualność przepisów
- Sprawdzaj szczegóły w oryginalnych źródłach
- Zachowuj ostrożność przy podejmowaniu decyzji prawnych

Twórcy aplikacji nie ponoszą odpowiedzialności za decyzje podjęte na podstawie analiz z aplikacji.

***


**Zbudowane z ❤️ dla polskiego prawa używając Python i GPT-5-nano**

⭐ **Jeśli ten projekt Ci pomógł, zostaw gwiazdkę!** ⭐

***
