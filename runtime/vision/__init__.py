"""
Vision Engine - Perception Layer

Handles:
- Screen capture
- Object detection (YOLOv8)
- Text recognition (OCR)
- UI element tracking
- Semantic mapping
"""

from .screen_capture import ScreenCapture
from .detector import ObjectDetector
from .ocr_engine import OCREngine
from .ui_mapper import UIMapper
from .trackers import ElementTracker

__all__ = [
    'ScreenCapture',
    'ObjectDetector',
    'OCREngine',
    'UIMapper',
    'ElementTracker'
]
