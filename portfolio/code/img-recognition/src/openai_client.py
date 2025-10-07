"""
OpenAI GPT-5-mini Client with Vision - Responses API correct format
"""
import os
import logging
import base64
from typing import Optional, Dict, Any
from openai import OpenAI

from config import Config
from image_processor import ImageProcessor

class ImageRecognitionAI:
    """GPT-5-mini with Responses API - correct multimodal format"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.image_processor = ImageProcessor(config)
        self.logger = logging.getLogger(__name__)
        
    def analyze_image(self, image_path: str, analysis_type: str = "comprehensive",
                     language: str = "polish", custom_prompt: str = "") -> Dict[str, Any]:
        """
        Analyze image using GPT-5-mini with Responses API
        """
        try:
            # Download if URL
            if image_path.startswith(('http://', 'https://')):
                self.logger.info("Downloading image from URL...")
                downloaded_path = self.image_processor.download_image(image_path)
                if not downloaded_path:
                    return {"error": "Failed to download image", "success": False}
                image_path = downloaded_path
            
            # Validate
            if not self.image_processor.validate_image(image_path):
                return {"error": "Invalid image file", "success": False}
            
            # Preprocess only once
            if not "processed_" in os.path.basename(image_path):
                processed_path = self.image_processor.preprocess_image(image_path)
                if processed_path:
                    image_path = processed_path
            
            # Encode to base64
            image_base64 = self.image_processor.encode_image_to_base64(image_path)
            if not image_base64:
                return {"error": "Failed to encode image", "success": False}
            
            # Build prompt
            analysis_prompt = self._build_analysis_prompt(analysis_type, language, custom_prompt)
            
            # NAPRAWIONE: image_url jest stringiem, nie obiektem!
            response = self.client.responses.create(
                model="gpt-5-mini",
                input=[
                    {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": analysis_prompt
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{image_base64}"  # ✅ Bezpośredni string!
                            }
                        ]
                    }
                ],
                reasoning={"effort": "medium"},
                text={"verbosity": "high"},
                max_output_tokens=1200
            )
            
            analysis_result = response.output_text.strip()
            
            # Get image info
            image_info = self.image_processor.get_image_info(image_path)
            
            # Cleanup
            self.image_processor.cleanup_temp_files()
            
            return {
                "analysis": analysis_result,
                "analysis_type": analysis_type,
                "language": language,
                "image_info": image_info,
                "success": True,
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            self.logger.error(f"Image analysis failed: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}", 
                "success": False,
                "timestamp": self._get_timestamp()
            }
    
    def _build_analysis_prompt(self, analysis_type: str, language: str, custom_prompt: str) -> str:
        """Build concise, direct analysis prompt"""
        
        if custom_prompt:
            return custom_prompt
        
        if language == "polish":
            prompts = {
                "comprehensive": """Przeanalizuj szczegółowo ten obraz. Opisz wszystkie widoczne elementy, scenę, obiekty, osoby, kolory, oświetlenie, teksty i nastrój. Podaj kompletną analizę.""",
                
                "objects": """Zidentyfikuj i opisz WSZYSTKIE obiekty na tym obrazie. Dla każdego podaj: nazwę, położenie w kadrze, rozmiar, stan, kolor i materiał.""",
                
                "scene": """Opisz szczegółowo scenę: gdzie to się dzieje, jaka sytuacja, co się dzieje, pora dnia/roku.""",
                
                "text": """Znajdź i przepisz DOKŁADNIE wszystkie teksty, napisy, znaki i symbole widoczne na tym obrazie. Zachowaj formatowanie.""",
                
                "artistic": """Wykonaj profesjonalną analizę artystyczną: styl fotograficzny, technika, kompozycja, światło, kolory, głębia ostrości, wartości estetyczne."""
            }
        else:
            prompts = {
                "comprehensive": """Analyze this image in detail. Describe all visible elements, scene, objects, people, colors, lighting, text and mood. Provide complete analysis.""",
                
                "objects": """Identify and describe ALL objects in this image. For each provide: name, position, size, condition, color and material.""",
                
                "scene": """Describe the scene in detail: where is this, what situation, what's happening, time of day/year.""",
                
                "text": """Find and transcribe EXACTLY all text, signs, symbols visible in this image. Preserve formatting.""",
                
                "artistic": """Perform professional artistic analysis: photographic style, technique, composition, light, colors, depth of field, aesthetic values."""
            }
        
        return prompts.get(analysis_type, prompts["comprehensive"])
    
    def compare_images(self, image_path1: str, image_path2: str, 
                      language: str = "polish") -> Dict[str, Any]:
        """Compare two images"""
        try:
            # Analyze both
            result1 = self.analyze_image(image_path1, "comprehensive", language)
            result2 = self.analyze_image(image_path2, "comprehensive", language)
            
            if result1["success"] and result2["success"]:
                compare_prompt = f"""Porównaj te dwa obrazy:

OBRAZ 1: {result1["analysis"]}

OBRAZ 2: {result2["analysis"]}

Opisz podobieństwa, różnice i wnioski.""" if language == "polish" else f"""Compare these images:

IMAGE 1: {result1["analysis"]}

IMAGE 2: {result2["analysis"]}

Describe similarities, differences and conclusions."""
                
                response = self.client.responses.create(
                    model="gpt-5-mini",
                    input=compare_prompt,
                    reasoning={"effort": "medium"},
                    text={"verbosity": "high"},
                    max_output_tokens=1000
                )
                
                return {
                    "comparison": response.output_text.strip(),
                    "success": True,
                    "timestamp": self._get_timestamp()
                }
            else:
                return {"error": "Failed to analyze one or both images", "success": False}
            
        except Exception as e:
            self.logger.error(f"Image comparison failed: {str(e)}")
            return {"error": f"Comparison failed: {str(e)}", "success": False}
    
    def extract_text_from_image(self, image_path: str, language: str = "polish") -> Dict[str, Any]:
        """Extract text from image (OCR)"""
        result = self.analyze_image(image_path, "text", language)
        
        if result["success"]:
            return {
                "extracted_text": result["analysis"],
                "success": True,
                "timestamp": self._get_timestamp()
            }
        else:
            return result
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
