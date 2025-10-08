"""
Konfiguracja aplikacji RPG Story Generator
"""
import os
from dataclasses import dataclass
from typing import Optional, Tuple
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

@dataclass
class Config:
    """Konfiguracja aplikacji RPG"""
    
    # API Keys
    openai_api_key: str
    
    # Model Configuration
    model_name: str = "gpt-5-nano"
    reasoning_effort: str = "medium"
    text_verbosity: str = "high"
    max_output_tokens: int = 21500
    temperature: float = 0.85  # Większa kreatywność dla RPG
    
    # Story Configuration
    max_story_context: int = 13000  # Max znaków kontekstu
    min_story_length: int = 400  # Min słów w odpowiedzi
    auto_save: bool = True
    
    # Game Settings
    genres: Tuple[str, ...] = (
        "Fantasy",
        "Sci-Fi",
        "Horror",
        "Postapokalipsa",
        "Cyberpunk",
        "Steampunk",
        "Noir",
        "Superhero"
    )
    
    difficulties: Tuple[str, ...] = (
        "Łatwy",
        "Średni",
        "Trudny",
        "Hardcore"
    )
    
    # Logging
    log_level: str = "INFO"
    
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
