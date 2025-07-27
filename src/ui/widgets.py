"""
Custom UI widgets for ClipperTool
"""

import tkinter as tk
from src.ui.constants import COLORS, FONTS


class GoldenButton(tk.Frame):
    """Custom futuristic golden button widget"""

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
        """Draw the button in its current state"""
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
                12, 7, width - 12, 7, width - 7, 12, width - 7, height - 12,
                       width - 12, height - 7, 12, height - 7, 7, height - 12, 7, 12
            ]
            self.canvas.create_polygon(inner_points, fill="", outline=COLORS['accent_gold'], width=1)

        # Text
        display_text = f"{self.icon} {self.text}" if self.icon else self.text
        self.canvas.create_text(
            width / 2, height / 2,
            text=display_text,
            fill=text_color,
            font=FONTS['body'] + ("bold",),
            anchor="center"
        )

    def on_enter(self, event):
        """Handle mouse enter event"""
        if not self.active:
            self.canvas.configure(cursor="hand2")
            self.draw_hover_effect()

    def on_leave(self, event):
        """Handle mouse leave event"""
        self.draw_button()

    def draw_hover_effect(self):
        """Draw button with hover effect"""
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
            font=FONTS['body'] + ("bold",),
            anchor="center"
        )

    def set_active(self, active):
        """Set the active state of the button"""
        self.active = active
        self.draw_button()


class StatusIndicator(tk.Frame):
    """Animated status indicator widget"""

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
            font=FONTS['header'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        )
        self.status_label.pack(side="left")

        self.running = False
        self.animation_step = 0
        self.set_status(False)

    def set_status(self, running):
        """Set the status indicator state"""
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
        """Draw static status indicator"""
        self.status_canvas.delete("all")
        color = COLORS['success'] if self.running else COLORS['text_secondary']
        self.status_canvas.create_oval(2, 2, 14, 14, fill=color, outline=color)

    def animate_indicator(self):
        """Animate the status indicator with pulsing effect"""
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