"""
Core clipboard processing functionality
"""

import threading
import time
import pyperclip
from src.config.config_manager import ConfigManager


class ClipboardCleaner:
    """Handles text filtering based on keywords and mode"""

    def __init__(self, keywords, mode):
        self.keywords = keywords
        self.mode = mode

    def process_text(self, text):
        """Process text based on keywords and mode"""
        lines = text.splitlines()

        if self.mode == "remove":
            filtered_lines = [
                line for line in lines
                if not any(keyword in line for keyword in self.keywords)
            ]
        else:  # keep mode
            filtered_lines = [
                line for line in lines
                if any(keyword in line for keyword in self.keywords)
            ]

        return "\n".join(filtered_lines)


class ClipboardProcessor:
    """Main clipboard processing engine"""

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or ConfigManager()
        self.running = False
        self.last_clipboard = None
        self.processed_count = 0
        self.processing_thread = None

        # Callbacks for UI updates
        self.on_processed_callback = None
        self.on_error_callback = None

    def set_callbacks(self, on_processed=None, on_error=None):
        """Set callback functions for UI updates"""
        if on_processed:
            self.on_processed_callback = on_processed
        if on_error:
            self.on_error_callback = on_error

    def start_processing(self, config):
        """Start clipboard monitoring and processing"""
        if self.running:
            return

        self.running = True
        self.config = config
        self.processing_thread = threading.Thread(
            target=self._clipboard_loop,
            daemon=True
        )
        self.processing_thread.start()

    def stop_processing(self):
        """Stop clipboard monitoring"""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=1.0)

    def reset_stats(self):
        """Reset processing statistics"""
        self.processed_count = 0

    def get_processed_count(self):
        """Get number of processed items"""
        return self.processed_count

    def _clipboard_loop(self):
        """Main clipboard monitoring loop"""
        while self.running:
            try:
                text = pyperclip.paste()

                if text != self.last_clipboard:
                    self.last_clipboard = text
                    cleaned = self._clean_clipboard(text)

                    if cleaned != text:
                        pyperclip.copy(cleaned)
                        self.processed_count += 1

                        # Notify UI of processing
                        if self.on_processed_callback:
                            self.on_processed_callback(self.processed_count)

            except Exception as e:
                if self.on_error_callback:
                    self.on_error_callback(str(e))
                else:
                    print(f"Clipboard processing error: {e}")

            time.sleep(0.5)

    def _clean_clipboard(self, text):
        """Clean clipboard text based on current configuration"""
        filename = self.config.get("selected_file", "")
        if not filename:
            return text

        keywords = self.config_manager.load_keywords_from_file(filename)
        if not keywords:
            return text

        cleaner = ClipboardCleaner(keywords, self.config.get("mode", "remove"))
        return cleaner.process_text(text)
