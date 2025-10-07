"""
Image processing utilities for Image Recognition AI
"""
import os
import io
import base64
import logging
import requests
from typing import Optional, Tuple, Union, List
from pathlib import Path
from PIL import Image, ImageOps, ExifTags
import numpy as np

from config import Config

class ImageProcessor:
    """Advanced image processing for AI recognition"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def validate_image(self, image_path: str) -> bool:
        """Validate if image is suitable for processing"""
        try:
            # Check file existence
            if image_path.startswith(('http://', 'https://')):
                return self._validate_url_image(image_path)
            
            if not os.path.exists(image_path):
                self.logger.error(f"Image file not found: {image_path}")
                return False
            
            # Check file size
            file_size = os.path.getsize(image_path)
            if file_size > self.config.max_image_size:
                self.logger.error(f"Image too large: {file_size} bytes")
                return False
            
            # Check file format
            file_extension = Path(image_path).suffix.lower()
            if file_extension not in self.config.supported_formats:
                self.logger.error(f"Unsupported format: {file_extension}")
                return False
            
            # Try to open image
            with Image.open(image_path) as img:
                img.verify()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Image validation failed: {str(e)}")
            return False
    
    def _validate_url_image(self, url: str) -> bool:
        """Validate image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.head(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            if not any(fmt in content_type for fmt in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']):
                self.logger.error(f"Invalid content type: {content_type}")
                return False
            
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > self.config.max_image_size:
                self.logger.error(f"Image too large: {content_length} bytes")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"URL validation failed: {str(e)}")
            return False
    
    def download_image(self, url: str, save_path: Optional[str] = None) -> Optional[str]:
        """Download image from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            self.logger.info(f"Downloading image from: {url}")
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            if save_path is None:
                save_path = "temp_downloaded_image.jpg"
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.logger.info(f"Image downloaded to: {save_path}")
            return save_path
            
        except Exception as e:
            self.logger.error(f"Failed to download image: {str(e)}")
            return None
    
    def preprocess_image(self, image_path: str, optimize_for_ai: bool = True) -> Optional[str]:
        """Preprocess image for better AI recognition - ZOPTYMALIZOWANE"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    self.logger.info(f"Converted image to RGB mode")
            
                # Handle EXIF orientation
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                
                    exif = img._getexif()
                    if exif is not None:
                        orientation_value = exif.get(orientation)
                        if orientation_value:
                            img = ImageOps.exif_transpose(img)
                            self.logger.info("Applied EXIF orientation correction")
                except:
                    pass  # Skip if EXIF not available
            
                # NAPRAWIONE: Zmniejszamy rozmiary dla GPT-5-nano (oszczędzamy tokeny)
                # Maksymalny rozmiar dla vision models
                max_dimension = 1024  # Zmniejszone z 2048
            
                if img.width > max_dimension or img.height > max_dimension:
                    img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                    self.logger.info(f"Resized image to: {img.size}")
            
                # NAPRAWIONE: Nie procesuj już procesowanych obrazów
                if "processed_" in os.path.basename(image_path):
                    self.logger.info("Image already processed, skipping re-processing")
                    return image_path
            
                # Optimize for AI analysis
                if optimize_for_ai:
                    # Enhance contrast slightly
                    from PIL import ImageEnhance
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.05)  # Zmniejszone z 1.1
                
                    # Sharpen slightly
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(1.05)  # Zmniejszone z 1.1
            
                # Save processed image with lower quality for token savings
                processed_path = f"processed_{Path(image_path).name}"
                img.save(processed_path, 'JPEG', 
                        quality=75,  # Zmniejszone z 85 - oszczędzamy tokeny
                        optimize=True)
            
                self.logger.info(f"Preprocessed image saved to: {processed_path}")
                return processed_path
            
        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {str(e)}")
            return None
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Encode image to base64 for OpenAI Vision API"""
        try:
            with open(image_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                self.logger.info("Image encoded to base64")
                return encoded_string
                
        except Exception as e:
            self.logger.error(f"Base64 encoding failed: {str(e)}")
            return None
    
    def get_image_info(self, image_path: str) -> dict:
        """Get detailed image information"""
        try:
            info = {
                'path': image_path,
                'exists': False,
                'size_bytes': 0,
                'dimensions': (0, 0),
                'format': 'unknown',
                'mode': 'unknown',
                'has_exif': False,
                'valid': False
            }
            
            if os.path.exists(image_path):
                info['exists'] = True
                info['size_bytes'] = os.path.getsize(image_path)
                
                with Image.open(image_path) as img:
                    info['dimensions'] = img.size
                    info['format'] = img.format or 'unknown'
                    info['mode'] = img.mode
                    info['has_exif'] = hasattr(img, '_getexif') and img._getexif() is not None
                    info['valid'] = True
            
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get image info: {str(e)}")
            return {'error': str(e), 'valid': False}
    
    def create_thumbnail(self, image_path: str, size: Tuple[int, int] = (200, 200)) -> Optional[str]:
        """Create thumbnail of the image"""
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                thumbnail_path = f"thumbnail_{Path(image_path).name}"
                img.save(thumbnail_path, 'JPEG', quality=80)
                
                self.logger.info(f"Thumbnail created: {thumbnail_path}")
                return thumbnail_path
                
        except Exception as e:
            self.logger.error(f"Thumbnail creation failed: {str(e)}")
            return None
    
    def cleanup_temp_files(self, file_patterns: List[str] = None):
        """Clean up temporary files"""
        if file_patterns is None:
            file_patterns = [
                "temp_*.jpg", "temp_*.jpeg", "temp_*.png",
                "processed_*.jpg", "thumbnail_*.jpg",
                "temp_downloaded_image.*"
            ]
        
        try:
            import glob
            files_removed = 0
            
            for pattern in file_patterns:
                for file_path in glob.glob(pattern):
                    try:
                        os.remove(file_path)
                        files_removed += 1
                    except:
                        pass
            
            if files_removed > 0:
                self.logger.info(f"Cleaned up {files_removed} temporary files")
                
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
