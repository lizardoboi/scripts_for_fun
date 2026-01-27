"""
Simple Mouse Click Tracker
Tracks left, right, and middle mouse button clicks.
Press Escape to stop tracking.
"""

from pynput import mouse, keyboard
from datetime import datetime


class ClickTracker:
    def __init__(self):
        self.left_clicks = 0
        self.right_clicks = 0
        self.middle_clicks = 0
        self.click_log = []
        self.running = True

    def on_click(self, x, y, button, pressed):
        if pressed:
            timestamp = datetime.now().strftime("%H:%M:%S")

            if button == mouse.Button.left:
                self.left_clicks += 1
                btn_name = "Left"
            elif button == mouse.Button.right:
                self.right_clicks += 1
                btn_name = "Right"
            elif button == mouse.Button.middle:
                self.middle_clicks += 1
                btn_name = "Middle"
            else:
                btn_name = str(button)

            self.click_log.append((timestamp, btn_name, x, y))
            total = self.left_clicks + self.right_clicks + self.middle_clicks

            print(f"[{timestamp}] {btn_name} click at ({x}, {y}) | "
                  f"Total: {total} (L:{self.left_clicks} R:{self.right_clicks} M:{self.middle_clicks})")

    def on_key_press(self, key):
        if key == keyboard.Key.esc:
            self.running = False
            return False  # Stop keyboard listener

    def start(self):
        print("=" * 50)
        print("Mouse Click Tracker Started")
        print("Press Escape to stop")
        print("=" * 50)

        mouse_listener = mouse.Listener(on_click=self.on_click)
        keyboard_listener = keyboard.Listener(on_press=self.on_key_press)

        mouse_listener.start()
        keyboard_listener.start()

        keyboard_listener.join()  # Wait for Escape key
        mouse_listener.stop()

        self.print_summary()

    def print_summary(self):
        print("\n" + "=" * 50)
        print("Session Summary")
        print("=" * 50)
        print(f"Left clicks:   {self.left_clicks}")
        print(f"Right clicks:  {self.right_clicks}")
        print(f"Middle clicks: {self.middle_clicks}")
        print(f"Total clicks:  {self.left_clicks + self.right_clicks + self.middle_clicks}")
        print("=" * 50)


if __name__ == "__main__":
    tracker = ClickTracker()
    tracker.start()
