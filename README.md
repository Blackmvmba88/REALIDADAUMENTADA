# 🕶️ REALIDAD AUMENTADA

## Augmented Reality Assistant
### by Iyari Cancino Gomez / BlackMamba RECORDS

**Learn by seeing. Act by following. Master by doing.**

REALIDAD AUMENTADA is an experimental augmented-reality assistant for learning
complex software through visual guidance directly on the screen.

The current proof of concept uses computer vision to detect a target UI element
on the user screen and draws a transparent overlay around it. The long-term goal
is to evolve this into a tutorial engine that can guide users through tools like
Blender, Ableton, creative software, engineering dashboards, and technical
workflows.

---

## Core Idea

Instead of explaining software only with text, this system points at the actual
interface.

```text
Screen Capture
   ↓
Computer Vision Detection
   ↓
Target Match
   ↓
Transparent Overlay
   ↓
Instruction / Highlight
   ↓
User Action
   ↓
Next Step
```

The assistant becomes a visual layer between the user and the software being
learned.

---

## Current Prototype

The prototype includes:

- Screen capture with `mss`.
- Image recognition with OpenCV template matching.
- Transparent always-on-top overlay with Tkinter.
- Rectangle highlight around detected UI targets.
- Simulation mode for environments without a GUI display.

Current entry point:

```bash
python main.py
```

The default target image is:

```text
blender_template.png
```

---

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

Expected behavior:

1. The app starts the AR assistant.
2. It captures the screen.
3. It searches for the configured template image.
4. If found, it draws a red rectangle over the matching UI element.
5. If a GUI cannot be created, it falls back to simulation mode.

---

## Repository Contents

```text
main.py                  Core AR assistant prototype
requirements.txt         Python dependencies
ROADMAP.md               Development roadmap
blender_template.png     Example target image
audio_dance.gif          Audio-reactive visual output
animate_dance.py         Audio-reactive animation experiment
visualize_waveform.py    Waveform visualization experiment
waveform.png             Generated waveform artifact
waveform_with_beats.png  Generated waveform artifact with beats
```

---

## Roadmap Direction

The project roadmap moves toward:

- Structured tutorial files using JSON or YAML.
- A tutorial runner that executes steps in order.
- Rich overlay instructions.
- Hotkeys for pause, resume, skip, and exit.
- More robust detection using ORB/SIFT-style feature matching.
- OCR-assisted screen understanding.
- Tutorial creator tools.
- Packaging for Windows, macOS, and Linux.

See [`ROADMAP.md`](ROADMAP.md).

---

## Future Vision

REALIDAD AUMENTADA can become a learning engine for:

- Blender tutorials.
- Ableton / music production workflows.
- Video editing interfaces.
- Engineering software.
- Electronics repair overlays.
- Computer maintenance guidance.
- AR-guided classroom systems.
- BlackMamba University training modules.

The final goal is not just a helper app.

The final goal is a visual mentor: a system that watches the interface, detects
where the user is, and shows the next correct action.

---

## Safety and Privacy Boundary

This prototype captures the local screen for visual matching.

Current behavior:

- No cloud upload.
- No remote inference.
- No account login automation.
- No hidden recording.
- No credential handling.

Recommended rule:

```text
Do not run on private, banking, password, or sensitive screens.
```

Future versions should include explicit privacy controls, capture indicators,
local-only mode, and user-controlled permissions.

---

## Author

**Iyari Cancino Gomez**  
Founder of **BlackMamba RECORDS**.

REALIDAD AUMENTADA is part of the BlackMamba engineering ecosystem: visual
intelligence, creative tools, music technology, augmented learning, and practical
systems for people who want to learn faster by seeing the next move.
