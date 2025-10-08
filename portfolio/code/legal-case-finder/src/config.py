"""
Konfiguracja aplikacji Legal Case Finder
Aplikacja oparta o prawo obowiązujące w Polsce
Integracja z Systemem Analizy Orzeczeń Sądowych
Uses OpenAI Responses API (GPT-5) 

To nie jest porada prawna - zawsze kontaktuj się z ustalonym ekspertem!

# Author: Sebastian C.
# Repository: https://github.com/sebastian-c87/my-IT-profile-hub
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

@dataclass
class Config:
    """Konfiguracja aplikacji"""
    
    # API Keys
    openai_api_key: str
    
    # Model Configuration
    model_name: str = "gpt-5-nano"
    reasoning_effort: str = "medium"
    text_verbosity: str = "high"
    max_output_tokens: int = 20000
    
    # Web Search Configuration
    enable_web_search: bool = True
    
    # Application Settings
    log_level: str = "INFO"
    
    # Lawyer Information
    lawyer_name: str = "Kamila Sadłowicz"
    lawyer_location: str = "Warszawa"
    lawyer_description: str = "Mecenas Kamila to doświadczona adwokatem z indywidualnym podejściem do każdej sprawy oraz \n gwarantuje maksymalne zaangażowanie w trakcie swoich działań podczas pomocy prawnej"
    
    # Legal Domains (Dziedziny prawa)
    legal_domains: tuple = (
        "Prawo karne",
        "Prawo cywilne",
        "Prawo rodzinne",
        "Prawo pracy",
        "Prawo spadkowe",
        "Prawo gospodarcze",
        "Prawo administracyjne",
        "Prawo podatkowe",
        "Prawo nieruchomości",
        "Prawo konsumenckie",
        "Prawo własności intelektualnej i AI"
    )
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Utwórz konfigurację z zmiennych środowiskowych"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "Brak klucza API OpenAI!\n"
                "Ustaw zmienną środowiskową OPENAI_API_KEY lub dodaj ją do pliku .env"
            )
        
        return cls(
            openai_api_key=api_key,
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
        )

# Globalna instancja konfiguracji
config = Config.from_env()
