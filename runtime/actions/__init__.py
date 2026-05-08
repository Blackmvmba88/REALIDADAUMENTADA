"""
Actions Module - System Control

Handles:
- Mouse control
- Keyboard control
- Macro execution
"""

from .mouse import MouseController
from .keyboard import KeyboardController

__all__ = ['MouseController', 'KeyboardController']
