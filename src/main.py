#!/usr/bin/env python3
"""
ClipperTool - Advanced Clipboard Processing System
Main application entry point
"""

import tkinter as tk
import os
from utils.resources import resource_path
from ui.main_window import ClipperToolUI


def main():
    app = tk.Tk()
    app.title("ClipperTool")

    # Try to set the icon
    try:
        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            app.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not load icon: {e}")

    # Initialize the UI
    ClipperToolUI(app)

    # Start the application
    app.mainloop()


if __name__ == "__main__":
    main()
