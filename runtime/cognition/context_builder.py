"""
Context Builder - Constructs semantic context from state
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import logging

from .state_engine import WorldState


logger = logging.getLogger(__name__)


@dataclass
class Context:
    """Semantic context for decision making"""
    timestamp: float
    application: str
    mode: Optional[str]
    active_tool: Optional[str]
    recent_actions: List[str]
    visible_elements: List[str]
    inferred_intent: Optional[str] = None
    confidence: float = 0.5
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)


class ContextBuilder:
    """Builds semantic context from world state"""
    
    def __init__(self):
        self.context_history: List[Context] = []
        self.max_history = 50
    
    def build_context(self, state: WorldState) -> Context:
        """
        Build context from world state
        
        Args:
            state: Current world state
            
        Returns:
            Semantic context
        """
        visible_elements = list(state.ui_elements.keys())
        recent_actions = state.user_workflow[-5:] if state.user_workflow else []
        
        context = Context(
            timestamp=state.timestamp,
            application=state.application,
            mode=state.current_mode,
            active_tool=state.active_tool,
            recent_actions=recent_actions,
            visible_elements=visible_elements,
            confidence=state.confidence,
            metadata=state.metadata.copy()
        )
        
        # Infer intent
        context.inferred_intent = self._infer_intent(context)
        
        # Add to history
        self.context_history.append(context)
        if len(self.context_history) > self.max_history:
            self.context_history = self.context_history[-self.max_history:]
        
        return context
    
    def _infer_intent(self, context: Context) -> Optional[str]:
        """Infer user intent from context"""
        # Simple heuristics
        if context.active_tool:
            return f"using_{context.active_tool}"
        
        if context.recent_actions:
            return context.recent_actions[-1]
        
        return None
