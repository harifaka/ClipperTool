"""
Popup dialogs for ClipperTool
"""

import tkinter as tk
from tkinter import messagebox

from src.ui.constants import COLORS, FONTS


class CreateConfigDialog:
    """Dialog for creating new configuration files"""

    def __init__(self, parent, config_manager, on_success_callback=None):
        self.config_manager = config_manager
        self.on_success_callback = on_success_callback
        self.result = None

        self._create_dialog(parent)

    def _create_dialog(self, parent):
        """Create the dialog window"""
        self.popup = tk.Toplevel(parent)
        self.popup.title("Create New Configuration")
        self.popup.geometry("450x250")
        self.popup.resizable(False, False)
        self.popup.configure(bg=COLORS['bg_primary'])

        self.popup.transient(parent)
        self.popup.grab_set()

        # Center the dialog
        self.popup.geometry("450x250+{}+{}".format(
            parent.winfo_rootx() + 175,
            parent.winfo_rooty() + 200
        ))

        self._create_content()

    def _create_content(self):
        """Create dialog content"""
        main_frame = tk.Frame(self.popup, bg=COLORS['bg_card'], relief="raised", bd=2)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(
            main_frame,
            text="▼ NEW CONFIGURATION",
            font=FONTS['header'],
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(pady=(20, 20))

        # Label
        tk.Label(
            main_frame,
            text="Configuration Name:",
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        ).pack(anchor="w", padx=20)

        # Entry
        self.entry = tk.Entry(
            main_frame,
            font=FONTS['body'],
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['text_primary'],
            relief="solid",
            bd=1
        )
        self.entry.pack(fill="x", padx=20, pady=(5, 20), ipady=8)
        self.entry.focus()

        # Buttons
        self._create_buttons(main_frame)

        # Bind Enter key
        self.entry.bind("<Return>", lambda e: self._on_submit())

    def _create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = tk.Frame(parent, bg=COLORS['bg_card'])
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            font=FONTS['button'],
            relief="solid",
            bd=1,
            cursor="hand2"
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        # Create button
        create_btn = tk.Button(
            button_frame,
            text="Create",
            command=self._on_submit,
            bg=COLORS['success'],
            fg=COLORS['bg_primary'],
            font=FONTS['button'],
            relief="solid",
            bd=1,
            cursor="hand2"
        )
        create_btn.pack(side="right")

    def _on_submit(self):
        """Handle submit button click"""
        filename = self.entry.get().strip()
        if not filename:
            messagebox.showwarning("Warning", "Please enter a filename!")
            return

        try:
            filepath = self.config_manager.create_filter_file(filename)
            self.result = filename if not filename.endswith(".txt") else filename
            self.popup.destroy()

            if self.on_success_callback:
                self.on_success_callback(self.result)

            messagebox.showinfo("Success", f"Config file '{self.result}' created successfully!")

        except FileExistsError:
            messagebox.showerror("Error", "File already exists!")
        except IOError as e:
            messagebox.showerror("Error", str(e))

    def _on_cancel(self):
        """Handle cancel button click"""
        self.popup.destroy()

    def show(self):
        """Show the dialog and return the result"""
        self.popup.wait_window()
        return self.result


def show_error_message(title, message):
    """Show an error message dialog"""
    messagebox.showerror(title, message)


def show_warning_message(title, message):
    """Show a warning message dialog"""
    messagebox.showwarning(title, message)


def show_info_message(title, message):
    """Show an info message dialog"""
    messagebox.showinfo(title, message)


def show_confirmation_dialog(title, message):
    """Show a confirmation dialog and return True/False"""
    return messagebox.askyesno(title, message)