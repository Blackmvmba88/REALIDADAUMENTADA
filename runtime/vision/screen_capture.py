"""
Screen capture engine - High-performance frame grabbing
"""

import numpy as np
import mss
import time
from typing import Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Frame:
    """Captured frame with metadata"""
    image: np.ndarray
    timestamp: float
    frame_id: int
    width: int
    height: int
    
    def __post_init__(self):
        self.datetime = datetime.fromtimestamp(self.timestamp)


class ScreenCapture:
    """Efficient screen capture using mss"""
    
    def __init__(self, monitor_index: int = 1, target_fps: int = 30):
        """
        Initialize screen capture
        
        Args:
            monitor_index: Monitor to capture (1-indexed, 1 is primary)
            target_fps: Target frames per second
        """
        self.sct = mss.mss()
        self.monitor_index = monitor_index
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.frame_count = 0
        self.last_capture_time = 0
        
        # Get monitor info
        self.monitor = self.sct.monitors[monitor_index]
        self.width = self.monitor['width']
        self.height = self.monitor['height']
        
    def capture(self) -> Optional[Frame]:
        """Capture a single frame with timing control"""
        current_time = time.time()
        
        # Enforce FPS limit
        if current_time - self.last_capture_time < self.frame_time:
            return None
        
        # Capture
        screenshot = self.sct.grab(self.monitor)
        image = np.array(screenshot)
        # Convert BGRA to BGR
        image = image[:, :, :3]
        
        self.frame_count += 1
        self.last_capture_time = current_time
        
        return Frame(
            image=image,
            timestamp=current_time,
            frame_id=self.frame_count,
            width=self.width,
            height=self.height
        )
    
    def get_monitor_info(self) -> dict:
        """Get monitor information"""
        return {
            'width': self.width,
            'height': self.height,
            'top': self.monitor['top'],
            'left': self.monitor['left']
        }
    
    def close(self):
        """Cleanup"""
        if self.sct:
            self.sct.close()
