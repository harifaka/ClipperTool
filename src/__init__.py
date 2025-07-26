# src/__init__.py
"""ClipperTool - A professional clipboard filtering application."""

__version__ = "1.0.0"
__author__ = "Harifaka"

# src/config/__init__.py
"""Configuration management module."""

from .config.config_manager import ConfigManager

__all__ = ['ConfigManager']

# src/core/__init__.py
"""Core functionality module."""

__all__ = ['ClipboardProcessor', 'ClipboardMonitor', 'FilterMode']

# src/ui/__init__.py
"""User interface module."""

from .main_window import ClipperApp

__all__ = ['ClipperApp']

# src/utils/__init__.py
"""Utility functions module."""

from .resources import resource_path, get_app_data_dir, ensure_directory_exists

__all__ = ['resource_path', 'get_app_data_dir', 'ensure_directory_exists']