"""
Resource management utilities for ClipperTool.
Handles paths and resource loading for both development and bundled environments.
"""

import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    Args:
        relative_path: Relative path to resource

    Returns:
        Absolute path to resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Development environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_app_data_dir() -> str:
    """
    Get application data directory.

    Returns:
        Path to application data directory
    """
    return os.path.join(os.path.expanduser("~"), "Documents", "ClipperTool")


def ensure_directory_exists(path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.

    Args:
        path: Directory path to ensure exists
    """
    os.makedirs(path, exist_ok=True)