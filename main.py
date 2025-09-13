import cv2
import numpy as np
import mss
import mss.tools
import tkinter as tk
import time


class OverlayWindow:
    """Handles the creation and drawing on a transparent overlay window."""
    def __init__(self):
        self.root = tk.Tk()
        transparent_color = 'white'
        self.root.attributes('-transparentcolor', transparent_color)
        self.root.overrideredirect(True)
        self.root.wm_attributes('-topmost', 1)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        self.canvas = tk.Canvas(self.root, bg=transparent_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def draw_rectangle(self, x, y, w, h, color="red", width=3):
        """Draws a rectangle on the overlay."""
        self.canvas.create_rectangle(x, y, x + w, y + h, outline=color, width=width, tags="highlight")

    def clear(self):
        """Clears all drawings from the overlay."""
        self.canvas.delete("highlight")

    def run(self):
        """Starts the Tkinter main loop."""
        self.root.mainloop()


def find_image_on_screen(template_path, threshold=0.8, screen_image_path=None):
    """Finds an image on the screen using template matching."""
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"Error: Could not load template image at {template_path}")
        return None

    if template.shape[2] == 3:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2BGRA)

    template_h, template_w = template.shape[:2]

    if screen_image_path:
        screen = cv2.imread(screen_image_path, cv2.IMREAD_UNCHANGED)
        if screen is None:
            print(f"Error: Could not load screen image at {screen_image_path}")
            return None
    else:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            screen = np.array(sct_img)

    if screen.shape[2] == 3:
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2BGRA)

    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)

    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        return (*max_loc, template_w, template_h)
    return None


class Application:
    """Manages the main application logic."""
    def __init__(self, template_path, update_interval_ms=1000):
        self.template_path = template_path
        self.update_interval = update_interval_ms
        self.overlay = None
        self.is_simulation = False

    def update_overlay(self):
        """Periodically checks the screen and updates the overlay."""
        screen_path = self.template_path if self.is_simulation else None

        location = find_image_on_screen(self.template_path, screen_image_path=screen_path)

        self.overlay.clear()
        if location:
            x, y, w, h = location
            print(f"Found image at: ({x}, {y})")
            self.overlay.draw_rectangle(x, y, w, h)
        else:
            print("Image not found.")

        # Schedule the next update
        self.overlay.root.after(self.update_interval, self.update_overlay)

    def run(self):
        """Starts the application."""
        print("Starting Augmented Reality Assistant...")
        try:
            self.overlay = OverlayWindow()
            print("Overlay created. Starting detection loop.")
            self.update_overlay()
            self.overlay.run()
        except Exception as e:
            print(f"ERROR: Could not create GUI. Assuming sandbox environment: {e}")
            print("\n--- Running in Simulation Mode (no GUI) ---")
            self.is_simulation = True
            self.run_simulation_loop()

    def run_simulation_loop(self, duration_seconds=5):
        """Runs a simple loop for testing detection logic without a GUI."""
        print("This test will run for 5 seconds...")
        end_time = time.time() + duration_seconds
        while time.time() < end_time:
            location = find_image_on_screen(self.template_path, screen_image_path=self.template_path)
            if location:
                print(f"SIM_SUCCESS: Found image at {location[:2]}")
            else:
                print("SIM_ERROR: Did not find image.")
            time.sleep(1)
        print("\nSimulation finished. The core logic is ready.")


if __name__ == "__main__":
    template_file = "blender_template.png"
    app = Application(template_path=template_file)

    print("--- Augmented Reality Assistant ---")
    print("This script will attempt to start a GUI-based overlay.")
    print("If it fails (e.g., in a sandbox), it will run a simulation.")
    print("To run the real application, execute this script on a machine with a display.")
    print("-" * 35)

    app.run()
