# Project Roadmap: Augmented Reality Assistant

This document outlines the strategic roadmap for the development of the Augmented Reality Assistant. The goal is to evolve the current proof-of-concept into a robust and user-friendly application that can effectively teach users how to operate complex software like Blender, Ableton, etc.

## Phase 1: Proof of Concept (Completed)

This initial phase focused on validating the core technical idea.

*   **Status:** ✅ Complete
*   **Achievements:**
    *   Established a Python environment with necessary libraries (`OpenCV`, `mss`).
    *   Implemented a core function to find a static image (a "target") on the screen.
    *   Developed a basic transparent overlay window to display a highlight around the found target.
    *   The current script can successfully locate a predefined image on the screen and has a simulation mode for testing.

---

## Phase 2: Building the Tutorial Engine

This phase focuses on turning the core functionality into a flexible system for creating and running tutorials.

*   **Step 1: Structured Tutorial Format**
    *   **Goal:** Define a clear, file-based format for tutorials (e.g., using JSON or YAML). This decouples the tutorial content from the code.
    *   **Details:** A tutorial file will contain a list of steps. Each step should define:
        *   `target_image`: The path to the image file to search for.
        *   `instruction_text`: The text to display to the user for this step.
        *   `highlight_shape`: (e.g., "rectangle", "arrow") and its properties.

*   **Step 2: Tutorial Runner**
    *   **Goal:** Create a "runner" class that loads a tutorial file and executes it step-by-step.
    *   **Details:** The runner will manage the state of the tutorial. It will continuously look for the `target_image` of the current step. Once the target is found, it will display the corresponding instruction and highlight. It should then wait for a user action (e.g., a click or a key press) before moving to the next step.

*   **Step 3: Enhancing the Overlay**
    *   **Goal:** Improve the overlay to display rich information.
    *   **Details:** The overlay should be able to render the `instruction_text` clearly on the screen. It should also support drawing different shapes, like arrows, to point at UI elements more effectively.

---

## Phase 3: User Interface & Experience

This phase focuses on making the application easy and enjoyable to use.

*   **Step 1: Tutorial Selection Menu**
    *   **Goal:** Build a simple graphical user interface (GUI) that appears when the application starts.
    *   **Details:** This menu will allow users to browse and select which tutorial they want to run (e.g., "Blender: Creating a Donut - Part 1").

*   **Step 2: In-Tutorial Controls**
    *   **Goal:** Give users control while a tutorial is active.
    *   **Details:** Implement global keyboard shortcuts (hotkeys) to allow users to pause, resume, skip a step, or exit the tutorial at any time.

---

## Phase 4: Advanced Detection & Intelligence

This phase focuses on making the detection logic more robust and less brittle.

*   **Step 1: Advanced Image Recognition**
    *   **Goal:** Move beyond static template matching, which can fail if the UI theme, resolution, or scale changes.
    *   **Details:** Research and implement feature-based matching algorithms (e.g., SIFT, ORB in OpenCV). These methods are more resilient to changes in appearance.

*   **Step 2: Optical Character Recognition (OCR)**
    *   **Goal:** Add the ability to read text from the screen.
    *   **Details:** Integrate an OCR library (like Tesseract) to verify steps by reading the text of a menu or button, making detection much more reliable than just using images.

---

## Phase 5: Community & Distribution

This phase focuses on growing the project and making it accessible.

*   **Step 1: Tutorial Creator Tool**
    *   **Goal:** Build a simple tool that allows the community to easily create new tutorials.
    *   **Details:** This could be a GUI application that helps a user capture screen regions for `target_image`s and write the corresponding instructions, then exports it all into the correct tutorial format.

*   **Step 2: Packaging & Installation**
    *   **Goal:** Make the application easy to install and run for non-technical users.
    *   **Details:** Use a tool like PyInstaller or cx_Freeze to package the Python application into a single executable file for Windows, macOS, and Linux.
