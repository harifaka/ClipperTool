import tkinter as tk
from tkinter import ttk
from constants import COLORS

class ControlSection(tk.Frame):
    def __init__(self, parent, toggle_callback):
        super().__init__(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        self.pack(fill="x", pady=(0, 20), padx=2)

        header_frame = tk.Frame(self, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ SYSTEM CONTROL",
            font=("Consolas", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        self.start_stop_button = tk.Button(
            self,
            text="▶ START PROCESSING",
            font=("Consolas", 16, "bold"),
            relief="raised",
            bd=3,
            cursor="hand2",
            command=toggle_callback
        )
        self.start_stop_button.pack(fill="x", ipady=20, pady=10)

    def set_running(self, running):
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


class StatsSection(tk.Frame):
    def __init__(self, parent, reset_callback):
        super().__init__(parent, bg=COLORS['bg_card'], relief="raised", bd=1)
        self.pack(fill="x", pady=(0, 20), padx=2)

        header_frame = tk.Frame(self, bg=COLORS['bg_card'])
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="▼ SYSTEM METRICS",
            font=("Consolas", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['accent_gold']
        ).pack(anchor="w")

        stats_frame = tk.Frame(self, bg=COLORS['bg_card'])
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
            command=reset_callback,
            style="Modern.TButton"
        ).pack(side="right")

    def update_stats(self, count):
        self.processed_label.config(text=f"PROCESSED: {count} ITEMS")


class Footer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.pack(fill="x", side="bottom", pady=(20, 0))

        tk.Label(
            self,
            text="◢ ClipperTool - Advanced Clipboard Processing System ◣",
            font=("Consolas", 9),
            bg=COLORS['bg_primary'],
            fg=COLORS['text_secondary']
        ).pack()
