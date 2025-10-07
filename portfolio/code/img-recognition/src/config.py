"""
Configuration management for Image Recognition AI
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Application configuration"""
    openai_api_key: str
    log_level: str = "INFO"
    max_retries: int = 3
    timeout: int = 60
    max_image_size: int = 10 * 1024 * 1024  # ZMIENIONE: 10MB zamiast 20MB
    supported_formats: tuple = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
    image_quality: int = 75              # ZMIENIONE z 85
    max_width: int = 1024                # ZMIENIONE z 2048  
    max_height: int = 1024               # ZMIENIONE z 2048

    
    def __post_init__(self):
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
            
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables"""
        return cls(
            openai_api_key=os.getenv('OPENAI_API_KEY', ''),
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            timeout=int(os.getenv('TIMEOUT', '60')),
            max_image_size=int(os.getenv('MAX_IMAGE_SIZE', str(20 * 1024 * 1024)))
        )
