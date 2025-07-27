import tkinter as tk
import os
from utils.resources import resource_path
from ui.main_window import ClipperToolUI


class ClipperTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ClipperTool")
        self.running = False

        # Try to set the icon
        try:
            icon_path = resource_path("favicon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")

        # Initialize UI
        self.ui = ClipperToolUI(self.root)
        self.file_var = self.ui.file_var
        self.toggle_running = self.ui.toggle_running

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ClipperTool()
    app.run()
