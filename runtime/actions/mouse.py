"""
Mouse control
"""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class MouseController:
    """Mouse control using pyautogui"""
    
    def __init__(self):
        try:
            import pyautogui
            self.pyautogui = pyautogui
            logger.info("Mouse controller initialized")
        except ImportError:
            logger.error("pyautogui not installed. Install with: pip install pyautogui")
            self.pyautogui = None
    
    def move_to(self, x: float, y: float, duration: float = 0.5):
        """Move mouse to position"""
        if self.pyautogui is None:
            return
        
        self.pyautogui.moveTo(x, y, duration=duration)
        logger.debug(f"Mouse moved to ({x}, {y})")
    
    def click(self, x: float = None, y: float = None, button: str = 'left'):
        """Click at position"""
        if self.pyautogui is None:
            return
        
        if x is not None and y is not None:
            self.pyautogui.click(x, y, button=button)
        else:
            self.pyautogui.click(button=button)
        
        logger.debug(f"Mouse click: {button} at ({x}, {y})")
    
    def get_position(self) -> Tuple[float, float]:
        """Get current mouse position"""
        if self.pyautogui is None:
            return (0, 0)
        
        return self.pyautogui.position()
