"""
Image Recognition AI Package
GPT-5 powered image analysis and recognition tool
"""

__version__ = "1.0.0"
__author__ = "AI Developer" 
__description__ = "Advanced image recognition using OpenAI GPT-5 Vision and TensorFlow"

# Package exports
from .config import Config
from .openai_client import ImageRecognitionAI
from .image_processor import ImageProcessor

__all__ = ['Config', 'ImageRecognitionAI', 'ImageProcessor']
