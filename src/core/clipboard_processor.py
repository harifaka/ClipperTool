"""
Clipboard processing logic for ClipperTool.
Handles filtering text based on keywords and mode settings.
"""

import threading
import time
import pyperclip
from typing import List, Callable, Optional
from enum import Enum


class FilterMode(Enum):
    """Enumeration for filter modes."""
    REMOVE = "remove"
    KEEP = "keep"


class ClipboardProcessor:
    """Handles clipboard text processing and filtering."""

    def __init__(self, keywords: List[str], mode: FilterMode):
        self.keywords = keywords
        self.mode = mode

    def process_text(self, text: str) -> str:
        """
        Process text based on keywords and mode.

        Args:
            text: Input text to process

        Returns:
            Filtered text
        """
        if not text or not self.keywords:
            return text

        lines = text.splitlines()

        if self.mode == FilterMode.REMOVE:
            filtered_lines = [
                line for line in lines
                if not any(keyword in line for keyword in self.keywords)
            ]
        else:  # KEEP mode
            filtered_lines = [
                line for line in lines
                if any(keyword in line for keyword in self.keywords)
            ]

        return "\n".join(filtered_lines)


class ClipboardMonitor:
    """Monitors and processes clipboard changes."""

    def __init__(self):
        self.running = False
        self.last_clipboard = None
        self.processor: Optional[ClipboardProcessor] = None
        self.error_callback: Optional[Callable[[str], None]] = None
        self._monitor_thread: Optional[threading.Thread] = None

    def set_processor(self, processor: ClipboardProcessor) -> None:
        """Set the clipboard processor."""
        self.processor = processor

    def set_error_callback(self, callback: Callable[[str], None]) -> None:
        """Set error callback function."""
        self.error_callback = callback

    def start_monitoring(self) -> None:
        """Start monitoring clipboard changes."""
        if self.running:
            return

        self.running = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self) -> None:
        """Stop monitoring clipboard changes."""
        self.running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)

    def is_running(self) -> bool:
        """Check if monitoring is active."""
        return self.running

    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.running:
            try:
                current_text = pyperclip.paste()

                if current_text != self.last_clipboard and self.processor:
                    self.last_clipboard = current_text
                    processed_text = self.processor.process_text(current_text)

                    if processed_text != current_text:
                        pyperclip.copy(processed_text)

            except Exception as e:
                if self.error_callback:
                    self.error_callback(f"Clipboard monitoring error: {e}")
                else:
                    print(f"Clipboard monitoring error: {e}")

            time.sleep(0.5)