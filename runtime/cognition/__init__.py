"""
Cognition Engine - Context & State Management

Handles:
- State machine
- Context building
- Intent detection
- Action prediction
"""

from .state_engine import StateEngine
from .context_builder import ContextBuilder

__all__ = [
    'StateEngine',
    'ContextBuilder'
]
