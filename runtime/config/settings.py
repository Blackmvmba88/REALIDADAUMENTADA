"""
Global configuration and constants
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent
RUNTIME_DIR = ROOT_DIR / "runtime"
LOGS_DIR = ROOT_DIR / "logs"
MODELS_DIR = ROOT_DIR / "models"

# Create directories if they don't exist
for directory in [LOGS_DIR, MODELS_DIR]:
    directory.mkdir(exist_ok=True)


@dataclass
class VisionConfig:
    """Vision engine configuration"""
    # Screen capture
    monitor_index: int = 0
    capture_fps: int = 30
    
    # YOLOv8 detector
    yolo_model: str = "yolov8n.pt"  # nano model for speed
    yolo_confidence: float = 0.45
    yolo_iou: float = 0.5
    
    # OCR
    ocr_enabled: bool = True
    ocr_lang: List[str] = None
    ocr_confidence: float = 0.3
    
    # Tracker
    tracker_enabled: bool = True
    
    def __post_init__(self):
        if self.ocr_lang is None:
            self.ocr_lang = ['en', 'es']


@dataclass
class CognitionConfig:
    """Cognition engine configuration"""
    # State tracking
    state_update_interval: float = 0.1  # seconds
    
    # Context window
    context_history_size: int = 100
    
    # Inference
    enable_intent_detection: bool = True
    enable_action_prediction: bool = True


@dataclass
class OverlayConfig:
    """Overlay renderer configuration"""
    # Display
    width: int = 1920
    height: int = 1080
    always_on_top: bool = True
    opacity: float = 0.8
    
    # Rendering
    enable_animations: bool = True
    animation_fps: int = 60
    
    # Colors
    accent_color: tuple = (0, 255, 0)  # Green
    warning_color: tuple = (255, 165, 0)  # Orange
    error_color: tuple = (255, 0, 0)  # Red


@dataclass
class TelemetryConfig:
    """Telemetry and logging configuration"""
    log_level: str = "INFO"
    enable_telemetry: bool = True
    telemetry_buffer_size: int = 1000
    save_screenshots: bool = False
    screenshot_dir: Path = None
    
    def __post_init__(self):
        if self.screenshot_dir is None:
            self.screenshot_dir = LOGS_DIR / "screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)


# Runtime configuration instances
vision_config = VisionConfig()
cognition_config = CognitionConfig()
overlay_config = OverlayConfig()
telemetry_config = TelemetryConfig()


# Supported applications
SUPPORTED_APPS = {
    'blender': {
        'window_title_pattern': 'Blender',
        'modes': ['sculpt', 'edit', 'object', 'pose', 'weight_paint'],
        'ui_regions': ['toolbar', 'properties', 'viewport', 'outliner']
    },
    'vscode': {
        'window_title_pattern': 'Visual Studio Code',
        'modes': ['editor', 'debug', 'git'],
        'ui_regions': ['sidebar', 'editor', 'terminal', 'output']
    },
    'generic': {
        'window_title_pattern': '*',
        'modes': ['default'],
        'ui_regions': ['entire_screen']
    }
}
