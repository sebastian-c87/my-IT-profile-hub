"""
Configuration management for Social Media Generator
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
    timeout: int = 30
    
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
            timeout=int(os.getenv('TIMEOUT', '30'))
        )
