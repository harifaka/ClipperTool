"""
Main window UI for ClipperTool
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
import subprocess
import platform
import os

from src.ui.constants import COLORS, FONTS, WINDOW_CONFIG
from src.ui.widgets import GoldenButton, StatusIndicator
from src.ui.popups import CreateConfigDialog, show_error_message, show_warning_message
from src.config.config_manager import ConfigManager
from src.core.clipboard_processor import ClipboardProcessor


class ClipperToolUI:
    """Main application UI class"""

    def __init__(self, root):
        self.root = root
        self.config_manager = ConfigManager()
        self.clipboard_processor = ClipboardProcessor(self.config_manager)

        # Load configuration
        self.config = self.config_manager.load_config()

        # Initialize UI
        self._setup_window()
        self._setup_styles()
        self._setup_callbacks()
        self._create_ui()
        self._load_filter_files()
        self._update_ui()

    def _setup_window(self):
        """Configure the main window"""
        self.root.geometry(WINDOW_CONFIG['geometry'])
        self.root.minsize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
        self.root.configure(bg=COLORS['bg_primary'])

    def _setup_styles(self):
        """Configure UI styles"""
        # Initialize with dark theme
        self.style = tb.Style("cyborg")

        # Configure custom styles
        self.style.configure("Card.TFrame", background=COLORS['bg_card'])
        self.style.configure("Main.TFrame", background=COLORS['bg_primary'])

        # Modern labels
        self.style.configure(
            "Title.TLabel",
            background=COLORS['bg_primary'],
            foreground=COLORS['text_primary'],
            font=FONTS['title']
        )

        self.style.configure(
            "Subtitle.TLabel",
            background=COLORS['bg_card'],
            foreground=COLORS['text_secondary'],
            font=FONTS['body']
        )

        self.style.configure(
            "Header.TLabel",
            background=COLORS['bg_card'],
            foreground=COLORS['accent_gold'],
            font=FONTS['header']
        )

        # Modern combobox
        self.style.configure(
            "Modern.TCombobox",
            fieldbackground=COLORS['bg_secondary'],
            background=COLORS['bg_secondary'],
            foreground=COLORS['text_primary'],
            borderwidth=1,
            relief="solid",
            font=FONTS['body']
        )

        # Modern buttons
        self.style.configure(
            "Modern.TButton",
            background=COLORS['bg_secondary'],
            foreground=COLORS['text_primary'],
            borderwidth=1,
            focuscolor="none",
            font=FONTS['button']
        )

    def _setup_callbacks(self):
        """Setup callbacks for clipboard processor"""
        self.clipboard_processor.set_callbacks(
            on_processed=self._on_clipboard_processed,
            on_error=self._on_clipboard_error
        )

    def _create_ui(self):
        """Create the main UI"""
        # Main container
        main_container = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=25, pady=25)

        # Create sections
        self._create_header(main_container)
        self._create_config_section(main_container)
        self._create_mode_section(main_container)
        self._create_control_section(main_container)
        self._create_stats_section(main_container)
        self._create_footer(main_container)

    def _create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        header_frame.pack(fill="x", pady=(0, 30))

        # Title
        title_label = tk.Label(
            header_frame,
            text="◢ CLIPPERTOOL ◣",
            font=FONTS['title'],
            bg=COLORS['bg_primary'],
            fg=COLORS['accent_gold']
        )
        title_label.pack(side="left")

        # Status indicator
        self.status_indicator = StatusIndicator(header_frame)
        self.status_indicator.pack(side="right")

    def _create_config_section(self, parent):
        """Create configuration section"""
        config_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        config_card.pack(fill="x", pady=(0, 20), padx=2)

        # Header
        header_frame = tk.Frame(config_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ CONFIGURATION MATRIX",
            font=FONTS['header'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        # Content
        content_frame = tk.Frame(config_card, bg=COLORS['bg_card'])
        content_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Label(
            content_frame,
            text="Select Filter Configuration:",
            font=FONTS['button'],
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
        self.file_dropdown.bind("<<ComboboxSelected>>", lambda e: self._save_and_update())

        # Action buttons
        self._create_config_buttons(content_frame)

    def _create_config_buttons(self, parent):
        """Create configuration action buttons"""
        button_container = tk.Frame(parent, bg=COLORS['bg_card'])
        button_container.pack(fill="x")

        ttk.Button(
            button_container,
            text="+ New Config",
            command=self._create_new_config,
            style="Modern.TButton"
        ).pack(side="left", padx=(0, 10), fill="x", expand=True)

        ttk.Button(
            button_container,
            text="⚙ Edit Config",
            command=self._open_selected_config,
            style="Modern.TButton"
        ).pack(side="left", padx=(5, 10), fill="x", expand=True)

        ttk.Button(
            button_container,
            text="📁 Open Folder",
            command=self._open_config_folder,
            style="Modern.TButton"
        ).pack(side="left", padx=(5, 0), fill="x", expand=True)

    def _create_mode_section(self, parent):
        """Create mode selection section"""
        mode_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        mode_card.pack(fill="x", pady=(0, 20), padx=2)

        # Header
        header_frame = tk.Frame(mode_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ PROCESSING MODE",
            font=FONTS['header'],
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
            command=lambda: self._set_mode("remove"),
            icon="⊗"
        )
        self.remove_mode_btn.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.keep_mode_btn = GoldenButton(
            button_frame,
            text="KEEP LINES",
            command=lambda: self._set_mode("keep"),
            icon="⊕"
        )
        self.keep_mode_btn.pack(side="left", fill="both", expand=True, padx=(10, 0))

    def _create_control_section(self, parent):
        """Create control section"""
        control_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        control_card.pack(fill="x", pady=(0, 20), padx=2)

        # Header
        header_frame = tk.Frame(control_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ SYSTEM CONTROL",
            font=FONTS['header'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        # Control content
        control_content = tk.Frame(control_card, bg=COLORS['bg_card'])
        control_content.pack(fill="x", padx=20, pady=(0, 20))

        # Main control button
        self.start_stop_button = tk.Button(
            control_content,
            command=self._toggle_processing,
            font=FONTS['button_main'],
            relief="raised",
            bd=3,
            cursor="hand2"
        )
        self.start_stop_button.pack(fill="x", ipady=20, pady=10)

    def _create_stats_section(self, parent):
        """Create statistics section"""
        stats_card = tk.Frame(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        stats_card.pack(fill="x", pady=(0, 20), padx=2)

        # Header
        header_frame = tk.Frame(stats_card, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ SYSTEM METRICS",
            font=FONTS['header'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        # Stats content
        stats_frame = tk.Frame(stats_card, bg=COLORS['bg_card'])
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.processed_label = tk.Label(
            stats_frame,
            text="PROCESSED: 0 ITEMS",
            font=FONTS['body'] + ("bold",),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_blue']
        )
        self.processed_label.pack(side="left")

        ttk.Button(
            stats_frame,
            text="Reset Counter",
            command=self._reset_stats,
            style="Modern.TButton"
        ).pack(side="right")

    def _create_footer(self, parent):
        """Create footer section"""
        footer_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        footer_frame.pack(fill="x", side="bottom", pady=(20, 0))

        tk.Label(
            footer_frame,
            text="◢ ClipperTool - Advanced Clipboard Processing System ◣",
            font=FONTS['footer'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_secondary']
        ).pack()

    # Event handlers
    def _create_new_config(self):
        """Handle create new config button"""
        dialog = CreateConfigDialog(
            self.root,
            self.config_manager,
            self._on_config_created
        )
        dialog.show()

    def _on_config_created(self, filename):
        """Handle successful config creation"""
        self._load_filter_files()
        if not filename.endswith(".txt"):
            filename += ".txt"
        self.file_var.set(filename)
        self._save_and_update()

    def _open_selected_config(self):
        """Open selected config file in default editor"""
        filename = self.file_var.get()
        if not filename:
            show_warning_message("Warning", "No config file selected!")
            return

        filepath = self.config_manager.get_filter_file_path(filename)
        if not os.path.exists(filepath):
            show_error_message("Error", "Selected config file does not exist!")
            return

        try:
            if platform.system() == "Windows":
                os.startfile(filepath)
            elif platform.system() == "Darwin":
                subprocess.call(["open", filepath])
            else:
                subprocess.call(["xdg-open", filepath])
        except Exception as e:
            show_error_message("Error", f"Could not open file:\n{e}")

    def _open_config_folder(self):
        """Open config folder in file explorer"""
        try:
            folder_path = self.config_manager.get_filters_folder()
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", folder_path])
            else:
                subprocess.call(["xdg-open", folder_path])
        except Exception as e:
            show_error_message("Error", f"Could not open folder:\n{e}")

    def _set_mode(self, mode):
        """Set processing mode"""
        self.config["mode"] = mode
        self._save_and_update()

    def _toggle_processing(self):
        """Toggle clipboard processing on/off"""
        if self.clipboard_processor.running:
            self.clipboard_processor.stop_processing()
        else:
            if not self.file_var.get():
                show_warning_message("Warning", "Please select a configuration file first!")
                return
            self.clipboard_processor.start_processing(self.config)

        self._update_ui()

    def _reset_stats(self):
        """Reset processing statistics"""
        self.clipboard_processor.reset_stats()
        self._update_stats()

    def _load_filter_files(self):
        """Load available filter files"""
        files = self.config_manager.get_filter_files()
        self.file_dropdown['values'] = files

        selected_file = self.config.get("selected_file", "")

        if selected_file in files:
            self.file_var.set(selected_file)
        elif files:
            self.file_var.set(files[0])
        else:
            self.file_var.set("")

        self._update_ui()

    def _save_and_update(self):
        """Save configuration and update UI"""
        self.config["selected_file"] = self.file_var.get()
        self.config_manager.save_config(self.config)
        self._update_ui()

    def _update_ui(self):
        """Update UI elements"""
        mode = self.config.get("mode", "remove")
        running = self.clipboard_processor.running

        # Update window title
        status_text = "ONLINE" if running else "OFFLINE"
        self.root.title(f"ClipperTool - {mode.upper()} MODE [{status_text}]")

        # Update status indicator
        self.status_indicator.set_status(running)

        # Update main control button
        if running:
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

        # Update stats
        self._update_stats()

    def _update_stats(self):
        """Update statistics display"""
        count = self.clipboard_processor.get_processed_count()
        self.processed_label.configure(text=f"PROCESSED: {count} ITEMS")

    # Callbacks for clipboard processor
    def _on_clipboard_processed(self, count):
        """Handle clipboard processing event"""
        self.root.after(0, self._update_stats)

    def _on_clipboard_error(self, error_msg):
        """Handle clipboard processing error"""
        print(f"Clipboard processing error: {error_msg}")
        # Could show error in UI if desired