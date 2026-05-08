# REALIDADAUMENTADA - Perception Runtime

## Vision Cognitiva + Asistencia Adaptativa + Runtime Universal

### 🔥 What This Is

Not an overlay script. Not a tutorial AI. 

This is the **foundation of a Cognitive Augmented Reality System** that perceives, understands, and assists across any digital interface.

### 🚀 Architecture

```
Perception Runtime
├── Vision Engine 👁️
│   ├── Screen Capture (mss)
│   ├── Object Detection (YOLOv8)
│   ├── Text Recognition (EasyOCR)
│   ├── UI Mapping (Semantic)
│   └── Tracking (Coherence)
├── Cognition Engine 🧠
│   ├── State Machine
│   ├── Context Builder
│   ├── Intent Detection
│   └── Action Prediction
├── Overlay Renderer 🎨
│   ├── PyQt6 Transparent Overlay
│   ├── Real-time Visualization
│   └── Animations
└── Memory System 💾
    ├── Telemetry
    ├── Session Logging
    └── State History
```

### 📊 Vision Pipeline

**Screen Capture** → **Detection** → **OCR** → **UI Mapping** → **Tracking** → **State**

### ⚙️ Getting Started

#### 1. Install dependencies

```bash
pip install -r requirements.txt
```

#### 2. Run the runtime

```bash
python -m runtime.main
```

### 🧬 Key Components

#### Vision (`runtime/vision/`)
- **ScreenCapture**: High-FPS frame grabbing
- **ObjectDetector**: YOLOv8-based detection
- **OCREngine**: Text recognition
- **UIMapper**: Semantic UI element classification
- **ElementTracker**: Track elements across frames

#### Cognition (`runtime/cognition/`)
- **StateEngine**: World model state tracking
- **ContextBuilder**: Semantic context from state

#### Overlays (`runtime/overlays/`)
- **OverlayRenderer**: PyQt6-based transparent overlay

#### Memory (`runtime/memory/`)
- **Telemetry**: Event logging and session management

### 🎯 Next Steps (Roadmap)

**Sprint 1 ✅** - Vision Runtime (Current)
- ✅ Modular architecture
- ✅ Screen capture
- ✅ YOLO detection
- ✅ OCR integration
- ✅ UI semantic mapping
- ✅ Element tracking

**Sprint 2** - Context Engine
- [ ] Advanced mode detection
- [ ] Workflow recognition
- [ ] Intent inference
- [ ] Action prediction

**Sprint 3** - Intelligent Assistant
- [ ] Ollama integration
- [ ] Voice (Whisper)
- [ ] TTS output
- [ ] Contextual recommendations

**Sprint 4** - Agentic Runtime
- [ ] Adaptive control
- [ ] Macro execution
- [ ] PID assistance
- [ ] Multi-app adapters

### 🔗 Supported Applications

- Blender (primary)
- VSCode (in progress)
- DJI (planned)
- Xbox Controller (planned)
- Generic (fallback)

### 📝 Configuration

Edit `runtime/config/settings.py`:

```python
vision_config = VisionConfig(
    monitor_index=1,
    capture_fps=30,
    yolo_model="yolov8n.pt",
    yolo_confidence=0.45
)
```

### 🛠️ Development

```bash
# Format code
black runtime/

# Lint
flake8 runtime/

# Type checking
mypy runtime/

# Tests
pytest tests/
```

### 📚 Documentation

Each module has detailed docstrings. Start with:
- `runtime/main.py` - Entry point
- `runtime/vision/screen_capture.py` - Frame grabbing
- `runtime/cognition/state_engine.py` - State management

### ⚡ Performance

- **Target FPS**: 30 (configurable)
- **Detection latency**: ~50ms (YOLOv8 nano)
- **OCR latency**: ~200ms
- **Total pipeline**: ~250ms (full perception cycle)

### 🔮 Vision

This system will eventually enable:
- Cross-application learning
- Adaptive assistance
- Gesture-aware control
- Multi-modal interaction
- Autonomous optimization

### 📄 License

Built with 🔥 by @Blackmvmba88

---

**Remember**: This is not about detecting rectangles. 

This is about **interpreting the digital world and responding to it intelligently**.
