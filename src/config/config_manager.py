"""
Configuration management for ClipperTool
"""

import os
import json


class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), "Documents", "ClipperTool")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.filters_folder = os.path.join(self.config_dir, "Configs")

        # Ensure directories exist
        os.makedirs(self.filters_folder, exist_ok=True)

        self._default_config = {"selected_file": "", "mode": "remove"}

    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(self.config_file):
            return self._default_config.copy()

        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)

            # Ensure required keys exist
            for key, default_value in self._default_config.items():
                if key not in data:
                    data[key] = default_value

            return data
        except Exception:
            return self._default_config.copy()

    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_filters_folder(self):
        """Get the filters folder path"""
        return self.filters_folder

    def get_filter_files(self):
        """Get list of available filter files"""
        try:
            return [f for f in os.listdir(self.filters_folder) if f.endswith(".txt")]
        except Exception:
            return []

    def create_filter_file(self, filename):
        """Create a new filter file"""
        if not filename.endswith(".txt"):
            filename += ".txt"

        filepath = os.path.join(self.filters_folder, filename)

        if os.path.exists(filepath):
            raise FileExistsError(f"File '{filename}' already exists")

        try:
            with open(filepath, "w") as f:
                f.write("# Add your keywords here, one per line\n")
            return filepath
        except Exception as e:
            raise IOError(f"Could not create file: {e}")

    def get_filter_file_path(self, filename):
        """Get full path to a filter file"""
        return os.path.join(self.filters_folder, filename)

    def load_keywords_from_file(self, filename):
        """Load keywords from a filter file"""
        filepath = self.get_filter_file_path(filename)

        if not os.path.exists(filepath):
            return []

        try:
            with open(filepath, "r") as f:
                keywords = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]
            return keywords
        except Exception:
            return []