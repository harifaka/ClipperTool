import tkinter as tk
from tkinter import messagebox
import os
import platform
import subprocess
from constants import COLORS, FILTERS_FOLDER

class NewConfigPopup:
    def __init__(self, parent, on_success_callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Create New Configuration")
        self.top.geometry("450x250")
        self.top.resizable(False, False)
        self.top.configure(bg=COLORS['bg_primary'])
        self.top.transient(parent)
        self.top.grab_set()

        main_frame = tk.Frame(self.top, bg=COLORS['bg_card'], relief="raised", bd=2)
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

        self.entry = tk.Entry(
            main_frame,
            font=("Consolas", 12),
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_primary'],
            insertbackground=COLORS['text_primary'],
            relief="solid",
            bd=1
        )
        self.entry.pack(fill="x", padx=20, pady=(5, 20), ipady=8)
        self.entry.focus()

        button_frame = tk.Frame(main_frame, bg=COLORS['bg_card'])
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.top.destroy,
            style="Modern.TButton"
        ).pack(side="right", padx=(10, 0))

        ttk.Button(
            button_frame,
            text="Create",
            command=self.on_submit,
            style="Modern.TButton"
        ).pack(side="right")

        self.entry.bind("<Return>", lambda e: self.on_submit())

        self.on_success_callback = on_success_callback

    def on_submit(self):
        filename = self.entry.get().strip()
        if not filename:
            return
        if not filename.endswith(".txt"):
            filename += ".txt"
        filepath = os.path.join(FILTERS_FOLDER, filename)
        if os.path.exists(filepath):
            messagebox.showerror("Error", "File already exists!")
            return
        try:
            with open(filepath, "w") as f:
                f.write("# Add your keywords here, one per line\n")
            self.top.destroy()
            messagebox.showinfo("Success", f"Config file '{filename}' created successfully!")
            if self.on_success_callback:
                self.on_success_callback(filename)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create file:\n{e}")

def open_file(filepath):
    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":
            subprocess.call(["open", filepath])
        else:
            subprocess.call(["xdg-open", filepath])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")

def open_folder(folder_path):
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", folder_path])
        else:
            subprocess.call(["xdg-open", folder_path])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open folder:\n{e}")
