import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import os
import json
import threading
import time
import pyperclip
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sys
import subprocess
import platform

CONFIG_DIR = os.path.join(os.path.expanduser("~"), "Documents", "ClipperTool")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
FILTERS_FOLDER = os.path.join(CONFIG_DIR, "Configs")

os.makedirs(FILTERS_FOLDER, exist_ok=True)

# Modern color scheme
COLORS = {
    'primary': '#2563eb',
    'primary_hover': '#1d4ed8',
    'secondary': '#64748b',
    'success': '#10b981',
    'success_hover': '#059669',
    'danger': '#ef4444',
    'danger_hover': '#dc2626',
    'warning': '#f59e0b',
    'dark': '#1e293b',
    'light': '#f8fafc',
    'border': '#e2e8f0',
    'text_primary': '#0f172a',
    'text_secondary': '#64748b'
}


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
        base_path = sys._MEIPASS
    except Exception:
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


class ModernButton(ttk.Frame):
    def __init__(self, parent, text, command, style_type="primary", **kwargs):
        super().__init__(parent, **kwargs)
        self.command = command
        self.style_type = style_type

        # Create the button with modern styling
        self.button = ttk.Button(
            self,
            text=text,
            command=command,
            style=f"{style_type.title()}.TButton"
        )
        self.button.pack(fill="both", expand=True)


