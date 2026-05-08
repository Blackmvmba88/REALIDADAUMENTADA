"""
Telemetry and logging system
"""

import logging
from typing import Any, Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json

from ..config.settings import telemetry_config, LOGS_DIR


logger = logging.getLogger(__name__)


@dataclass
class TelemetryEvent:
    """A single telemetry event"""
    timestamp: float
    event_type: str
    data: Dict[str, Any]
    
    def to_dict(self) -> dict:
        return asdict(self)


class Telemetry:
    """Telemetry collection and logging"""
    
    def __init__(self, session_name: str = "default"):
        self.session_name = session_name
        self.events: List[TelemetryEvent] = []
        self.start_time = datetime.now()
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup Python logging"""
        log_level = getattr(logging, telemetry_config.log_level)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        root_logger.addHandler(handler)
        
        # File handler
        log_file = LOGS_DIR / f"{self.session_name}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    def log_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        timestamp: float = None
    ) -> TelemetryEvent:
        """Log a telemetry event"""
        import time
        if timestamp is None:
            timestamp = time.time()
        
        event = TelemetryEvent(
            timestamp=timestamp,
            event_type=event_type,
            data=data
        )
        
        self.events.append(event)
        
        # Trim buffer
        if len(self.events) > telemetry_config.telemetry_buffer_size:
            self.events = self.events[-telemetry_config.telemetry_buffer_size:]
        
        return event
    
    def save_session(self) -> Path:
        """Save telemetry session to file"""
        session_file = LOGS_DIR / f"{self.session_name}_telemetry.json"
        
        data = {
            'session_name': self.session_name,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'events': [e.to_dict() for e in self.events]
        }
        
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Session saved to {session_file}")
        return session_file
