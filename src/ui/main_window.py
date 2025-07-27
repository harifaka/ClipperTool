import tkinter as tk
from tkinter import messagebox, ttk
import os
import threading
import time
import pyperclip
from constants import COLORS, FILTERS_FOLDER
from widgets import ControlSection, StatsSection, Footer
from popups import NewConfigPopup, open_file, open_folder

class ClipperTool:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.running = False
        self.processed_count = 0
        self.last_clipboard = ""

        # Create UI sections
        self.control_section = ControlSection(root, self.toggle_running)
        self.stats_section = StatsSection(root, self.reset_stats)
        self.footer = Footer(root)

        # Mode buttons placeholder (implement if needed)
        # e.g., self.remove_mode_btn = ...
        #       self.keep_mode_btn = ...

        self.file_var = tk.StringVar()
        self.file_dropdown = ttk.Combobox(root, textvariable=self.file_var, state="readonly")
        self.file_dropdown.pack(padx=20, pady=(0, 20), fill="x")
        self.file_dropdown.bind("<<ComboboxSelected>>", lambda e: self.save_and_update())

        # Buttons to open config or create new
        btn_frame = tk.Frame(root, bg=COLORS['bg_primary'])
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        ttk.Button(btn_frame, text="Open Config Folder", command=self.open_config_folder, style="Modern.TButton").pack(side="left")
        ttk.Button(btn_frame, text="Open Selected Config", command=self.open_selected_config, style="Modern.TButton").pack(side="left", padx=10)
        ttk.Button(btn_frame, text="New Config", command=self.open_new_config_popup, style="Modern.TButton").pack(side="right")

        self.load_filter_files()
        self.update_ui()

    def open_new_config_popup(self):
        NewConfigPopup(self.root, self.on_new_config_created)

    def on_new_config_created(self, filename):
        self.load_filter_files()
        self.file_var.set(filename)
        self.save_and_update()

    def open_selected_config(self):
        filename = self.file_var.get()
        if not filename:
            messagebox.showwarning("Warning", "No config file selected!")
            return
        filepath = os.path.join(FILTERS_FOLDER, filename)
        if not os.path.exists(filepath):
            messagebox.showerror("Error", "Selected config file does not exist!")
            return
        open_file(filepath)

    def open_config_folder(self):
        open_folder(FILTERS_FOLDER)

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

    def save_and_update(self):
        self.config["selected_file"] = self.file_var.get()
        # save_config(self.config) # Implement saving config to disk if you want
        self.update_ui()

    def reset_stats(self):
        self.processed_count = 0
        self.stats_section.update_stats(self.processed_count)

    def update_ui(self):
        status_text = "ONLINE" if self.running else "OFFLINE"
        self.root.title(f"ClipperTool - {status_text}")

        self.control_section.set_running(self.running)
        self.stats_section.update_stats(self.processed_count)

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
                    # Clean text logic here:
                    cleaned = self.clean_clipboard(text)
                    if cleaned != text:
                        pyperclip.copy(cleaned)
                        self.processed_count += 1
                        self.root.after(0, lambda: self.stats_section.update_stats(self.processed_count))
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.5)

    def clean_clipboard(self, text):
        filename = self.file_var.get()
        filepath = os.path.join(FILTERS_FOLDER, filename)
        if not os.path.exists(filepath):
            return text
        try:
            with open(filepath, "r") as f:
                keywords = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
        except Exception as e:
            print(f"Failed reading keywords: {e}")
            keywords = []

        # Placeholder for your cleaning logic:
        # For example, remove keywords if mode is "remove"
        # or keep only keywords if mode is "keep".
        # Here we just return the original text.
        return text
