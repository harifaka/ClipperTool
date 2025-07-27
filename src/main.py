import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import os
import json
import threading
import time
import pyperclip
import ttkbootstrap as tb
import sys
import subprocess
import platform

CONFIG_DIR = os.path.join(os.path.expanduser("~"), "Documents", "ClipperTool")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
FILTERS_FOLDER = os.path.join(CONFIG_DIR, "Configs")

os.makedirs(FILTERS_FOLDER, exist_ok=True)

# Modern high-tech color scheme
COLORS = {
    'bg_primary': '#0f0f0f',
    'bg_secondary': '#1a1a1a',
    'bg_card': '#252525',
    'accent_gold': '#d4af37',
    'accent_gold_hover': '#f4cf47',
    'accent_blue': '#00d4ff',
    'accent_green': '#00ff88',
    'accent_red': '#ff4757',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'border': '#333333',
    'success': '#00ff88',
    'danger': '#ff4757',
    'warning': '#ffa726'
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


class GoldenButton(tk.Frame):
    def __init__(self, parent, text, command, icon="", active=False, **kwargs):
        super().__init__(parent, bg=COLORS['bg_card'], **kwargs)
        self.command = command
        self.active = active
        self.icon = icon
        self.text = text

        # Create canvas for custom drawing
        self.canvas = tk.Canvas(
            self,
            height=50,
            bg=COLORS['bg_card'],
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        # Bind events
        self.canvas.bind("<Button-1>", lambda e: self.command())
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)

        # Initial draw
        self.draw_button()

    def draw_button(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width() or 200
        height = self.canvas.winfo_height() or 50

        if width <= 1 or height <= 1:
            self.after(10, self.draw_button)
            return

        # Golden frame colors
        if self.active:
            frame_color = COLORS['accent_gold']
            bg_color = COLORS['bg_secondary']
            text_color = COLORS['accent_gold']
        else:
            frame_color = COLORS['border']
            bg_color = COLORS['bg_card']
            text_color = COLORS['text_secondary']

        # Draw futuristic frame
        points = [
            10, 5,  # Top left
            width - 10, 5,  # Top right
            width - 5, 10,  # Top right corner
            width - 5, height - 10,  # Bottom right
            width - 10, height - 5,  # Bottom right corner
            10, height - 5,  # Bottom left
            5, height - 10,  # Bottom left corner
            5, 10  # Top left corner
        ]

        # Background
        self.canvas.create_polygon(points, fill=bg_color, outline=frame_color, width=2)

        # Inner glow effect for active state
        if self.active:
            inner_points = [
                12, 7,
                width - 12, 7,
                width - 7, 12,
                width - 7, height - 12,
                width - 12, height - 7,
                12, height - 7,
                7, height - 12,
                7, 12
            ]
            self.canvas.create_polygon(inner_points, fill="", outline=COLORS['accent_gold'], width=1)

        # Text
        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.canvas.create_text(
            width / 2, height / 2,
            text=display_text,
            fill=text_color,
            font=("Consolas", 11, "bold"),
            anchor="center"
        )

    def on_enter(self, event):
        if not self.active:
            self.canvas.configure(cursor="hand2")
            # Redraw with hover effect
            self.draw_hover_effect()

    def on_leave(self, event):
        self.draw_button()

    def draw_hover_effect(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Hover effect
        frame_color = COLORS['accent_gold'] if not self.active else COLORS['accent_gold_hover']
        bg_color = COLORS['bg_secondary']
        text_color = COLORS['accent_gold_hover']

        points = [
            10, 5, width - 10, 5, width - 5, 10, width - 5, height - 10,
                   width - 10, height - 5, 10, height - 5, 5, height - 10, 5, 10
        ]

        self.canvas.create_polygon(points, fill=bg_color, outline=frame_color, width=2)

        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.canvas.create_text(
            width / 2, height / 2,
            text=display_text,
            fill=text_color,
            font=("Consolas", 11, "bold"),
            anchor="center"
        )

    def set_active(self, active):
        self.active = active
        self.draw_button()


class StatusIndicator(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg_card'], **kwargs)

        # Status canvas for animated indicator
        self.status_canvas = tk.Canvas(
            self,
            width=16,
            height=16,
            bg=COLORS['bg_card'],
            highlightthickness=0
        )
        self.status_canvas.pack(side="left", padx=(0, 12))

        # Status text
        self.status_label = tk.Label(
            self,
            text="OFFLINE",
            font=("Consolas", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        )
        self.status_label.pack(side="left")

        self.running = False
        self.animation_step = 0
        self.set_status(False)

    def set_status(self, running):
        self.running = running
        if running:
            self.status_label.configure(
                text="ONLINE",
                fg=COLORS['success']
            )
            self.animate_indicator()
        else:
            self.status_label.configure(
                text="OFFLINE",
                fg=COLORS['text_secondary']
            )
            self.draw_static_indicator()

    def draw_static_indicator(self):
        self.status_canvas.delete("all")
        color = COLORS['success'] if self.running else COLORS['text_secondary']
        self.status_canvas.create_oval(2, 2, 14, 14, fill=color, outline=color)

    def animate_indicator(self):
        if not self.running:
            return

        self.status_canvas.delete("all")

        # Pulsing effect
        base_size = 4
        pulse_size = int(2 + 2 * abs(0.5 - (self.animation_step % 60) / 60))

        # Outer ring
        self.status_canvas.create_oval(
            8 - base_size - pulse_size, 8 - base_size - pulse_size,
            8 + base_size + pulse_size, 8 + base_size + pulse_size,
            outline=COLORS['success'],
            width=1
        )

        # Inner dot
        self.status_canvas.create_oval(
            8 - base_size, 8 - base_size,
            8 + base_size, 8 + base_size,
            fill=COLORS['success'],
            outline=COLORS['success']
        )

        self.animation_step += 1
        self.after(50, self.animate_indicator)


class ClipperTool:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x650")
        self.root.minsize(700, 600)
        self.root.configure(bg=COLORS['bg_primary'])

        # Initialize with dark theme
        self.style = tb.Style("cyborg")

        self.config = load_config()
        self.running = False
        self.last_clipboard = None
        self.processed_count = 0

        self.setup_styles()
        self.create_modern_ui()
        self.load_filter_files()
        self.update_ui()

    def setup_styles(self):
        """Configure modern high-tech styles"""
        self.style.configure("Card.TFrame", background=COLORS['bg_card'])
        self.style.configure("Main.TFrame", background=COLORS['bg_primary'])

        # Modern labels
        self.style.configure(
            "Title.TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['text_primary'],
            font=("Consolas", 28, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            background=COLORS['bg_card'],
            foreground=COLORS['text_secondary'],
            font=("Consolas", 11)
        )

        self.style.configure(
            "Header.TLabel",
            background=COLORS['bg_card'],
            foreground=COLORS['accent_gold'],
            font=("Consolas", 12, "bold")
        )

        # Modern combobox
        self.style.configure(
            "Modern.TCombobox",
            fieldbackground=COLORS['bg_secondary'],
            background=COLORS['bg_secondary'],
            foreground=COLORS['text_primary'],
            borderwidth=1,
            relief="solid",
            font=("Consolas", 11)
        )

        # Modern buttons
        self.style.configure(
            "Modern.TButton",
            background=COLORS['bg_secondary'],
            foreground=COLORS['text_primary'],
            borderwidth=1,
            focuscolor="none",
            font=("Consolas", 10)
        )

        # Main action button
        self.style.configure(
            "Action.TButton",
            background=COLORS['success'],
            foreground=COLORS['bg_primary'],
            borderwidth=0,
            focuscolor="none",
            font=("Consolas", 14, "bold")
        )

    def create_modern_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=25, pady=25)

        # Header section
        self.create_header(main_container)

        # Configuration section
        self.create_config_section(main_container)

        # Mode selection section
        self.create_mode_section(main_container)

        # Control section
        self.create_control_section(main_container)

        # Stats section
        self.create_stats_section(main_container)

        # Footer
        self.create_footer(main_container)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill="x", pady=(0, 30))

        # Title with tech styling
        title_label = tk.Label(
            header_frame,
            text="◢ CLIPPERTOOL ◣",
            font=("Consolas", 24, "bold"),
            bg=COLORS['bg_primary'],
            fg=COLORS['accent_gold']
        )
        title_label.pack(side="left")

        # Status indicator
        self.status_indicator = StatusIndicator(header_frame)
        self.status_indicator.pack(side="right")

    def create_config_section(self, parent):
        # Configuration card
        config_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        config_card.pack(fill="x", pady=(0, 20), padx=2)

        # Card header
        header_frame = tk.Frame(config_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ CONFIGURATION MATRIX",
            font=("Consolas", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        # Config content
        content_frame = tk.Frame(config_card, bg=COLORS['bg_card'])
        content_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Label(
            content_frame,
            text="Select Filter Configuration:",
            font=("Consolas", 10),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(anchor="w", pady=(0, 8))

        self.file_var = tk.StringVar()
        self.file_dropdown = ttk.Combobox(
            content_frame,
            textvariable=self.file_var,
            state="readonly",
            style="Modern.TCombobox"
        )
        self.file_dropdown.pack(fill="x", pady=(0, 15), ipady=8)
        self.file_dropdown.bind("<<ComboboxSelected>>", lambda e: self.save_and_update())

        # Action buttons
        button_container = tk.Frame(content_frame, bg=COLORS['bg_card'])
        button_container.pack(fill="x")

        ttk.Button(
            button_container,
            text="+ New Config",
            command=self.create_new_config,
            style="Modern.TButton"
        ).pack(side="left", padx=(0, 10), fill="x", expand=True)

        ttk.Button(
            button_container,
            text="⚙ Edit Config",
            command=self.open_selected_config,
            style="Modern.TButton"
        ).pack(side="left", padx=(5, 10), fill="x", expand=True)

        ttk.Button(
            button_container,
            text="📁 Open Folder",
            command=self.open_config_folder,
            style="Modern.TButton"
        ).pack(side="left", padx=(5, 0), fill="x", expand=True)

    def create_mode_section(self, parent):
        # Mode selection card
        mode_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        mode_card.pack(fill="x", pady=(0, 20), padx=2)

        # Card header
        header_frame = tk.Frame(mode_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ PROCESSING MODE",
            font=("Consolas", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        # Mode buttons
        mode_frame = tk.Frame(mode_card, bg=COLORS['bg_card'])
        mode_frame.pack(fill="x", padx=20, pady=(0, 20))

        button_frame = tk.Frame(mode_frame, bg=COLORS['bg_card'])
        button_frame.pack(fill="x")

        self.remove_mode_btn = GoldenButton(
            button_frame,
            text="REMOVE LINES",
            command=lambda: self.set_mode("remove"),
            icon="⊗"
        )
        self.remove_mode_btn.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.keep_mode_btn = GoldenButton(
            button_frame,
            text="KEEP LINES",
            command=lambda: self.set_mode("keep"),
            icon="⊕"
        )
        self.keep_mode_btn.pack(side="left", fill="both", expand=True, padx=(10, 0))

    def create_control_section(self, parent):
        # Control card
        control_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        control_card.pack(fill="x", pady=(0, 20), padx=2)

        # Card header
        header_frame = tk.Frame(control_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ SYSTEM CONTROL",
            font=("Consolas", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        # Control content
        control_content = tk.Frame(control_card, bg=COLORS['bg_card'])
        control_content.pack(fill="x", padx=20, pady=(0, 20))

        # Main control button with enhanced visibility
        self.start_stop_button = tk.Button(
            control_content,
            command=self.toggle_running,
            font=("Consolas", 16, "bold"),
            relief="raised",
            bd=3,
            cursor="hand2"
        )
        self.start_stop_button.pack(fill="x", ipady=20, pady=10)

    def create_stats_section(self, parent):
        # Statistics card
        stats_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        stats_card.pack(fill="x", pady=(0, 20), padx=2)

        # Card header
        header_frame = tk.Frame(stats_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ SYSTEM METRICS",
            font=("Consolas", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        # Stats content
        stats_frame = tk.Frame(stats_card, bg=COLORS['bg_card'])
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.processed_label = tk.Label(
            stats_frame,
            text="PROCESSED: 0 ITEMS",
            font=("Consolas", 11, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_blue']
        )
        self.processed_label.pack(side="left")

        ttk.Button(
            stats_frame,
            text="Reset Counter",
            command=self.reset_stats,
            style="Modern.TButton"
        ).pack(side="right")

    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        footer_frame.pack(fill="x", side="bottom", pady=(20, 0))

        tk.Label(
            footer_frame,
            text="◢ ClipperTool - Advanced Clipboard Processing System ◣",
            font=("Consolas", 9),
            bg=COLORS['bg_primary'],
            fg=COLORS['text_secondary']
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
        popup.geometry("450x250")
        popup.resizable(False, False)
        popup.configure(bg=COLORS['bg_primary'])

        popup.transient(self.root)
        popup.grab_set()

        main_frame = tk.Frame(popup, bg=COLORS['bg_card'], relief="raised", bd=2)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            main_frame,
            text="▼ NEW CONFIGURATION",
            font=("Consolas", 14, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(pady=(20, 20))

        tk.Label(
            main_frame,
            text="Configuration Name:",
            font=("Consolas", 11),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(anchor="w", padx=20)

        entry = tk.Entry(
            main_frame,
            font=("Consolas", 12),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['text_primary'],
            relief="solid",
            bd=1
        )
        entry.pack(fill="x", padx=20, pady=(5, 20), ipady=8)
        entry.focus()

        button_frame = tk.Frame(main_frame, bg=COLORS['bg_card'])
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy,
            style="Modern.TButton"
        ).pack(side="right", padx=(10, 0))

        ttk.Button(
            button_frame,
            text="Create",
            command=on_submit,
            style="Modern.TButton"
        ).pack(side="right")

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
        self.processed_label.configure(text=f"PROCESSED: {self.processed_count} ITEMS")

    def update_ui(self):
        mode = self.config.get("mode", "remove")

        # Update window title
        status_text = "ONLINE" if self.running else "OFFLINE"
        self.root.title(f"ClipperTool - {mode.upper()} MODE [{status_text}]")

        # Update status indicator
        self.status_indicator.set_status(self.running)

        # Update main control button with enhanced visibility
        if self.running:
            self.start_stop_button.configure(
                text="◼ STOP PROCESSING",
                bg=COLORS['danger'],
                fg=COLORS['text_primary'],
                activebackground=COLORS['accent_red']
            )
        else:
            self.start_stop_button.configure(
                text="▶ START PROCESSING",
                bg=COLORS['success'],
                fg=COLORS['bg_primary'],
                activebackground=COLORS['accent_green']
            )

        # Update mode buttons
        self.remove_mode_btn.set_active(mode == "remove")
        self.keep_mode_btn.set_active(mode == "keep")

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
    app.title("ClipperTool")

    # Try to set the icon
    try:
        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            app.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not load icon: {e}")

    ClipperTool(app)
    app.mainloop()
