"""
Element tracking - Maintains coherence across frames
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import logging

from .detector import Detection
from .ui_mapper import UIElement, UIMap


logger = logging.getLogger(__name__)


@dataclass
class TrackedElement:
    """A tracked element across frames"""
    track_id: int
    element: UIElement
    age: int = 1  # frames alive
    hits: int = 1  # times matched
    last_seen: int = 0  # last frame seen
    position_history: List[Tuple[float, float]] = field(default_factory=list)
    
    @property
    def confidence_score(self) -> float:
        """Confidence based on tracking history"""
        return min(self.element.confidence * (1.0 + self.hits / 10), 1.0)


class ElementTracker:
    """Tracks UI elements across frames"""
    
    def __init__(self, max_distance: float = 50.0, max_age: int = 30):
        """
        Initialize tracker
        
        Args:
            max_distance: Maximum distance to match elements
            max_age: Maximum frames to keep track without match
        """
        self.max_distance = max_distance
        self.max_age = max_age
        self.next_track_id = 0
        self.tracks: Dict[int, TrackedElement] = {}
        self.frame_count = 0
    
    def update(self, ui_map: UIMap) -> UIMap:
        """
        Update tracking with new UI map
        
        Args:
            ui_map: New UI map from perception
            
        Returns:
            Updated UI map with tracking IDs
        """
        self.frame_count += 1
        
        # Match current detections to existing tracks
        detections = ui_map.elements
        matched_tracks = set()
        matched_detections = set()
        
        # Hungarian matching (simple greedy for now)
        for det_idx, detection in enumerate(detections):
            best_track_id = None
            best_distance = self.max_distance
            
            for track_id, track in self.tracks.items():
                distance = self._distance(detection, track.element)
                if distance < best_distance:
                    best_distance = distance
                    best_track_id = track_id
            
            if best_track_id is not None:
                # Match found
                self.tracks[best_track_id].element = detection
                self.tracks[best_track_id].age += 1
                self.tracks[best_track_id].hits += 1
                self.tracks[best_track_id].last_seen = self.frame_count
                self.tracks[best_track_id].position_history.append(detection.center)
                matched_tracks.add(best_track_id)
                matched_detections.add(det_idx)
            else:
                # New track
                if self.next_track_id not in self.tracks:
                    track = TrackedElement(
                        track_id=self.next_track_id,
                        element=detection
                    )
                    track.position_history.append(detection.center)
                    self.tracks[self.next_track_id] = track
                    self.next_track_id += 1
                matched_detections.add(det_idx)
        
        # Remove old tracks
        to_remove = []
        for track_id, track in self.tracks.items():
            if self.frame_count - track.last_seen > self.max_age:
                to_remove.append(track_id)
        
        for track_id in to_remove:
            del self.tracks[track_id]
        
        # Add track IDs to metadata
        for det_idx, detection in enumerate(detections):
            if det_idx < len(detections):
                for track_id, track in self.tracks.items():
                    if track.element is detection:
                        detection.metadata['track_id'] = track_id
                        detection.metadata['track_age'] = track.age
                        detection.metadata['track_confidence'] = track.confidence_score
                        break
        
        return ui_map
    
    def _distance(self, detection1: UIElement, detection2: UIElement) -> float:
        """Calculate distance between two elements"""
        c1 = detection1.center
        c2 = detection2.center
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
    
    def get_tracked_elements(self) -> List[TrackedElement]:
        """Get all currently tracked elements"""
        return list(self.tracks.values())
