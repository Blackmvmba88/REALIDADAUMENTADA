"""
Main Runtime Orchestrator

Coordinates all perception, cognition, and action systems
"""

import time
import logging
from typing import Optional
from datetime import datetime

from config.settings import (
    vision_config,
    cognition_config,
    overlay_config,
    telemetry_config
)
from vision import (
    ScreenCapture,
    ObjectDetector,
    OCREngine,
    UIMapper,
    ElementTracker
)
from cognition import StateEngine, ContextBuilder
from overlays import OverlayRenderer
from memory import Telemetry


# Setup logging
logging.basicConfig(
    level=getattr(logging, telemetry_config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PerceptionRuntime:
    """
    Main runtime orchestrator
    
    Coordinates:
    - Vision: Screen capture, detection, OCR, UI mapping
    - Cognition: State tracking, context building
    - Action: Control systems
    - Memory: Telemetry and logging
    """
    
    def __init__(self, application: str = "blender"):
        logger.info(f"Initializing Perception Runtime for {application}")
        
        self.application = application
        self.running = False
        
        # Vision pipeline
        self.screen_capture = ScreenCapture(
            monitor_index=vision_config.monitor_index,
            target_fps=vision_config.capture_fps
        )
        self.detector = ObjectDetector(
            model_name=vision_config.yolo_model,
            confidence=vision_config.yolo_confidence
        )
        self.ocr = OCREngine(
            languages=vision_config.ocr_lang,
            confidence_threshold=vision_config.ocr_confidence
        ) if vision_config.ocr_enabled else None
        self.ui_mapper = UIMapper()
        self.tracker = ElementTracker() if vision_config.tracker_enabled else None
        
        # Cognition pipeline
        self.state_engine = StateEngine(application=application)
        self.context_builder = ContextBuilder()
        
        # Overlay
        self.overlay = OverlayRenderer(
            width=overlay_config.width,
            height=overlay_config.height
        )
        
        # Memory
        self.telemetry = Telemetry(session_name=application)
        
        logger.info("Perception Runtime initialized successfully")
    
    def run(self, duration: Optional[float] = None, fps_limit: int = 30):
        """
        Run the perception runtime
        
        Args:
            duration: Run duration in seconds (None for infinite)
            fps_limit: Maximum FPS
        """
        logger.info(f"Starting runtime - duration: {duration}, FPS limit: {fps_limit}")
        
        self.running = True
        self.overlay.start()
        
        start_time = time.time()
        frame_count = 0
        frame_time = 1.0 / fps_limit
        
        try:
            while self.running:
                loop_start = time.time()
                
                # Check duration
                if duration and (time.time() - start_time) > duration:
                    logger.info(f"Duration limit reached ({duration}s)")
                    break
                
                # Vision: Capture and process
                frame = self.screen_capture.capture()
                if frame is None:
                    continue
                
                # Detection
                detections = self.detector.detect(frame.image)
                
                # OCR
                text_detections = []
                if self.ocr:
                    text_detections = self.ocr.recognize(frame.image)
                
                # UI Mapping
                ui_map = self.ui_mapper.build_ui_map(
                    detections=detections,
                    text_detections=text_detections,
                    application=self.application,
                    screen_width=frame.width,
                    screen_height=frame.height,
                    timestamp=frame.timestamp
                )
                
                # Tracking
                if self.tracker:
                    ui_map = self.tracker.update(ui_map)
                
                # Cognition: Build state and context
                ui_elements_dict = {i: e.to_dict() for i, e in enumerate(ui_map.elements)}
                state = self.state_engine.update_state(
                    timestamp=frame.timestamp,
                    ui_elements=ui_elements_dict,
                    active_tool=None,
                    current_mode=None
                )
                
                context = self.context_builder.build_context(state)
                
                # Telemetry
                self.telemetry.log_event(
                    event_type='frame_processed',
                    data={
                        'frame_id': frame.frame_id,
                        'detections': len(detections),
                        'text_detections': len(text_detections),
                        'ui_elements': len(ui_map.elements)
                    },
                    timestamp=frame.timestamp
                )
                
                # Render
                self._render_frame(ui_map)
                
                # Frame rate control
                elapsed = time.time() - loop_start
                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)
                
                frame_count += 1
                
                if frame_count % 30 == 0:
                    fps = frame_count / (time.time() - start_time)
                    logger.debug(f"FPS: {fps:.1f}, Detections: {len(detections)}, UI: {len(ui_map.elements)}")
        
        except KeyboardInterrupt:
            logger.info("Runtime interrupted by user")
        except Exception as e:
            logger.error(f"Runtime error: {e}", exc_info=True)
        finally:
            self.stop()
    
    def _render_frame(self, ui_map):
        """Render UI map to overlay"""
        if not self.overlay.is_running:
            return
        
        self.overlay.clear()
        
        # Draw detected elements
        for element in ui_map.elements:
            color = overlay_config.accent_color
            label = f"{element.element_type.value}: {element.label}"
            
            self.overlay.draw_box(
                element.x1,
                element.y1,
                element.x2,
                element.y2,
                color=color,
                label=label
            )
    
    def stop(self):
        """Stop the runtime"""
        logger.info("Stopping runtime")
        self.running = False
        self.overlay.stop()
        
        # Save telemetry
        self.telemetry.save_session()
        
        # Cleanup
        self.screen_capture.close()
        
        logger.info("Runtime stopped")


if __name__ == "__main__":
    # Example usage
    runtime = PerceptionRuntime(application="blender")
    runtime.run(duration=10)  # Run for 10 seconds
