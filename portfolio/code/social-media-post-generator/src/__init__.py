"""
Social Media Post Generator Package
GPT-5 powered content creation tool
"""

__version__ = "1.0.0"
__author__ = "AI Developer"
__description__ = "Professional social media content generator using OpenAI GPT-5"

# Package exports
from .config import Config
from .openai_client import SocialMediaAI

__all__ = ['Config', 'SocialMediaAI']
