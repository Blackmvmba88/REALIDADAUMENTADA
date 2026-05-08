"""
UI Semantic Mapper - Maps UI elements to semantic understanding
"""

import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
import logging

from .detector import Detection
from .ocr_engine import TextDetection


logger = logging.getLogger(__name__)


class UIElementType(Enum):
    """Types of UI elements"""
    BUTTON = "button"
    PANEL = "panel"
    WINDOW = "window"
    MENU = "menu"
    TEXT = "text"
    TOOLBAR = "toolbar"
    ICON = "icon"
    UNKNOWN = "unknown"


@dataclass
class UIElement:
    """A semantic UI element"""
    element_type: UIElementType
    label: str
    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    metadata: Dict = field(default_factory=dict)
    
    @property
    def center(self) -> tuple:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
    
    @property
    def area(self) -> float:
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        d = asdict(self)
        d['element_type'] = self.element_type.value
        return d


@dataclass
class UIMap:
    """Complete semantic map of the UI"""
    timestamp: float
    application: str
    window_title: str
    elements: List[UIElement] = field(default_factory=list)
    screen_width: int = 0
    screen_height: int = 0
    metadata: Dict = field(default_factory=dict)
    
    def get_elements_by_type(self, element_type: UIElementType) -> List[UIElement]:
        """Get all elements of a specific type"""
        return [e for e in self.elements if e.element_type == element_type]
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp,
            'application': self.application,
            'window_title': self.window_title,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'elements': [e.to_dict() for e in self.elements],
            'metadata': self.metadata
        }
    
    def to_json(self) -> str:
        """Convert to JSON"""
        return json.dumps(self.to_dict(), indent=2)


class UIMapper:
    """Maps visual detections to semantic UI understanding"""
    
    def __init__(self):
        self.element_heuristics = self._init_heuristics()
    
    def _init_heuristics(self) -> dict:
        """Initialize heuristics for element classification"""
        return {
            'button': {
                'size_ratio': (0.02, 0.3),  # width/height ratio
                'min_aspect': 1.5,  # minimum aspect ratio
            },
            'panel': {
                'min_area': 10000,  # minimum pixels
                'aspect_range': (0.3, 3.0),
            },
            'toolbar': {
                'height_ratio': 0.15,  # max % of screen height
                'min_area': 5000,
            }
        }
    
    def build_ui_map(
        self,
        detections: List[Detection],
        text_detections: List[TextDetection],
        application: str = "unknown",
        window_title: str = "unknown",
        screen_width: int = 1920,
        screen_height: int = 1080,
        timestamp: float = 0.0
    ) -> UIMap:
        """
        Build semantic UI map from detections
        
        Args:
            detections: YOLO detections
            text_detections: OCR text detections
            application: Application name
            window_title: Window title
            screen_width: Screen width
            screen_height: Screen height
            timestamp: Timestamp of capture
            
        Returns:
            Semantic UI map
        """
        ui_map = UIMap(
            timestamp=timestamp,
            application=application,
            window_title=window_title,
            screen_width=screen_width,
            screen_height=screen_height
        )
        
        # Convert detections to UI elements
        for detection in detections:
            element = self._classify_detection(detection)
            ui_map.elements.append(element)
        
        # Add text as UI elements
        for text in text_detections:
            element = UIElement(
                element_type=UIElementType.TEXT,
                label=text.text,
                x1=text.x1,
                y1=text.y1,
                x2=text.x2,
                y2=text.y2,
                confidence=text.confidence,
                metadata={'ocr': True}
            )
            ui_map.elements.append(element)
        
        return ui_map
    
    def _classify_detection(self, detection: Detection) -> UIElement:
        """Classify a detection into a UI element type"""
        # Simple heuristic classification
        # This can be replaced with trained classifier
        
        width = detection.x2 - detection.x1
        height = detection.y2 - detection.y1
        area = width * height
        aspect_ratio = width / max(height, 1)
        
        # Classify based on heuristics
        if area > 100000:
            element_type = UIElementType.PANEL
        elif width > height and height < 50:
            element_type = UIElementType.TOOLBAR
        elif 1.5 <= aspect_ratio <= 4.0 and height < 100:
            element_type = UIElementType.BUTTON
        else:
            element_type = UIElementType.UNKNOWN
        
        return UIElement(
            element_type=element_type,
            label=detection.class_name,
            x1=detection.x1,
            y1=detection.y1,
            x2=detection.x2,
            y2=detection.y2,
            confidence=detection.confidence,
            metadata={
                'yolo_class': detection.class_name,
                'class_id': detection.class_id
            }
        )
