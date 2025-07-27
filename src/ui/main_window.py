"""
Main window UI for ClipperTool - Modernized Version
"""

import os
import platform
import subprocess
import tkinter as tk
from tkinter import ttk

import ttkbootstrap as tb

from src.config.config_manager import ConfigManager
from src.core.clipboard_processor import ClipboardProcessor
from src.ui.popups import CreateConfigDialog, show_error_message, show_warning_message
from src.ui.widgets import StatusIndicator
from src.ui.constants import MODERN_COLORS, WINDOW_CONFIG


class ClipperToolUI:
    """Main application UI class - Modernized"""

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

        # Bind resize event for responsive behavior
        self.root.bind('<Configure>', self._on_window_resize)

        # Track window state for responsive adjustments
        self.last_width = 0
        self.last_height = 0

    def _setup_window(self):
        """Configure the main window with better sizing"""
        self.root.geometry(WINDOW_CONFIG['geometry'])
        self.root.minsize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
        self.root.configure(bg=MODERN_COLORS['bg_primary'])

        # Set window icon and title
        self.root.title("ClipperTool - Advanced Clipboard Processing")

        # Make window resizable and responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _setup_styles(self):
        """Configure modern UI styles"""
        # Initialize with dark theme but customize
        self.style = tb.Style("darkly")

        # Override with modern colors
        self.style.configure(
            "Modern.TFrame",
            background=MODERN_COLORS['bg_secondary'],
            relief="flat",
            borderwidth=1,
            bordercolor=MODERN_COLORS['border']
        )

        self.style.configure(
            "Card.TFrame",
            background=MODERN_COLORS['bg_secondary'],
            relief="flat",
            borderwidth=1,
            bordercolor=MODERN_COLORS['border']
        )

        # Modern labels
        self.style.configure(
            "Title.TLabel",
            background=MODERN_COLORS['bg_primary'],
            foreground=MODERN_COLORS['accent_blue'],
            font=('Segoe UI', 18, 'bold')
        )

        self.style.configure(
            "Header.TLabel",
            background=MODERN_COLORS['bg_secondary'],
            foreground=MODERN_COLORS['accent_orange'],
            font=('Segoe UI', 11, 'bold')
        )

        self.style.configure(
            "Body.TLabel",
            background=MODERN_COLORS['bg_secondary'],
            foreground=MODERN_COLORS['text_primary'],
            font=('Segoe UI', 10)
        )

        self.style.configure(
            "Muted.TLabel",
            background=MODERN_COLORS['bg_secondary'],
            foreground=MODERN_COLORS['text_muted'],
            font=('Segoe UI', 9)
        )

        # Modern combobox
        self.style.configure(
            "Modern.TCombobox",
            fieldbackground=MODERN_COLORS['bg_input'],
            background=MODERN_COLORS['bg_input'],
            foreground=MODERN_COLORS['text_primary'],
            borderwidth=1,
            bordercolor=MODERN_COLORS['border'],
            focuscolor=MODERN_COLORS['border_focus'],
            relief="flat",
            font=('Segoe UI', 10)
        )

        # Modern buttons
        self.style.configure(
            "Modern.TButton",
            background=MODERN_COLORS['bg_tertiary'],
            foreground=MODERN_COLORS['text_primary'],
            borderwidth=1,
            bordercolor=MODERN_COLORS['border'],
            focuscolor="none",
            relief="flat",
            font=('Segoe UI', 9),
            padding=(12, 8)
        )

        self.style.map(
            "Modern.TButton",
            background=[('active', MODERN_COLORS['hover']),
                        ('pressed', MODERN_COLORS['active'])]
        )

    def _setup_callbacks(self):
        """Setup callbacks for clipboard processor"""
        self.clipboard_processor.set_callbacks(
            on_processed=self._on_clipboard_processed,
            on_error=self._on_clipboard_error
        )

    def _create_ui(self):
        """Create the modern responsive UI that fits in window"""
        # Main container - no scrolling, everything should fit
        self.main_container = tk.Frame(
            self.root,
            bg=MODERN_COLORS['bg_primary']
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Configure main container grid for proper spacing
        self.main_container.grid_rowconfigure(1, weight=0)  # Header - fixed
        self.main_container.grid_rowconfigure(2, weight=1)  # Config - flexible
        self.main_container.grid_rowconfigure(3, weight=0)  # Mode - compact
        self.main_container.grid_rowconfigure(4, weight=0)  # Control - compact
        self.main_container.grid_rowconfigure(5, weight=0)  # Stats - compact
        self.main_container.grid_rowconfigure(6, weight=0)  # Footer - minimal
        self.main_container.grid_columnconfigure(0, weight=1)

        # Create sections with grid layout for better control
        self._create_header(self.main_container)
        self._create_config_section(self.main_container)
        self._create_mode_section(self.main_container)
        self._create_control_section(self.main_container)
        self._create_stats_section(self.main_container)
        self._create_footer(self.main_container)

    def _on_window_resize(self, event):
        """Handle window resize for responsive behavior"""
        if event.widget != self.root:
            return

        current_width = self.root.winfo_width()
        current_height = self.root.winfo_height()

        # Only update if size actually changed significantly
        if abs(current_width - self.last_width) > 10 or abs(current_height - self.last_height) > 10:

            self.last_width = current_width
            self.last_height = current_height

            # Trigger responsive layout update
            self.root.after(50, self._update_responsive_layout)

    def _update_responsive_layout(self):
        """Update layout based on current window size"""
        width = self.root.winfo_width()

        # Adjust padding based on window width
        if width < 700:
            padx = 15
        elif width < 900:
            padx = 25
        else:
            padx = 35

        # Update main container padding - make it smaller
        self.main_container.configure(padx=padx, pady=15)

    def _create_modern_card(self, parent, title, icon="▼", row=None):
        """Create a modern card container with proper grid placement"""
        # Card container with minimal padding
        card_container = tk.Frame(parent, bg=MODERN_COLORS['bg_primary'])
        if row is not None:
            card_container.grid(row=row, column=0, sticky="ew", pady=(0, 8), padx=2)
        else:
            card_container.pack(fill="x", pady=(0, 8), padx=2)

        # Main card
        card = tk.Frame(
            card_container,
            bg=MODERN_COLORS['bg_secondary'],
            relief="flat",
            bd=0
        )
        card.pack(fill="both", expand=True)

        # Add subtle border
        border_frame = tk.Frame(
            card,
            bg=MODERN_COLORS['border'],
            height=1
        )
        border_frame.pack(fill="x", side="top")

        # Header with icon and title - more compact
        header_frame = tk.Frame(card, bg=MODERN_COLORS['bg_secondary'])
        header_frame.pack(fill="x", padx=15, pady=(12, 8))

        title_label = tk.Label(
            header_frame,
            text=f"{icon} {title}",
            font=('Segoe UI', 10, 'bold'),  # Smaller font
            bg=MODERN_COLORS['bg_secondary'],
            fg=MODERN_COLORS['accent_orange']
        )
        title_label.pack(anchor="w")

        # Content frame - reduced padding
        content_frame = tk.Frame(card, bg=MODERN_COLORS['bg_secondary'])
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        return card, content_frame

    def _create_header(self, parent):
        """Create compact modern header section"""
        header_frame = tk.Frame(parent, bg=MODERN_COLORS['bg_primary'])
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        # Configure grid
        header_frame.grid_columnconfigure(0, weight=1)

        # Left side - Title
        left_frame = tk.Frame(header_frame, bg=MODERN_COLORS['bg_primary'])
        left_frame.grid(row=0, column=0, sticky="w")

        title_label = tk.Label(
            left_frame,
            text="⚡ CLIPPERTOOL",
            font=('Segoe UI', 16, 'bold'),  # Smaller title
            bg=MODERN_COLORS['bg_primary'],
            fg=MODERN_COLORS['accent_blue']
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            left_frame,
            text="Advanced Clipboard Processing System",
            font=('Segoe UI', 8),  # Smaller subtitle
            bg=MODERN_COLORS['bg_primary'],
            fg=MODERN_COLORS['text_muted']
        )
        subtitle_label.pack(anchor="w", pady=(1, 0))

        # Right side - Status
        right_frame = tk.Frame(header_frame, bg=MODERN_COLORS['bg_primary'])
        right_frame.grid(row=0, column=1, sticky="e")

        self.status_indicator = StatusIndicator(right_frame)
        self.status_indicator.pack()

    def _create_config_section(self, parent):
        """Create modern configuration section"""
        card, content = self._create_modern_card(parent, "CONFIGURATION", "⚙", row=1)

        # Configuration label - more compact
        tk.Label(
            content,
            text="Filter Configuration File:",
            font=('Segoe UI', 9),
            bg=MODERN_COLORS['bg_secondary'],
            fg=MODERN_COLORS['text_secondary']
        ).pack(anchor="w", pady=(0, 6))

        # Dropdown container for better styling
        dropdown_container = tk.Frame(content, bg=MODERN_COLORS['bg_secondary'])
        dropdown_container.pack(fill="x", pady=(0, 12))

        self.file_var = tk.StringVar()
        self.file_dropdown = ttk.Combobox(
            dropdown_container,
            textvariable=self.file_var,
            state="readonly",
            style="Modern.TCombobox",
            font=('Segoe UI', 9)  # Smaller font
        )
        self.file_dropdown.pack(fill="x", ipady=6)  # Less padding
        self.file_dropdown.bind("<<ComboboxSelected>>", lambda e: self._save_and_update())

        # Action buttons in responsive grid
        self._create_config_buttons(content)

    def _create_config_buttons(self, parent):
        """Create responsive configuration buttons"""
        button_container = tk.Frame(parent, bg=MODERN_COLORS['bg_secondary'])
        button_container.pack(fill="x")

        # Configure grid weights for responsiveness
        button_container.grid_columnconfigure(0, weight=1)
        button_container.grid_columnconfigure(1, weight=1)
        button_container.grid_columnconfigure(2, weight=1)

        # Modern styled buttons
        new_btn = ttk.Button(
            button_container,
            text="➕ New Config",
            command=self._create_new_config,
            style="Modern.TButton"
        )
        new_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        edit_btn = ttk.Button(
            button_container,
            text="✏ Edit Config",
            command=self._open_selected_config,
            style="Modern.TButton"
        )
        edit_btn.grid(row=0, column=1, padx=4, sticky="ew")

        folder_btn = ttk.Button(
            button_container,
            text="📁 Open Folder",
            command=self._open_config_folder,
            style="Modern.TButton"
        )
        folder_btn.grid(row=0, column=2, padx=(8, 0), sticky="ew")

    def _create_mode_section(self, parent):
        """Create compact mode selection section"""
        card, content = self._create_modern_card(parent, "PROCESSING MODE", "🧩", row=2)

        # Description - more compact
        tk.Label(
            content,
            text="Select how the filter should process clipboard content:",
            font=('Segoe UI', 9),
            bg=MODERN_COLORS['bg_secondary'],
            fg=MODERN_COLORS['text_secondary']
        ).pack(anchor="w", pady=(0, 10))

        # Mode buttons container
        mode_container = tk.Frame(content, bg=MODERN_COLORS['bg_secondary'])
        mode_container.pack(fill="x")
        mode_container.grid_columnconfigure(0, weight=1)
        mode_container.grid_columnconfigure(1, weight=1)

        self.remove_mode_btn = self._create_mode_button(
            mode_container,
            "⚔️ REMOVE LINES",
            "Remove matching lines from clipboard",
            lambda: self._set_mode("remove")
        )
        self.remove_mode_btn.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        self.keep_mode_btn = self._create_mode_button(
            mode_container,
            "📌 KEEP LINES",
            "Keep only matching lines in clipboard",
            lambda: self._set_mode("keep")
        )
        self.keep_mode_btn.grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _create_mode_button(self, parent, text, tooltip, command):
        """Create a compact mode selection button"""
        btn_frame = tk.Frame(parent, bg=MODERN_COLORS['bg_tertiary'], relief="flat", bd=1)

        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            font=('Segoe UI', 9, 'bold'),  # Smaller font
            bg=MODERN_COLORS['bg_tertiary'],
            fg=MODERN_COLORS['text_primary'],
            activebackground=MODERN_COLORS['hover'],
            activeforeground=MODERN_COLORS['text_primary'],
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=10  # Less padding
        )
        btn.pack(fill="both", expand=True)

        return btn_frame

    def _create_control_section(self, parent):
        """Create compact control section"""
        card, content = self._create_modern_card(parent, "SYSTEM CONTROL", "🎮", row=3)

        # Status display - more compact
        self.control_status = tk.Label(
            content,
            text="System is ready. Click below to start processing.",
            font=('Segoe UI', 9),
            bg=MODERN_COLORS['bg_secondary'],
            fg=MODERN_COLORS['text_secondary']
        )
        self.control_status.pack(anchor="w", pady=(0, 10))

        # Main control button - smaller
        self.start_stop_button = tk.Button(
            content,
            command=self._toggle_processing,
            font=('Segoe UI', 12, 'bold'),  # Smaller font
            relief="flat",
            bd=0,
            cursor="hand2",
            height=1  # Reduced height
        )
        self.start_stop_button.pack(fill="x", pady=3)

    def _create_stats_section(self, parent):
        """Create compact statistics section"""
        card, content = self._create_modern_card(parent, "SYSTEM METRICS", "📊", row=4)

        # Stats container
        stats_container = tk.Frame(content, bg=MODERN_COLORS['bg_secondary'])
        stats_container.pack(fill="x")

        # Left side - metrics
        left_stats = tk.Frame(stats_container, bg=MODERN_COLORS['bg_secondary'])
        left_stats.pack(side="left", fill="both", expand=True)

        self.processed_label = tk.Label(
            left_stats,
            text="Processed Items: 0",
            font=('Segoe UI', 10, 'bold'),  # Smaller font
            bg=MODERN_COLORS['bg_secondary'],
            fg=MODERN_COLORS['accent_blue']
        )
        self.processed_label.pack(anchor="w")

        self.status_text_label = tk.Label(
            left_stats,
            text="Status: Idle",
            font=('Segoe UI', 8),  # Smaller font
            bg=MODERN_COLORS['bg_secondary'],
            fg=MODERN_COLORS['text_muted']
        )
        self.status_text_label.pack(anchor="w", pady=(2, 0))

        # Right side - reset button
        reset_btn = ttk.Button(
            stats_container,
            text="🔄 Reset",
            command=self._reset_stats,
            style="Modern.TButton"
        )
        reset_btn.pack(side="right")

    def _create_footer(self, parent):
        """Create minimal footer section"""
        footer_frame = tk.Frame(parent, bg=MODERN_COLORS['bg_primary'])
        footer_frame.grid(row=5, column=0, sticky="ew", pady=(15, 5))

        # Separator line
        separator = tk.Frame(
            footer_frame,
            bg=MODERN_COLORS['border'],
            height=1
        )
        separator.pack(fill="x", pady=(0, 8))

        tk.Label(
            footer_frame,
            text="ClipperTool • Advanced Clipboard Processing System",
            font=('Segoe UI', 6),
            bg=MODERN_COLORS['bg_primary'],
            fg=MODERN_COLORS['text_muted']
        ).pack()

    # Event handlers (keeping existing functionality)
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
        """Set processing mode with visual feedback"""
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
        """Update UI elements with modern styling"""
        mode = self.config.get("mode", "remove")
        running = self.clipboard_processor.running

        # Update window title
        status_text = "ACTIVE" if running else "IDLE"
        self.root.title(f"ClipperTool • {mode.upper()} MODE • {status_text}")

        # Update status indicator
        self.status_indicator.set_status(running)

        # Update control status text
        if running:
            self.control_status.configure(
                text="🟢 System is actively monitoring clipboard...",
                fg=MODERN_COLORS['accent_green']
            )
        else:
            self.control_status.configure(
                text="📡 System is idle. Click below to start processing.",
                fg=MODERN_COLORS['text_secondary']
            )

        # Update main control button
        if running:
            self.start_stop_button.configure(
                text="⏹ STOP PROCESSING",
                bg=MODERN_COLORS['accent_red'],
                fg='white',
                activebackground=MODERN_COLORS['accent_red']
            )
        else:
            self.start_stop_button.configure(
                text="▶ START PROCESSING",
                bg=MODERN_COLORS['accent_green'],
                fg='white',
                activebackground=MODERN_COLORS['accent_green']
            )

        # Update mode buttons
        if mode == "remove":
            self.remove_mode_btn.configure(bg=MODERN_COLORS['accent_blue'])
            self.keep_mode_btn.configure(bg=MODERN_COLORS['bg_tertiary'])
        else:
            self.remove_mode_btn.configure(bg=MODERN_COLORS['bg_tertiary'])
            self.keep_mode_btn.configure(bg=MODERN_COLORS['accent_blue'])

        # Update stats
        self._update_stats()

        # Update status text
        status_label_text = "Active" if running else "Idle"
        self.status_text_label.configure(text=f"Status: {status_label_text}")

    def _update_stats(self):
        """Update statistics display"""
        count = self.clipboard_processor.get_processed_count()
        self.processed_label.configure(text=f"Processed Items: {count}")

    # Callbacks for clipboard processor
    def _on_clipboard_processed(self, count):
        """Handle clipboard processing event"""
        self.root.after(0, self._update_stats)

    def _on_clipboard_error(self, error_msg):
        """Handle clipboard processing error"""
        print(f"Clipboard processing error: {error_msg}")
        # Could show error in UI if desired
