"""
Main application window for ClipperTool.
Handles the primary user interface and user interactions.
"""

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from typing import Optional

from ..config.config_manager import ConfigManager
from ..core.clipboard_processor import ClipboardMonitor, ClipboardProcessor, FilterMode


class ClipperApp:
    """Main application window class."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        # Initialize components
        self.config_manager = ConfigManager()
        self.clipboard_monitor = ClipboardMonitor()
        self.config = self.config_manager.load_config()

        # UI variables
        self.file_var = tk.StringVar()

        # Setup error callback
        self.clipboard_monitor.set_error_callback(self._handle_error)

        # Initialize UI
        self._create_widgets()
        self._load_filter_files()
        self._update_ui()

        # Setup cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self) -> None:
        """Create and layout UI widgets."""
        # Apply theme
        self.style = tb.Style("cosmo")

        # Main frame
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill="both", expand=True)

        # File selection dropdown
        self.file_dropdown = ttk.Combobox(
            self.frame,
            textvariable=self.file_var,
            state="readonly"
        )
        self.file_dropdown.pack(fill="x", pady=5)
        self.file_dropdown.bind("<<ComboboxSelected>>", self._on_file_selected)

        # Start/Stop button
        self.start_stop_button = ttk.Button(
            self.frame,
            command=self._toggle_monitoring
        )
        self.start_stop_button.pack(fill="x", pady=10)

        # Create menu bar
        self._create_menu()

    def _create_menu(self) -> None:
        """Create application menu bar."""
        menubar = tk.Menu(self.root)

        # Mode menu
        mode_menu = tk.Menu(menubar, tearoff=0)
        mode_menu.add_command(
            label="Remove Mode",
            command=lambda: self._set_mode("remove")
        )
        mode_menu.add_command(
            label="Keep Mode",
            command=lambda: self._set_mode("keep")
        )
        menubar.add_cascade(label="Mode", menu=mode_menu)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Reload Configs",
            command=self._load_filter_files
        )
        menubar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menubar)

    def _load_filter_files(self) -> None:
        """Load available filter files into dropdown."""
        files = self.config_manager.get_filter_files()
        self.file_dropdown['values'] = files

        selected_file = self.config.get("selected_file", "")

        if selected_file in files:
            self.file_var.set(selected_file)
        elif files:
            self.file_var.set(files[0])
        else:
            self.file_var.set("")

        self._update_processor()
        self._update_ui()

    def _set_mode(self, mode: str) -> None:
        """Set the filtering mode."""
        self.config["mode"] = mode
        self._save_and_update()

    def _on_file_selected(self, event=None) -> None:
        """Handle file selection change."""
        self._save_and_update()

    def _save_and_update(self) -> None:
        """Save configuration and update UI."""
        self.config["selected_file"] = self.file_var.get()
        self.config_manager.save_config(self.config)
        self._update_processor()
        self._update_ui()

    def _update_processor(self) -> None:
        """Update the clipboard processor with current settings."""
        filename = self.file_var.get()
        keywords = self.config_manager.load_keywords_from_file(filename)
        mode = FilterMode.REMOVE if self.config.get("mode") == "remove" else FilterMode.KEEP

        processor = ClipboardProcessor(keywords, mode)
        self.clipboard_monitor.set_processor(processor)

    def _update_ui(self) -> None:
        """Update UI elements based on current state."""
        mode = self.config.get("mode", "remove")
        title_mode = "Remove Mode" if mode == "remove" else "Keep Mode"
        status_text = "Running" if self.clipboard_monitor.is_running() else "Stopped"

        # Update window title
        self.root.title(f"ClipperTool - {title_mode} ({status_text})")

        # Update background color
        bg_color = "#d0e7ff" if mode == "remove" else "#d0ffd8"
        self.root.configure(bg=bg_color)

        # Update button text
        button_action = "stop" if self.clipboard_monitor.is_running() else "run"
        self.start_stop_button.configure(
            text=f"Clipper is {status_text}. Press to {button_action} it."
        )

    def _toggle_monitoring(self) -> None:
        """Toggle clipboard monitoring on/off."""
        if self.clipboard_monitor.is_running():
            self.clipboard_monitor.stop_monitoring()
        else:
            self.clipboard_monitor.start_monitoring()

        self._update_ui()

    def _handle_error(self, error_message: str) -> None:
        """Handle errors from clipboard monitoring."""
        print(f"Error: {error_message}")
        # Could show a messagebox or log to file here

    def _on_closing(self) -> None:
        """Handle application shutdown."""
        self.clipboard_monitor.stop_monitoring()
        self.root.destroy()