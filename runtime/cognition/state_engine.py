"""
State Engine - Maintains world model state
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
import json
import logging


logger = logging.getLogger(__name__)


class ApplicationState(Enum):
    """Known application states"""
    UNKNOWN = "unknown"
    STARTING = "starting"
    READY = "ready"
    PROCESSING = "processing"
    ERROR = "error"


@dataclass
class WorldState:
    """Complete world state snapshot"""
    timestamp: float
    application: str
    application_state: ApplicationState = ApplicationState.UNKNOWN
    
    # Visual state
    ui_elements: Dict[str, Any] = field(default_factory=dict)
    active_tool: Optional[str] = None
    focused_element: Optional[str] = None
    
    # Contextual state
    current_mode: Optional[str] = None
    user_workflow: List[str] = field(default_factory=list)
    
    # Predictions
    possible_next_actions: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Metadata
    confidence: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        d = asdict(self)
        d['application_state'] = self.application_state.value
        return d
    
    def to_json(self) -> str:
        """Convert to JSON"""
        return json.dumps(self.to_dict(), indent=2, default=str)


class StateEngine:
    """Manages application state"""
    
    def __init__(self, application: str = "unknown"):
        self.application = application
        self.current_state: Optional[WorldState] = None
        self.state_history: List[WorldState] = []
        self.max_history = 100
    
    def update_state(
        self,
        timestamp: float,
        ui_elements: Dict[str, Any],
        active_tool: Optional[str] = None,
        current_mode: Optional[str] = None
    ) -> WorldState:
        """
        Update world state
        
        Args:
            timestamp: Current timestamp
            ui_elements: Current UI elements
            active_tool: Currently active tool
            current_mode: Current application mode
            
        Returns:
            Updated world state
        """
        state = WorldState(
            timestamp=timestamp,
            application=self.application,
            ui_elements=ui_elements,
            active_tool=active_tool,
            current_mode=current_mode
        )
        
        # Infer state
        state = self._infer_state(state)
        
        # Add to history
        self.current_state = state
        self.state_history.append(state)
        
        # Trim history
        if len(self.state_history) > self.max_history:
            self.state_history = self.state_history[-self.max_history:]
        
        return state
    
    def _infer_state(self, state: WorldState) -> WorldState:
        """Infer application state"""
        # Heuristics for state detection
        if not state.ui_elements:
            state.application_state = ApplicationState.STARTING
        else:
            state.application_state = ApplicationState.READY
        
        # Detect workflow from history
        if self.current_state:
            state.user_workflow = self.current_state.user_workflow.copy()
            if state.active_tool != self.current_state.active_tool:
                state.user_workflow.append(f"switched_tool:{state.active_tool}")
        
        return state
    
    def get_current_state(self) -> Optional[WorldState]:
        """Get current state"""
        return self.current_state
    
    def get_state_history(self, n: int = 10) -> List[WorldState]:
        """Get last n state updates"""
        return self.state_history[-n:]
