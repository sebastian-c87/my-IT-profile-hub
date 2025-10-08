
---

<div align="center">

# 🖼️ Image Recognition AI

### **Zaawansowana analiza obrazów zasilana przez GPT-5**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge)![open](https://img.shields.io/badge/OpenAI-GPT--5--mini-412991?style=for-the-badge)![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)![colab](https://img.shields.io/badge/Google-Colab-F9AB00?style=for-the-badge)

**Profesjonalne narzędzie do analizy obrazów wykorzystujące najnowsze możliwości GPT-5-mini**

[Funkcje](#-funkcje) -  [Instalacja](#-instalacja) -  [Użycie](#-użycie) -  [API Reference](#-api-reference) -  [Kontakt](#-kontakt-z-autorem)

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
- [Przykłady](#-przykłady)
- [API Reference](#-api-reference)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Kontakt](#-kontakt-z-autorem)

---

## 🎯 O projekcie

**Image Recognition AI** to zaawansowane narzędzie do analizy obrazów wykorzystujące moc **OpenAI GPT-5-mini** z natywną obsługą multimodal. Aplikacja oferuje szeroki zakres funkcji rozpoznawania wizualnego, od podstawowej analizy obiektów po zaawansowaną interpretację artystyczną.

### 🌟 Dlaczego Image Recognition AI?

- **🚀 Najnowsza technologia** - wykorzystuje GPT-5-mini z Responses API
- **🎨 Wszechstronność** - od prostego OCR po głęboką analizę artystyczną
- **💻 Dwa tryby** - aplikacja desktopowa i wersja Google Colab
- **🌐 Elastyczność** - obsługa URL i plików lokalnych
- **📊 Historia analiz** - śledzenie i eksport wyników
- **🔒 Bezpieczeństwo** - właściwe zarządzanie kluczami API

---

## ✨ Funkcje

### 🔍 Analiza kompleksowa
Szczegółowa analiza obrazu obejmująca wszystkie widoczne elementy, scenę, obiekty, osoby, kolory, oświetlenie, teksty i nastrój.

### 🏷️ Rozpoznawanie obiektów
Precyzyjna identyfikacja wszystkich obiektów z opisem położenia, rozmiaru, stanu, koloru i materiału.

### 🎬 Analiza sceny
Kontekstualna interpretacja miejsca, sytuacji, wydarzeń i czasu.

### 📝 OCR (Optical Character Recognition)
Dokładne wyodrębnianie i przepisywanie wszystkich tekstów z zachowaniem formatowania.

### 🎨 Analiza artystyczna
Profesjonalna ocena stylu fotograficznego, techniki, kompozycji, światła i wartości estetycznych.

### ⚖️ Porównywanie obrazów
Szczegółowe porównanie dwóch obrazów z identyfikacją podobieństw i różnic.

### 💾 Historia i eksport
Śledzenie wszystkich analiz z możliwością eksportu do formatu JSON.

***

## 🔧 Wymagania

### Wymagania systemowe

- **Python**: 3.8 lub nowszy
- **System operacyjny**: Windows, macOS, Linux
- **RAM**: Minimum 4GB (zalecane 8GB)
- **Połączenie internetowe**: Wymagane do komunikacji z OpenAI API

### Wymagane pakiety

- **openai** >= 1.0.0 - Oficjalny klient OpenAI Python
- **pillow** >= 10.0.0 - Przetwarzanie obrazów
- **requests** >= 2.31.0 - Obsługa HTTP
- **python-dotenv** >= 1.0.0 - Zarządzanie zmiennymi środowiskowymi

### Klucz API

Wymagany klucz API OpenAI z dostępem do modeli GPT-5. Uzyskaj go na: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

***

## 📦 Instalacja

### Metoda 1: Klonowanie repozytorium

    git clone https://github.com/yourusername/image-recognition-ai.git
    cd image-recognition-ai

### Metoda 2: Pobieranie jako ZIP

Pobierz i rozpakuj archiwum ZIP z GitHub, następnie przejdź do katalogu projektu.

### Instalacja zależności

    pip install -r requirements.txt

Lub instalacja ręczna:

    pip install openai>=1.0.0 pillow>=10.0.0 requests>=2.31.0 python-dotenv>=1.0.0

***

## ⚙️ Konfiguracja

### 1. Utwórz plik .env

W głównym katalogu projektu utwórz plik `.env` i dodaj swój klucz API:

    OPENAI_API_KEY=sk-your-api-key-here

### 2. Dostosuj konfigurację (opcjonalne)

Edytuj plik `src/config.py` aby dostosować parametry:

- **max_image_size** - maksymalny rozmiar obrazu (domyślnie 10MB)
- **image_quality** - jakość kompresji JPEG (domyślnie 75%)
- **max_width/max_height** - maksymalne wymiary obrazu (domyślnie 1024px)

### 3. Weryfikacja instalacji

    python src/main.py

Jeśli wszystko działa poprawnie, zobaczysz menu główne aplikacji.

***

## 🚀 Użycie

### Uruchomienie aplikacji lokalnej

    cd src
    python main.py

### Podstawowy przepływ pracy

**Krok 1:** Wybierz opcję z menu głównego (1-7)

**Krok 2:** Podaj źródło obrazu (plik lokalny lub URL)

**Krok 3:** Wybierz typ analizy

**Krok 4:** Poczekaj na wyniki analizy

**Krok 5:** Przeglądaj wyniki i zapisz w historii

### Obsługiwane formaty obrazów

- **JPEG / JPG** - Rekomendowane
- **PNG** - Obsługiwane z konwersją do RGB
- **WEBP** - Obsługiwane
- **GIF** - Obsługiwane (tylko pierwszy frame)
- **BMP** - Obsługiwane

### Źródła obrazów

**Pliki lokalne** - Pełna ścieżka do pliku na dysku

**URL** - Bezpośredni link do obrazu (http:// lub https://)

**Przeciąganie i upuszczanie** - W trybie Colab

***

## 🔬 Google Colab

### Uruchomienie w Colab

**1. Otwórz nowy notebook w Google Colab**

**2. Dodaj klucz API jako Secret:**
- Kliknij ikonę klucza 🔑 w lewym pasku
- Name: `OPENAI_API_KEY`
- Value: Twój klucz API OpenAI
- Włącz "Notebook access"

**3. Wklej i uruchom kod z pliku `colab_version.py`**

**4. Wywołaj funkcję setup():**

    setup()

### Funkcje Colab

- **setup()** - Główna funkcja uruchamiająca aplikację
- **analyze(image_input, analysis_type)** - Szybka analiza obrazu
- **history()** - Wyświetl historię analiz
- **export()** - Eksportuj wyniki do JSON

### Przykład użycia w Colab

    # Szybka analiza
    result = analyze("https://example.com/image.jpg", "comprehensive")
    
    # Analiza obiektów
    result = analyze("uploaded_image.jpg", "objects")
    
    # Historia
    history()
    
    # Eksport
    export()

***

## 🏗️ Architektura

### Struktura projektu

    img-recognition/
    ├── src/
    │   ├── main.py              # Główna aplikacja
    │   ├── openai_client.py     # Klient GPT-5-mini
    │   ├── image_processor.py   # Przetwarzanie obrazów
    │   ├── config.py            # Konfiguracja
    │   └── __init__.py
    ├── colab_version.py         # Wersja dla Google Colab
    ├── requirements.txt         # Zależności Python
    ├── .env.example            # Przykład konfiguracji
    ├── README.md               # Dokumentacja
    └── LICENSE                 # Licencja MIT

### Komponenty systemu

**OpenAI Client** - Komunikacja z GPT-5-mini przez Responses API z natywnym multimodal support

**Image Processor** - Walidacja, preprocessing, encoding obrazów do base64, optymalizacja rozmiaru

**Config Manager** - Zarządzanie konfiguracją, zmienne środowiskowe, parametry aplikacji

**Main Application** - Interface użytkownika, obsługa menu, historia analiz, eksport wyników

***

## 💡 Przykłady

### Przykład 1: Analiza zdjęcia krajobrazu

**Input:** Zdjęcie górskiego krajobrazu o wschodzie słońca

**Output:** Szczegółowy opis sceny, identyfikacja elementów naturalnych (góry, niebo, chmury), analiza oświetlenia i kolorów, interpretacja nastroju, ocena jakości technicznej fotografii

### Przykład 2: OCR dokumentu

**Input:** Skan faktury lub paragonu

**Output:** Precyzyjne przepisanie wszystkich tekstów, zachowanie struktury i formatowania, identyfikacja dat, kwot i pozycji

### Przykład 3: Analiza produktu

**Input:** Zdjęcie produktu e-commerce

**Output:** Identyfikacja wszystkich elementów produktu, opis materiałów i kolorów, stan i kondycja przedmiotu, kontekst i tło

### Przykład 4: Porównanie wersji

**Input:** Dwa zdjęcia tego samego miejsca w różnych porach roku

**Output:** Szczegółowe porównanie, identyfikacja zmian, analiza różnic w oświetleniu i kolorach, wnioski

***

## 📚 API Reference

### ColabImageRecognitionAI

**Inicjalizacja:**

    client = ColabImageRecognitionAI(api_key="your-api-key")

**Metody:**

**analyze_image(image_input, analysis_type, language)**
- **image_input** (str): Ścieżka do pliku lub URL
- **analysis_type** (str): "comprehensive", "objects", "scene", "text", "artistic"
- **language** (str): "polish" lub "english"
- **Return**: Dict z wynikami analizy

**encode_image_base64(image_input)**
- **image_input** (str): Ścieżka do pliku lub URL
- **Return**: String base64 lub None

### ImageRecognitionAI

**Główna klasa dla wersji lokalnej z dodatkowymi metodami:**

**compare_images(image_path1, image_path2, language)**
- **image_path1** (str): Ścieżka do pierwszego obrazu
- **image_path2** (str): Ścieżka do drugiego obrazu
- **language** (str): Język analizy
- **Return**: Dict z wynikami porównania

**extract_text_from_image(image_path, language)**
- **image_path** (str): Ścieżka do obrazu
- **language** (str): Język analizy
- **Return**: Dict z wyodrębnionym tekstem

---

## 🐛 Rozwiązywanie problemów

### Problem: "Invalid API key"

**Rozwiązanie:** Sprawdź czy klucz API jest poprawny i aktywny w pliku .env lub Colab Secrets

### Problem: "Rate limit exceeded"

**Rozwiązanie:** Poczekaj chwilę przed kolejnym zapytaniem lub zwiększ limity w swoim koncie OpenAI

### Problem: "Image too large"

**Rozwiązanie:** Zmniejsz rozmiar obrazu lub dostosuj parametry w config.py (max_image_size, max_width, max_height)

### Problem: "Module not found"

**Rozwiązanie:** Zainstaluj ponownie wymagane pakiety: pip install -r requirements.txt

### Problem: "Connection timeout"

**Rozwiązanie:** Sprawdź połączenie internetowe lub zwiększ timeout w config.py

***

## 🗺️ Roadmap

### Wersja 1.1 (Q1 2025)

- ✅ Batch processing wielu obrazów
- ✅ Eksport do PDF z wizualizacjami
- ✅ REST API endpoint
- ✅ Dashboard webowy

### Wersja 1.2 (Q2 2025)

- 🔄 Obsługa video frames
- 🔄 Real-time analysis z kamery
- 🔄 Integracja z bazami danych
- 🔄 Advanced caching

### Wersja 2.0 (Q3 2025)

- 🔮 Fine-tuning własnych modeli
- 🔮 Custom detection pipelines
- 🔮 Multi-language UI
- 🔮 Cloud deployment

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

- Zachowaj spójność stylu kodu
- Dodaj testy dla nowych funkcji
- Zaktualizuj dokumentację
- Opisz zmiany w Pull Request

***

## 📄 License

Ten projekt jest licencjonowany na licencji **MIT License** - zobacz plik [LICENSE](LICENSE) po szczegóły.

**MIT License** oznacza że możesz:
- ✅ Używać komercyjnie
- ✅ Modyfikować kod
- ✅ Dystrybuować
- ✅ Używać prywatnie

**Z zastrzeżeniem:**
- ⚠️ Dołączenia informacji o licencji i prawach autorskich
- ⚠️ Brak gwarancji

***
### 👨‍💻 Kontakt z Autorem

![Profile](https://img.shields.io/badge/👨‍🎓%20Computer%20Science%20Student-IT%20Enthusiast-blue?style=for-the-badge)
![Specialization](https://img.shields.io/badge/🛡️%20Specialist%20in-CyberSecurity%20|%20Python%20|%20AI-green?style=for-the-badge)

![Location](https://img.shields.io/badge/📍%20Location-Warszawa,%20Polska-red?style=for-the-badge)  
![Phone](https://img.shields.io/badge/📞_Whatsapp_&_Phone-%2B48%20539%20298%20079-orange?style=for-the-badge&logo=whatsapp)

[![GitHub](https://img.shields.io/badge/GitHub-sebastian--c87-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sebastian-c87)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sebastian%20Ciborowski-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sebastian-ciborowski-8442a6302/)  
[![Gmail](https://img.shields.io/badge/Gmail-Kontakt_bezpośredni-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ciborowski.s@gmail.com) 

<div align="center">

⭐ **Jeśli ten projekt Ci pomógł, zostaw gwiazdkę!** ⭐

</div>

[⬆ Powrót na górę](#-image-recognition-ai)

