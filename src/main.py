import tkinter as tk
from tkinter import ttk
import os
import json
import threading
import time
import pyperclip
import ttkbootstrap as tb
import sys

CONFIG_DIR = os.path.join(os.path.expanduser("~"), "Documents", "ClipperTool")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
FILTERS_FOLDER = os.path.join(CONFIG_DIR, "Configs")

os.makedirs(FILTERS_FOLDER, exist_ok=True)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"selected_file": "", "mode": "remove"}
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        if "selected_file" not in data:
            data["selected_file"] = ""
        if "mode" not in data:
            data["mode"] = "remove"
        return data
    except Exception:
        return {"selected_file": "", "mode": "remove"}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Development mode - get the directory where this script is located
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class ClipboardCleaner:
    def __init__(self, keywords, mode):
        self.keywords = keywords
        self.mode = mode

    def process_text(self, text):
        lines = text.splitlines()
        if self.mode == "remove":
            filtered_lines = [line for line in lines if not any(keyword in line for keyword in self.keywords)]
        else:
            filtered_lines = [line for line in lines if any(keyword in line for keyword in self.keywords)]
        return "\n".join(filtered_lines)


class ClipperTool:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.config = load_config()
        self.running = False
        self.last_clipboard = None

        self.create_widgets()
        self.load_filter_files()
        self.update_ui()

    def create_widgets(self):
        self.style = tb.Style("cosmo")
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill="both", expand=True)

        self.file_var = tk.StringVar()
        self.file_dropdown = ttk.Combobox(self.frame, textvariable=self.file_var, state="readonly")
        self.file_dropdown.pack(fill="x", pady=5)

        self.start_stop_button = ttk.Button(self.frame, command=self.toggle_running)
        self.start_stop_button.pack(fill="x", pady=10)

        menubar = tk.Menu(self.root)
        mode_menu = tk.Menu(menubar, tearoff=0)
        mode_menu.add_command(label="Remove Mode", command=lambda: self.set_mode("remove"))
        mode_menu.add_command(label="Keep Mode", command=lambda: self.set_mode("keep"))
        menubar.add_cascade(label="Mode", menu=mode_menu)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Reload Configs", command=self.load_filter_files)
        menubar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menubar)

    def load_filter_files(self):
        files = [f for f in os.listdir(FILTERS_FOLDER) if f.endswith(".txt")]
        self.file_dropdown['values'] = files

        selected_file = self.config.get("selected_file", "")

        if selected_file in files:
            self.file_var.set(selected_file)
        elif files:
            self.file_var.set(files[0])
        else:
            self.file_var.set("")

        self.update_ui()

    def set_mode(self, mode):
        self.config["mode"] = mode
        self.save_and_update()

    def save_and_update(self):
        self.config["selected_file"] = self.file_var.get()
        save_config(self.config)
        self.update_ui()

    def update_ui(self):
        mode = self.config.get("mode", "remove")
        title_mode = "Remove Mode" if mode == "remove" else "Keep Mode"
        status_text = "Running" if self.running else "Stopped"
        self.root.title(f"ClipperTool - {title_mode} ({status_text})")

        bg_color = "#d0e7ff" if mode == "remove" else "#d0ffd8"
        self.root.configure(bg=bg_color)
        self.frame.configure(style="TFrame")
        self.start_stop_button.configure(
            text=f"Clipper is {status_text}. Press to {'stop' if self.running else 'run'} it."
        )

    def toggle_running(self):
        self.running = not self.running
        self.save_and_update()
        if self.running:
            threading.Thread(target=self.clipboard_loop, daemon=True).start()

    def clipboard_loop(self):
        while self.running:
            try:
                text = pyperclip.paste()
                if text != self.last_clipboard:
                    self.last_clipboard = text
                    cleaned = self.clean_clipboard(text)
                    if cleaned != text:
                        pyperclip.copy(cleaned)
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.5)

    def clean_clipboard(self, text):
        filename = self.file_var.get()
        filepath = os.path.join(FILTERS_FOLDER, filename)
        if not os.path.exists(filepath):
            return text

        with open(filepath, "r") as f:
            keywords = [line.strip() for line in f if line.strip()]

        cleaner = ClipboardCleaner(keywords, self.config["mode"])
        return cleaner.process_text(text)


if __name__ == "__main__":
    app = tk.Tk()

    # Try to set the icon - handle gracefully if it fails
    try:
        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            app.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not load icon: {e}")

    ClipperTool(app)
    app.mainloop()