class StatusIndicator(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Status dot
        self.status_canvas = tk.Canvas(self, width=12, height=12, highlightthickness=0)
        self.status_canvas.pack(side="left", padx=(0, 8))

        # Status text
        self.status_label = ttk.Label(self, text="Stopped", font=("Segoe UI", 9, "bold"))
        self.status_label.pack(side="left")

        self.set_status(False)

    def set_status(self, running):
        self.status_canvas.delete("all")
        color = COLORS['success'] if running else COLORS['secondary']
        self.status_canvas.create_oval(2, 2, 10, 10, fill=color, outline=color)
        self.status_label.configure(text="Running" if running else "Stopped")


class ClipperTool:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x550")
        self.root.minsize(600, 500)

        # Initialize with dark theme
        self.style = tb.Style("superhero")

        self.config = load_config()
        self.running = False
        self.last_clipboard = None
        self.processed_count = 0

        self.setup_styles()
        self.create_modern_ui()
        self.load_filter_files()
        self.update_ui()

    def setup_styles(self):
        """Configure modern button and widget styles"""
        # Primary button style
        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focuscolor="none",
            relief="flat"
        )

        # Success button style
        self.style.configure(
            "Success.TButton",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focuscolor="none",
            relief="flat"
        )

        # Danger button style
        self.style.configure(
            "Danger.TButton",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focuscolor="none",
            relief="flat"
        )

        # Modern combobox style
        self.style.configure(
            "Modern.TCombobox",
            fieldbackground="white",
            borderwidth=1,
            relief="solid"
        )

    def create_modern_ui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header section
        self.create_header(main_container)

        # Configuration section
        self.create_config_section(main_container)

        # Control section
        self.create_control_section(main_container)

        # Stats section
        self.create_stats_section(main_container)

        # Footer
        self.create_footer(main_container)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 30))

        # Title
        title_label = ttk.Label(
            header_frame,
            text="ClipperTool Pro",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(side="left")

        # Mode indicator
        self.mode_frame = ttk.Frame(header_frame)
        self.mode_frame.pack(side="right")

        self.mode_label = ttk.Label(
            self.mode_frame,
            text="REMOVE MODE",
            font=("Segoe UI", 10, "bold"),
            foreground="white"
        )
        self.mode_label.pack(padx=12, pady=6)

    def create_config_section(self, parent):
        # Configuration card
        config_card = ttk.LabelFrame(parent, text="Configuration", padding=20)
        config_card.pack(fill="x", pady=(0, 20))

        # Config file selection
        config_label = ttk.Label(config_card, text="Select Configuration File:", font=("Segoe UI", 10, "bold"))
        config_label.pack(anchor="w", pady=(0, 8))

        self.file_var = tk.StringVar()
        self.file_dropdown = ttk.Combobox(
            config_card,
            textvariable=self.file_var,
            state="readonly",
            font=("Segoe UI", 10),
            style="Modern.TCombobox"
        )
        self.file_dropdown.pack(fill="x", pady=(0, 15))
        self.file_dropdown.bind("<<ComboboxSelected>>", lambda e: self.save_and_update())

        # Action buttons
        button_container = ttk.Frame(config_card)
        button_container.pack(fill="x")

        # New config button
        new_btn = ttk.Button(
            button_container,
            text="✚ New Config",
            command=self.create_new_config,
            style="Primary.TButton"
        )
        new_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # Edit config button
        edit_btn = ttk.Button(
            button_container,
            text="✏ Edit Config",
            command=self.open_selected_config,
            style="Success.TButton"
        )
        edit_btn.pack(side="left", padx=(5, 10), fill="x", expand=True)

        # Open folder button
        folder_btn = ttk.Button(
            button_container,
            text="📁 Open Folder",
            command=self.open_config_folder,
            style="Secondary.TButton"
        )
        folder_btn.pack(side="left", padx=(5, 0), fill="x", expand=True)

    def create_control_section(self, parent):
        # Control card
        control_card = ttk.LabelFrame(parent, text="Control Panel", padding=20)
        control_card.pack(fill="x", pady=(0, 20))

        # Status indicator
        status_frame = ttk.Frame(control_card)
        status_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(status_frame, text="Status:", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.status_indicator = StatusIndicator(status_frame)
        self.status_indicator.pack(side="left", padx=(10, 0))

        # Main control button
        self.start_stop_button = ttk.Button(
            control_card,
            command=self.toggle_running,
            style="Success.TButton"
        )
        self.start_stop_button.pack(fill="x", ipady=12)

        # Mode toggle buttons
        mode_frame = ttk.Frame(control_card)
        mode_frame.pack(fill="x", pady=(15, 0))

        ttk.Label(mode_frame, text="Processing Mode:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 8))

        mode_buttons = ttk.Frame(mode_frame)
        mode_buttons.pack(fill="x")

        self.remove_mode_btn = ttk.Button(
            mode_buttons,
            text="🗑 Remove Lines",
            command=lambda: self.set_mode("remove"),
            style="Danger.TButton"
        )
        self.remove_mode_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.keep_mode_btn = ttk.Button(
            mode_buttons,
            text="✓ Keep Lines",
            command=lambda: self.set_mode("keep"),
            style="Success.TButton"
        )
        self.keep_mode_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))

    def create_stats_section(self, parent):
        # Statistics card
        stats_card = ttk.LabelFrame(parent, text="Statistics", padding=20)
        stats_card.pack(fill="x", pady=(0, 20))

        stats_frame = ttk.Frame(stats_card)
        stats_frame.pack(fill="x")

        # Processed count
        self.processed_label = ttk.Label(
            stats_frame,
            text="Processed: 0 items",
            font=("Segoe UI", 10)
        )
        self.processed_label.pack(side="left")

        # Reset button
        reset_btn = ttk.Button(
            stats_frame,
            text="Reset Counter",
            command=self.reset_stats,
            style="Secondary.TButton"
        )
        reset_btn.pack(side="right")

    def create_footer(self, parent):
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill="x", side="bottom")

        ttk.Label(
            footer_frame,
            text="ClipperTool Pro - Advanced Clipboard Processing",
            font=("Segoe UI", 8),
            foreground=COLORS['text_secondary']
        ).pack()

    def create_new_config(self):
        def on_submit():
            filename = entry.get().strip()
            if not filename:
                return
            if not filename.endswith(".txt"):
                filename += ".txt"
            filepath = os.path.join(FILTERS_FOLDER, filename)
            if os.path.exists(filepath):
                tk.messagebox.showerror("Error", "File already exists!")
                return
            try:
                with open(filepath, "w") as f:
                    f.write("# Add your keywords here, one per line\n")
                popup.destroy()
                self.load_filter_files()
                self.file_var.set(filename)
                self.save_and_update()
                tk.messagebox.showinfo("Success", f"Config file '{filename}' created successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not create file:\n{e}")

        # Modern popup dialog
        popup = tk.Toplevel(self.root)
        popup.title("Create New Configuration")
        popup.geometry("400x200")
        popup.resizable(False, False)

        # Center the popup
        popup.transient(self.root)
        popup.grab_set()

        main_frame = ttk.Frame(popup, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Configuration Name:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        entry = ttk.Entry(main_frame, font=("Segoe UI", 11))
        entry.pack(fill="x", pady=(0, 20), ipady=8)
        entry.focus()

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side="right", padx=(10, 0))
        ttk.Button(button_frame, text="Create", command=on_submit, style="Primary.TButton").pack(side="right")

        # Enter key binding
        entry.bind("<Return>", lambda e: on_submit())

    def open_selected_config(self):
        filename = self.file_var.get()
        if not filename:
            tk.messagebox.showwarning("Warning", "No config file selected!")
            return

        filepath = os.path.join(FILTERS_FOLDER, filename)
        if not os.path.exists(filepath):
            tk.messagebox.showerror("Error", "Selected config file does not exist!")
            return

        try:
            if platform.system() == "Windows":
                os.startfile(filepath)
            elif platform.system() == "Darwin":
                subprocess.call(["open", filepath])
            else:
                subprocess.call(["xdg-open", filepath])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not open file:\n{e}")

    def open_config_folder(self):
        try:
            if platform.system() == "Windows":
                os.startfile(FILTERS_FOLDER)
            elif platform.system() == "Darwin":
                subprocess.call(["open", FILTERS_FOLDER])
            else:
                subprocess.call(["xdg-open", FILTERS_FOLDER])
        except Exception as e:
            tk.messagebox.showerror("Error", f"Could not open folder:\n{e}")

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

    def reset_stats(self):
        self.processed_count = 0
        self.update_stats()

    def update_stats(self):
        self.processed_label.configure(text=f"Processed: {self.processed_count} items")

    def update_ui(self):
        mode = self.config.get("mode", "remove")

        # Update window title
        status_text = "Running" if self.running else "Stopped"
        self.root.title(f"ClipperTool Pro - {mode.title()} Mode ({status_text})")

        # Update mode indicator
        mode_text = "REMOVE MODE" if mode == "remove" else "KEEP MODE"
        mode_color = COLORS['danger'] if mode == "remove" else COLORS['success']

        self.mode_label.configure(text=mode_text)
        self.mode_frame.configure(style="Card.TFrame")

        # Update status indicator
        self.status_indicator.set_status(self.running)

        # Update main control button
        if self.running:
            self.start_stop_button.configure(
                text="⏹ Stop Processing",
                style="Danger.TButton"
            )
        else:
            self.start_stop_button.configure(
                text="▶ Start Processing",
                style="Success.TButton"
            )

        # Update mode buttons
        if mode == "remove":
            self.remove_mode_btn.configure(style="Danger.TButton")
            self.keep_mode_btn.configure(style="Secondary.TButton")
        else:
            self.remove_mode_btn.configure(style="Secondary.TButton")
            self.keep_mode_btn.configure(style="Success.TButton")

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
                        self.processed_count += 1
                        self.root.after(0, self.update_stats)
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.5)

    def clean_clipboard(self, text):
        filename = self.file_var.get()
        filepath = os.path.join(FILTERS_FOLDER, filename)
        if not os.path.exists(filepath):
            return text

        with open(filepath, "r") as f:
            keywords = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

        cleaner = ClipboardCleaner(keywords, self.config["mode"])
        return cleaner.process_text(text)


if __name__ == "__main__":
    app = tk.Tk()

    # Set window properties
    app.title("ClipperTool Pro")

    # Try to set the icon
    try:
        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            app.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not load icon: {e}")

    ClipperTool(app)
    app.mainloop()