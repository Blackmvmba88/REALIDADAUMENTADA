"""
Keyboard control
"""

import logging
from typing import List

logger = logging.getLogger(__name__)


class KeyboardController:
    """Keyboard control using pyautogui"""
    
    def __init__(self):
        try:
            import pyautogui
            self.pyautogui = pyautogui
            logger.info("Keyboard controller initialized")
        except ImportError:
            logger.error("pyautogui not installed. Install with: pip install pyautogui")
            self.pyautogui = None
    
    def press(self, key: str):
        """Press a key"""
        if self.pyautogui is None:
            return
        
        self.pyautogui.press(key)
        logger.debug(f"Key pressed: {key}")
    
    def hotkey(self, *keys):
        """Press multiple keys simultaneously"""
        if self.pyautogui is None:
            return
        
        self.pyautogui.hotkey(*keys)
        logger.debug(f"Hotkey: {' + '.join(keys)}")
    
    def type_text(self, text: str, interval: float = 0.05):
        """Type text"""
        if self.pyautogui is None:
            return
        
        self.pyautogui.typewrite(text, interval=interval)
        logger.debug(f"Text typed: {text}")
