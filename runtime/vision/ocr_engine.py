"""
Optical Character Recognition engine
"""

import numpy as np
from typing import List, Optional
from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)


@dataclass
class TextDetection:
    """A single text detection"""
    text: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float
    language: str = "en"
    
    @property
    def center(self) -> tuple:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)


class OCREngine:
    """EasyOCR text recognition"""
    
    def __init__(self, languages: List[str] = None, confidence_threshold: float = 0.3):
        """
        Initialize OCR engine
        
        Args:
            languages: Languages to recognize (e.g., ['en', 'es'])
            confidence_threshold: Minimum confidence for text
        """
        self.languages = languages or ['en']
        self.confidence_threshold = confidence_threshold
        self.reader = None
        
        try:
            import easyocr
            self.reader = easyocr.Reader(self.languages, gpu=True)
            logger.info(f"OCR initialized with languages: {self.languages}")
        except ImportError:
            logger.error("easyocr not installed. Install with: pip install easyocr")
        except Exception as e:
            logger.warning(f"GPU not available for OCR, using CPU: {e}")
            try:
                import easyocr
                self.reader = easyocr.Reader(self.languages, gpu=False)
            except ImportError:
                logger.error("easyocr not installed")
    
    def recognize(self, image: np.ndarray) -> List[TextDetection]:
        """Recognize text in image
        
        Args:
            image: Input image (BGR)
            
        Returns:
            List of text detections
        """
        if self.reader is None:
            return []
        
        try:
            # Convert BGR to RGB for OCR
            image_rgb = image[:, :, ::-1]
            results = self.reader.readtext(image_rgb)
            
            detections = []
            for detection in results:
                coords = detection[0]
                text = detection[1]
                confidence = float(detection[2])
                
                if confidence < self.confidence_threshold:
                    continue
                
                # Extract bounding box
                x_coords = [point[0] for point in coords]
                y_coords = [point[1] for point in coords]
                x1, x2 = min(x_coords), max(x_coords)
                y1, y2 = min(y_coords), max(y_coords)
                
                text_det = TextDetection(
                    text=text,
                    confidence=confidence,
                    x1=float(x1),
                    y1=float(y1),
                    x2=float(x2),
                    y2=float(y2)
                )
                detections.append(text_det)
            
            return detections
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return []
    
    def extract_text_from_region(self, image: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> str:
        """Extract text from a specific region"""
        region = image[y1:y2, x1:x2]
        detections = self.recognize(region)
        return " ".join([d.text for d in detections])
