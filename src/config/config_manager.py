"""
Configuration management for ClipperTool.
Handles loading, saving, and managing application settings.
"""

import os
import json
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration settings."""

    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), "Documents", "ClipperTool")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.filters_folder = os.path.join(self.config_dir, "Configs")

        # Ensure directories exist
        os.makedirs(self.filters_folder, exist_ok=True)

        self._default_config = {
            "selected_file": "",
            "mode": "remove"
        }

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        if not os.path.exists(self.config_file):
            return self._default_config.copy()

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Ensure all required keys exist
            for key, default_value in self._default_config.items():
                if key not in data:
                    data[key] = default_value

            return data
        except (json.JSONDecodeError, FileNotFoundError, Exception):
            return self._default_config.copy()

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_filters_folder(self) -> str:
        """Get the path to the filters folder."""
        return self.filters_folder

    def get_filter_files(self) -> list:
        """Get list of available filter files."""
        try:
            files = [f for f in os.listdir(self.filters_folder) if f.endswith(".txt")]
            return sorted(files)
        except FileNotFoundError:
            return []

    def load_keywords_from_file(self, filename: str) -> list:
        """Load keywords from a filter file."""
        if not filename:
            return []

        filepath = os.path.join(self.filters_folder, filename)
        if not os.path.exists(filepath):
            return []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                keywords = [line.strip() for line in f if line.strip()]
            return keywords
        except Exception as e:
            print(f"Error loading keywords from {filename}: {e}")
            return []