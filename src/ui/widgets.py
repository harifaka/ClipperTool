"""
Custom UI widgets for ClipperTool
"""

import tkinter as tk
from src.ui.constants import MODERN_COLORS, FONTS


class GoldenButton(tk.Frame):
    """Futuristic golden button with hover and active states"""

    def __init__(self, parent, text, command, icon="", active=False, **kwargs):
        super().__init__(parent, bg=MODERN_COLORS['bg_card'], **kwargs)
        self.command = command
        self.active = active
        self.icon = icon
        self.text = text

        self.canvas = tk.Canvas(
            self,
            height=50,
            bg=MODERN_COLORS['bg_card'],
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        self.canvas.bind("<Button-1>", lambda e: self.command())
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)

        self._draw_button()

    def _draw_button(self):
        """Draw the current state of the button"""
        self.canvas.delete("all")
        width = self.canvas.winfo_width() or 200
        height = self.canvas.winfo_height() or 50

        if width <= 1 or height <= 1:
            self.after(10, self._draw_button)
            return

        frame_color = MODERN_COLORS['accent_gold'] if self.active else MODERN_COLORS['border']
        bg_color = MODERN_COLORS['bg_secondary'] if self.active else MODERN_COLORS['bg_card']
        text_color = MODERN_COLORS['accent_gold'] if self.active else MODERN_COLORS['text_secondary']

        # Futuristic polygon frame
        points = [
            10, 5, width - 10, 5,
            width - 5, 10, width - 5, height - 10,
            width - 10, height - 5, 10, height - 5,
            5, height - 10, 5, 10
        ]

        self.canvas.create_polygon(points, fill=bg_color, outline=frame_color, width=2)

        # Inner glow if active
        if self.active:
            inner = [
                12, 7, width - 12, 7,
                width - 7, 12, width - 7, height - 12,
                width - 12, height - 7, 12, height - 7,
                7, height - 12, 7, 12
            ]
            self.canvas.create_polygon(inner, fill="", outline=MODERN_COLORS['accent_gold'], width=1)

        text = f"{self.icon} {self.text}" if self.icon else self.text
        self.canvas.create_text(
            width / 2, height / 2,
            text=text,
            fill=text_color,
            font=FONTS['body'] + ("bold",),
            anchor="center"
        )

    def _draw_hover(self):
        """Draw hover state"""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        frame_color = MODERN_COLORS['accent_gold_hover'] if not self.active else MODERN_COLORS['accent_gold']
        bg_color = MODERN_COLORS['bg_secondary']
        text_color = MODERN_COLORS['accent_gold_hover']

        points = [
            10, 5, width - 10, 5,
            width - 5, 10, width - 5, height - 10,
            width - 10, height - 5, 10, height - 5,
            5, height - 10, 5, 10
        ]

        self.canvas.create_polygon(points, fill=bg_color, outline=frame_color, width=2)

        text = f"{self.icon} {self.text}" if self.icon else self.text
        self.canvas.create_text(
            width / 2, height / 2,
            text=text,
            fill=text_color,
            font=FONTS['body'] + ("bold",),
            anchor="center"
        )

    def _on_enter(self, _):
        if not self.active:
            self._draw_hover()

    def _on_leave(self, _):
        self._draw_button()

    def set_active(self, active: bool):
        self.active = active
        self._draw_button()


class StatusIndicator(tk.Frame):
    """Circular pulsing online/offline status indicator"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=MODERN_COLORS['bg_card'], **kwargs)

        self.status_canvas = tk.Canvas(
            self,
            width=16,
            height=16,
            bg=MODERN_COLORS['bg_card'],
            highlightthickness=0
        )
        self.status_canvas.pack(side="left", padx=(0, 12))

        self.status_label = tk.Label(
            self,
            text="OFFLINE",
            font=FONTS['header'],
            bg=MODERN_COLORS['bg_card'],
            fg=MODERN_COLORS['text_secondary']
        )
        self.status_label.pack(side="left")

        self.running = False
        self.animation_step = 0
        self.set_status(False)

    def set_status(self, running: bool):
        """Update status and begin animation if needed"""
        self.running = running

        if running:
            self.status_label.configure(text="ONLINE", fg=MODERN_COLORS['success'])
            self._animate()
        else:
            self.status_label.configure(text="OFFLINE", fg=MODERN_COLORS['text_secondary'])
            self._draw_static()

    def _draw_static(self):
        """Draw static circle"""
        self.status_canvas.delete("all")
        color = MODERN_COLORS['success'] if self.running else MODERN_COLORS['text_secondary']
        self.status_canvas.create_oval(2, 2, 14, 14, fill=color, outline=color)

    def _animate(self):
        """Pulsing circle animation"""
        if not self.running:
            return

        self.status_canvas.delete("all")

        base = 4
        pulse = int(2 + 2 * abs(0.5 - (self.animation_step % 60) / 60))

        self.status_canvas.create_oval(
            8 - base - pulse, 8 - base - pulse,
            8 + base + pulse, 8 + base + pulse,
            outline=MODERN_COLORS['success'],
            width=1
        )

        self.status_canvas.create_oval(
            8 - base, 8 - base,
            8 + base, 8 + base,
            fill=MODERN_COLORS['success'],
            outline=MODERN_COLORS['success']
        )

        self.animation_step += 1
        self.after(50, self._animate)
