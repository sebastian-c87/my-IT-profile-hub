
---

<div align="center">

# 🎮 RPG Story Generator

### **Interaktywna gra fabularna zasilana przez GPT-5-nano**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge) ![open](https://img.shields.io/badge/OpenAI-GPT--5--mini-412991?style=for-the-badge) ![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge) ![colab](https://img.shields.io/badge/Google-Colab-F9AB00?style=for-the-badge)

**Twoje przygody, Twoje decyzje, nieskończone możliwości**

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
- [Gatunki](#-gatunki)
- [Poziomy trudności](#-poziomy-trudności)
- [Architektura](#-architektura)
- [Przykład rozgrywki](#-przykład-rozgrywki)
- [API Reference](#-api-reference)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Kontakt](#-autorzy)

***

## 🎯 O projekcie

**RPG Story Generator** to zaawansowana, interaktywna gra fabularna, w której **sztuczna inteligencja GPT-5-nano pełni rolę Mistrza Gry**. System tworzy dynamiczne, niepowtarzalne historie, które rozwijają się w oparciu o decyzje gracza. Każda rozgrywka jest unikalna - świat reaguje na Twoje wybory, postacie pamiętają Twoje działania, a konsekwencje są realne.

### 🌟 Dlaczego RPG Story Generator?

- **🤖 AI Game Master** - GPT-5-nano jako profesjonalny Mistrz Gry prowadzący narrację
- **🎲 Nieograniczona kreatywność** - każda rozgrywka jest inna, brak skryptowanych ścieżek
- **📖 Żywa narracja** - szczegółowe opisy wykorzystujące wszystkie zmysły
- **🔀 Dynamiczny świat** - świat reaguje na Twoje decyzje w czasie rzeczywistym
- **💬 Inteligentne NPC** - postacie z własnymi celami, osobowościami i dialogami
- **💾 Pełny system zapisu** - kontynuuj przygodę w dowolnym momencie
- **🎭 8 gatunków** - od Fantasy po Cyberpunk
- **⚔️ 4 poziomy trudności** - od przyjaznego świata po hardcore survival
- **📱 Dwa tryby** - aplikacja desktopowa i Google Colab

***

## ✨ Funkcje

### 🎮 System rozgrywki

**Mistrz Gry prowadzi narrację:**
- **Szczegółowe opisy scen** - lokacje, atmosfera, dźwięki, zapachy
- **Żywe postacie NPC** - z dialogami, emocjami i motywacjami
- **Wydarzenia i konflikty** - dynamiczne wyzwania dostosowane do sytuacji
- **Opcje działania** - zawsze 3-4 propozycje + możliwość własnej akcji
- **Konsekwencje decyzji** - każdy wybór ma znaczenie

### 🎭 Gatunki i światy

8 unikalnych gatunków do wyboru:
- **Fantasy** - magia, smoki, epickie przygody
- **Sci-Fi** - kosmos, technologia, przyszłość
- **Horror** - mroczne tajemnice, supernatural, survival
- **Postapokalipsa** - zniszczony świat, walka o przetrwanie
- **Cyberpunk** - neon, hakerzy, korporacje
- **Steampunk** - parowa technologia, wiktoriańska era
- **Noir** - detektywistyka, mroczne ulice, tajemnice
- **Superhero** - moce, misje ratunkowe, złoczyńcy

### ⚔️ Poziomy trudności

- **Łatwy** - przyjazny świat, szczęście w krytycznych momentach
- **Średni** - zbalansowane wyzwania wymagające przemyślenia
- **Trudny** - niebezpieczny świat, poważne konsekwencje
- **Hardcore** - bezlitosny survival, każda decyzja może być ostatnia

### 💾 Zarządzanie sesją

- **Automatyczny zapis** - historia zapisywana na bieżąco
- **Wczytywanie gier** - kontynuuj przygodę od ostatniego punktu
- **Eksport historii** - zapisz kompletną narrację do TXT/JSON
- **Statystyki sesji** - śledź postępy (tury, słowa, czas gry)
- **Historia akcji** - pełna dokumentacja Twoich decyzji

---

## 🔧 Wymagania

### Wymagania systemowe

- **Python**: 3.8 lub nowszy
- **System operacyjny**: Windows, macOS, Linux
- **RAM**: Minimum 4GB (zalecane 8GB)
- **Połączenie internetowe**: Wymagane do komunikacji z OpenAI API

### Wymagane pakiety

- **openai** >= 1.0.0 - Oficjalny klient OpenAI Python
- **python-dotenv** >= 1.0.0 - Zarządzanie zmiennymi środowiskowymi

### Klucz API

Wymagany klucz API OpenAI z dostępem do GPT-5-nano. Uzyskaj go na: https://platform.openai.com/api-keys

***

## 📦 Instalacja

### Metoda 1: Klonowanie repozytorium

    git clone https://github.com/yourusername/rpg-story-generator.git
    cd rpg-story-generator

### Metoda 2: Pobieranie jako ZIP

Pobierz i rozpakuj archiwum ZIP z GitHub, następnie przejdź do katalogu projektu.

### Instalacja zależności

    pip install -r requirements.txt

Lub instalacja ręczna:

    pip install openai>=1.0.0 python-dotenv>=1.0.0

***

## ⚙️ Konfiguracja

### 1. Utwórz plik .env

W głównym katalogu projektu utwórz plik `.env` i dodaj swój klucz API:

    OPENAI_API_KEY=sk-your-api-key-here

### 2. Dostosuj konfigurację (opcjonalne)

Edytuj plik `src/config.py` aby dostosować parametry:

**Model Configuration:**
- **model_name**: Model OpenAI (domyślnie: gpt-5-nano)
- **reasoning_effort**: Poziom rozumowania (domyślnie: high)
- **max_output_tokens**: Maksymalna długość odpowiedzi (domyślnie: 3000)
- **min_story_length**: Minimalna długość opisu (domyślnie: 300 słów)

**Story Configuration:**
- **max_story_context**: Maksymalna długość kontekstu (domyślnie: 4000 znaków)
- **auto_save**: Automatyczny zapis (domyślnie: True)

### 3. Weryfikacja instalacji

    cd src
    python main.py

Jeśli wszystko działa poprawnie, zobaczysz menu główne gry.

***

## 🚀 Użycie

### Uruchomienie aplikacji lokalnej

    cd src
    python main.py

### Podstawowy przepływ gry

**Krok 1: Menu główne**
Wybierz "1. Nowa gra" aby rozpocząć przygodę

**Krok 2: Wybór gatunku**
Wybierz spośród 8 gatunków (Fantasy, Sci-Fi, Horror, etc.)

**Krok 3: Poziom trudności**
Wybierz trudność (Łatwy, Średni, Trudny, Hardcore)

**Krok 4: Opis bohatera**
Opisz początkową sytuację swojego bohatera:
- "Jestem rycerzem poszukującym zaginionego artefaktu"
- "Budzę się w kapsuле ratunkowej na nieznanej planecie"
- "Jestem detektywem prowadzącym sprawę zagadkowego morderstwa"

**Krok 5: Rozgrywka**
- Mistrz Gry opisze świat i przedstawi sytuację
- Otrzymasz 3-4 opcje działania
- Wybierz numer opcji (np. "1") LUB opisz własną akcję
- Historia rozwija się na podstawie Twoich decyzji!

**Krok 6: Podczas gry**
- Wpisz numer opcji aby wybrać zaproponowaną akcję
- Opisz własne działanie dla unikalnego podejścia
- Używaj komend: 'menu', 'statystyki', 'exit'
- Zapisuj grę regularnie!

### Menu główne

**1. 🆕 Nowa gra**
Rozpocznij nową przygodę - wybierz gatunek, trudność i opisz bohatera

**2. 💾 Wczytaj grę**
Kontynuuj zapisaną przygodę od ostatniego punktu

**3. 📋 Zapisane gry**
Przeglądaj listę wszystkich zapisanych sesji z szczegółami

**4. ❓ Pomoc**
Instrukcje, wskazówki i informacje o gatunkach

**5. 🚪 Zakończ**
Wyjście z aplikacji (z opcją zapisu aktywnej gry)

### Menu podczas gry

**1. ↩️ Powrót do gry**
Kontynuuj rozgrywkę

**2. 💾 Zapisz grę**
Zapisz obecną sesję do pliku JSON

**3. 📊 Statystyki sesji**
Zobacz statystyki: liczba tur, słowa, czas rozpoczęcia

**4. 📖 Pełna historia**
Wyświetl kompletną narrację z wszystkimi turami + opcja zapisu do TXT

**5. 🚪 Zakończ grę**
Wyjdź z gry (z opcją zapisu)

### Specjalne komendy

Podczas rozgrywki możesz użyć:

- **'menu'** - otwórz menu gry
- **'statystyki'** - wyświetl statystyki sesji
- **'exit'** - zakończ grę i wyjdź (z opcją zapisu)

---

## 🔬 Google Colab

### Uruchomienie w Colab

**Krok 1:** Otwórz nowy notebook w Google Colab

**Krok 2:** Dodaj klucz API jako Secret
- Kliknij ikonę klucza 🔑 w lewym pasku
- Name: `OPENAI_API_KEY`
- Value: Twój klucz API OpenAI
- Włącz "Notebook access"

**Krok 3:** Wklej cały kod z pliku `colab_version.py`

**Krok 4:** Uruchom komórkę i wywołaj:

    setup()

Gra uruchomi się automatycznie w trybie interaktywnym!

### Funkcje Colab

**setup()** - Główna funkcja uruchamiająca grę

### Uproszczone menu Colab

1. 🆕 Nowa gra
2. ❓ Pomoc
3. 🚪 Zakończ

### Zapisywanie w Colab

- Używaj komendy 'save' podczas gry
- Pliki JSON są dostępne w sekcji Files 📁 w lewym pasku
- Pobierz klikając prawym przyciskiem → Download

### Specjalne komendy w Colab

- **'save'** - zapisz grę do JSON
- **'exit'** - zakończ rozgrywkę
- Numery opcji lub opisy akcji działają tak samo

***

## 🎭 Gatunki

### 1. ⚔️ Fantasy

**Opis:** Magiczny świat pełen legend, smoki, elfy, czarodziejstwo

**Typowe elementy:**
- Epickie questy i poszukiwanie artefaktów
- Magia i zaklęcia
- Różnorodne rasy (elfy, krasnoludy, orki)
- Starożytne ruiny i tajemnice
- Smoczy skarby i pradawne zło

**Przykładowy scenariusz:** "Jestem młodym magiem odkrywającym zapomnianą księgę zaklęć"

### 2. 🚀 Sci-Fi

**Opis:** Futurystyczna przyszłość, kosmos, zaawansowana technologia

**Typowe elementy:**
- Podróże kosmiczne i obce cywilizacje
- AI, roboty, cyborgi
- Stacje kosmiczne i kolonie
- Technologiczne gadżety
- Dystopie i utopie przyszłości

**Przykładowy scenariusz:** "Budzę się z kriostazy na pokładzie statku kolonizacyjnego"

### 3. 👻 Horror

**Opis:** Mroczne tajemnice, supernatural, atmosfera strachu

**Typowe elementy:**
- Nawiedzone miejsca
- Duchy, demony, potwory
- Psychologiczny terror
- Survival horror
- Mroczne sekrety i przekleństwa

**Przykładowy scenariusz:** "Jestem badaczem paranormalnym w nawiedzonym dworze"

### 4. ☢️ Postapokalipsa

**Opis:** Zniszczony świat po katastrofie, walka o przetrwanie

**Typowe elementy:**
- Ruiny cywilizacji
- Zmutowane stworzenia
- Ograniczone zasoby
- Bandy i frakcje
- Trudne moralne decyzje

**Przykładowy scenariusz:** "Przetrwałem nuklearną wojnę i szukam bezpiecznego schronienia"

### 5. 🌃 Cyberpunk

**Opis:** Dystopiczna przyszłość, neon, megakorporacje, hakerzy

**Typowe elementy:**
- Neonowe miasta
- Cyberprzestrzeń i hacking
- Wszczepy i augmentacje
- Korporacyjne spiski
- Streetowa walka o wolność

**Przykładowy scenariusz:** "Jestem netrunnerem łamiącym zabezpieczenia megakorporacji"

### 6. ⚙️ Steampunk

**Opis:** Alternatywna wiktoriańska era, parowa technologia

**Typowe elementy:**
- Maszyny parowe i zegarkowe mechanizmy
- Sterowce i mechaniczne pojazdy
- Wiktoriańska estetyka
- Szaleni wynalazcy
- Rewolucje przemysłowe

**Przykładowy scenariusz:** "Jestem wynalazcą testującym nową maszynę parową"

### 7. 🕵️ Noir

**Opis:** Mroczna detektywistyka, lata 40-50, tajemnice

**Typowe elementy:**
- Detektywistyczne śledztwa
- Femme fatales i gangsterzy
- Mroczne ulice i zakamarki miasta
- Korupcja i spiski
- Moralna ambiwalencja

**Przykładowy scenariusz:** "Jestem prywatnym detektywem prowadzącym sprawę zaginionej dziedziczki"

### 8. 🦸 Superhero

**Opis:** Superbohaterowie, moce, misje ratunkowe

**Typowe elementy:**
- Nadludzkie moce
- Walka ze złoczyńcami
- Ochrona niewinnych
- Sekretna tożsamość
- Epickie starcia dobra ze złem

**Przykładowy scenariusz:** "Odkryłem nadludzkie zdolności i muszę powstrzymać zagrożenie"

***

## ⚔️ Poziomy trudności

### 🟢 Łatwy

**Charakterystyka:**
- Świat jest przyjazny i wybaczający
- Gracze mają szczęście w krytycznych momentach
- Łatwe wyzwania do pokonania
- Wsparcie od NPC
- Dobre zakończenia bardziej prawdopodobne

**Dla kogo:** Początkujący, gracze chcący cieszyć się historią bez frustracji

### 🟡 Średni

**Charakterystyka:**
- Zbalansowany świat z uzasadnionymi wyzwaniami
- Decyzje mają konsekwencje, ale nie katastrofalne
- Wymaga przemyślenia strategii
- Realistyczne reakcje świata
- Mix sukcesów i porażek

**Dla kogo:** Standardowa rozgrywka, gracze szukający równowagi

### 🟠 Trudny

**Charakterystyka:**
- Niebezpieczny świat z poważnymi wyzwaniami
- Złe decyzje prowadzą do trudnych sytuacji
- Wymaga strategicznego myślenia
- Ograniczone zasoby i pomoc
- Ciemniejsze zwroty akcji

**Dla kogo:** Doświadczeni gracze szukający wyzwania

### 🔴 Hardcore

**Charakterystyka:**
- Bezlitosny świat survival
- Każda decyzja może być ostatnia
- Śmierć bohatera jest realna
- Minimalne wsparcie, maksymalne zagrożenie
- Ciemna, brutalna narracja

**Dla kogo:** Hardcore gracze, miłośnicy ekstremalnych wyzwań

***

## 🏗️ Architektura

### Struktura projektu

    rpg-story-generator/
    ├── src/
    │   ├── __init__.py          # Inicjalizacja pakietu
    │   ├── main.py              # Główna aplikacja desktopowa
    │   ├── openai_client.py     # Klient GPT-5-nano (Game Master)
    │   ├── story_manager.py     # Zarządzanie historią i zapisami
    │   └── config.py            # Konfiguracja aplikacji
    ├── saves/                   # Folder z zapisanymi sesjami (auto-generowany)
    ├── colab_version.py         # Wersja dla Google Colab
    ├── requirements.txt         # Zależności Python
    ├── .env.example            # Przykład konfiguracji
    ├── README.md               # Dokumentacja
    └── LICENSE                 # Licencja MIT

### Komponenty systemu

**OpenAI Client (RPGGameMaster)**
- Komunikacja z GPT-5-nano przez Responses API
- Generowanie wprowadzenia do gry
- Kontynuacja historii na podstawie akcji gracza
- Inteligentne prompty dla Mistrza Gry
- Strukturalna narracja z opcjami działania

**Story Manager**
- Zarządzanie sesją gry
- Historia tur i akcji gracza
- System zapisu/wczytywania (JSON)
- Kontekst dla AI (ostatnie tury)
- Statystyki sesji (tury, słowa, czas)
- Eksport do TXT

**Config Manager**
- Zarządzanie konfiguracją aplikacji
- Zmienne środowiskowe (.env)
- Parametry modelu AI
- Ustawienia gatunków i trudności

**Main Application**
- Interface użytkownika w konsoli
- Zarządzanie przepływem gry
- Menu i nawigacja
- Parsowanie akcji gracza (numery vs opisy)
- Specjalne komendy (menu, statystyki, exit)

### Przepływ danych

1. **Start gry** → Gracz wybiera gatunek, trudność, opisuje bohatera
2. **AI generuje intro** → GPT-5-nano tworzy początkową scenę z opcjami
3. **Gracz podejmuje akcję** → Wybiera numer lub opisuje działanie
4. **AI kontynuuje** → Reaguje na akcję, rozwija fabułę, daje nowe opcje
5. **Loop** → Kroki 3-4 powtarzają się tworząc dynamiczną historię
6. **Zapis** → Sesja zapisywana automatycznie lub manualnie

---

## 🎬 Przykład rozgrywki

### Rozpoczęcie gry

**Gracz wybiera:**
- Gatunek: Fantasy
- Trudność: Średni
- Scenariusz: "Jestem młodym magiem odkrywającym pradawną księgę zaklęć"

### Mistrz Gry odpowiada:

*Długi, szczegółowy opis wprowadzający do świata...*

**Wprowadzenie zawiera:**
- Opis biblioteki i atmosfery
- Szczegóły o znalezionej księdze
- Pojawienie się tajemniczej postaci (NPC)
- Pierwsze wydarzenie (magiczne zagrożenie)

**Opcje działania:**
1. Otworzyć księgę i spróbować odczytać zaklęcie
2. Zapytać tajemniczą postać kim jest i czego chce
3. Schować księgę i uciec z biblioteki
4. Możesz też opisać własną akcję!

### Gracz wybiera:

    ➤ Twoja akcja: 2

### Mistrz Gry kontynuuje:

*Szczegółowy opis reakcji postaci...*
*Rozwój fabuły i nowe wydarzenia...*
*Kolejny zestaw opcji do wyboru...*

### I tak dalej...

Każda tura buduje historię, świat reaguje na decyzje, postacie pamiętają akcje gracza, konsekwencje są realne!

***

## 📚 API Reference

### RPGGameMaster

**Inicjalizacja:**

    from config import config
    from openai_client import RPGGameMaster
    
    game_master = RPGGameMaster(config)

**Główna metoda - generate_story_intro:**

    generate_story_intro(genre: str, initial_scenario: str, difficulty: str) -> Dict[str, Any]

**Parametry:**
- **genre** (str): Gatunek gry (np. "Fantasy")
- **initial_scenario** (str): Początkowa sytuacja bohatera
- **difficulty** (str): Poziom trudności

**Zwraca:**

    {
        "story": "Szczegółowe wprowadzenie do gry...",
        "genre": "Fantasy",
        "difficulty": "Średni",
        "success": True,
        "timestamp": "2025-10-09T00:00:00.000000"
    }

**Metoda - continue_story:**

    continue_story(genre: str, difficulty: str, story_context: str, player_action: str) -> Dict[str, Any]

**Parametry:**
- **genre** (str): Gatunek gry
- **difficulty** (str): Poziom trudności
- **story_context** (str): Kontekst dotychczasowej historii
- **player_action** (str): Akcja wykonana przez gracza

**Zwraca:**

    {
        "story": "Kontynuacja historii z reakcją na akcję...",
        "player_action": "Wybieram opcję 1",
        "success": True,
        "timestamp": "2025-10-09T00:05:00.000000"
    }

### StoryManager

**Inicjalizacja:**

    from story_manager import StoryManager
    
    story_manager = StoryManager()

**Metoda - start_new_session:**

    start_new_session(genre: str, difficulty: str, initial_scenario: str, intro_story: str)

Rozpoczyna nową sesję gry i dodaje wprowadzenie jako turę 0.

**Metoda - add_turn:**

    add_turn(turn_number: int, player_action: str, story_response: str)

Dodaje nową turę do historii sesji.

**Metoda - get_story_context:**

    get_story_context(max_turns: int = 5) -> str

Zwraca sformatowany kontekst ostatnich N tur dla AI.

**Metoda - save_session:**

    save_session(filename: Optional[str] = None) -> str

Zapisuje sesję do pliku JSON. Zwraca ścieżkę do pliku.

**Metoda - get_session_stats:**

    get_session_stats() -> Dict[str, Any]

Zwraca statystyki obecnej sesji:

    {
        "session_id": "20251009_000000",
        "genre": "Fantasy",
        "difficulty": "Średni",
        "total_turns": 15,
        "total_words": 4523,
        "start_time": "2025-10-09T00:00:00"
    }

---

## 🐛 Rozwiązywanie problemów

### Problem: "Invalid API key"

**Rozwiązanie:** Sprawdź czy klucz API jest poprawny i aktywny w pliku .env

    OPENAI_API_KEY=sk-twój-prawdziwy-klucz

### Problem: "Rate limit exceeded"

**Rozwiązanie:** Poczekaj chwilę przed kolejnym zapytaniem. GPT-5-nano ma limity requestów. Sprawdź limity w swoim koncie OpenAI.

### Problem: "Krótkie lub niekompletne odpowiedzi"

**Przyczyna:** max_output_tokens ustawione za nisko

**Rozwiązanie:** Zwiększ max_output_tokens w config.py (zalecane: 3000)

    max_output_tokens: int = 3000

### Problem: "Pusta odpowiedź od Mistrza Gry"

**Przyczyna:** Błąd w komunikacji z API lub błędny format odpowiedzi

**Rozwiązanie:** Sprawdź logi, zweryfikuj klucz API, upewnij się że masz dostęp do GPT-5-nano

### Problem: "Błąd zapisu sesji"

**Przyczyna:** Brak uprawnień do zapisu lub zapełniony dysk

**Rozwiązanie:** Upewnij się że folder saves/ istnieje i masz uprawnienia do zapisu

### Problem: "Historia nie pamięta wcześniejszych wydarzeń"

**Przyczyna:** max_story_context za niski

**Rozwiązanie:** Zwiększ max_story_context w config.py (zalecane: 4000)

    max_story_context: int = 4000

***

## 🗺️ Roadmap

### Wersja 1.1 (Q1 2025)

- ✅ Multi-player support - gra dla wielu graczy jednocześnie
- ✅ Persystentne światy - zapisywanie stanu całego świata
- ✅ System inwentarza - przedmioty, zasoby, ekwipunek
- ✅ System umiejętności - rozwój postaci, poziomy, exp

### Wersja 1.2 (Q2 2025)

- 🔄 Graficzny interfejs (GUI) - PyQt/Tkinter
- 🔄 Generowanie obrazów AI - wizualizacje scen (DALL-E)
- 🔄 Efekty dźwiękowe - muzyka i ambientne dźwięki
- 🔄 Achievement system - osiągnięcia i nagrody

### Wersja 2.0 (Q3 2025)

- 🔮 Multiplayer online - serwer gry dla wielu graczy
- 🔮 Web interface - przeglądarkowa wersja gry
- 🔮 Mobile app (iOS/Android) - gra na telefony
- 🔮 Voice interaction - sterowanie głosem
- 🔮 Custom world creation - tworzenie własnych światów

---

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
- Testuj na Python 3.8+

### Obszary do rozwoju

- 🎨 Nowe gatunki i scenariusze
- 🌍 Wsparcie dla innych języków
- 🎮 Mechaniki gry (combat, skill checks)
- 📊 Statystyki i achievements
- 🖼️ Integracje z generatorami obrazów

***

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

---

<div align="center">

**Zbudowane z ❤️ dla miłośników gier RPG używając Python i GPT-5-nano**

⭐ **Jeśli ten projekt Ci się podoba, zostaw gwiazdkę!** ⭐

</div>

---