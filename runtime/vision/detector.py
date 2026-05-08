"""
Object detection engine using YOLOv8
"""

import numpy as np
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
import logging


logger = logging.getLogger(__name__)


@dataclass
class Detection:
    """A single detection result"""
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_id: int
    class_name: str
    mask: Optional[np.ndarray] = None
    
    @property
    def bbox(self) -> Tuple[float, float, float, float]:
        return (self.x1, self.y1, self.x2, self.y2)
    
    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
    
    @property
    def area(self) -> float:
        return (self.x2 - self.x1) * (self.y2 - self.y1)


class ObjectDetector:
    """YOLOv8 object detector"""
    
    def __init__(self, model_name: str = "yolov8n.pt", confidence: float = 0.45):
        """
        Initialize YOLO detector
        
        Args:
            model_name: YOLOv8 model (n, s, m, l, x)
            confidence: Detection confidence threshold
        """
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_name)
            self.confidence = confidence
            logger.info(f"Loaded YOLOv8 model: {model_name}")
        except ImportError:
            logger.error("ultralytics not installed. Install with: pip install ultralytics")
            self.model = None
    
    def detect(self, image: np.ndarray) -> List[Detection]:
        """Detect objects in image
        
        Args:
            image: Input image (BGR)
            
        Returns:
            List of detections
        """
        if self.model is None:
            return []
        
        try:
            results = self.model(image, conf=self.confidence, verbose=False)
            detections = []
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id]
                    
                    detection = Detection(
                        x1=float(x1),
                        y1=float(y1),
                        x2=float(x2),
                        y2=float(y2),
                        confidence=confidence,
                        class_id=class_id,
                        class_name=class_name
                    )
                    detections.append(detection)
            
            return detections
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []
    
    def detect_ui_elements(self, image: np.ndarray) -> List[Detection]:
        """Detect UI elements (buttons, panels, etc)
        
        This is a specialized detector for UI elements.
        Currently uses generic YOLO, but can be replaced with
        a custom-trained UI detector.
        """
        # For now, use generic detection
        # TODO: Train custom UI detector on Blender/VSCode screenshots
        return self.detect(image)
