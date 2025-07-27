import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.main import ClipperTool

import threading
import time
import pytest


@pytest.fixture
def app():
    app_instance = ClipperTool()  # or however you instantiate it
    yield app_instance
    # Cleanup if needed
    if hasattr(app_instance, 'root'):
        app_instance.root.destroy()

def test_app_starts_and_stops(app):
    # Run the mainloop in a separate thread to avoid blocking test runner
    def run_app():
        app.root.after(2000, app.root.quit)  # quit after 2 seconds
        app.root.mainloop()

    t = threading.Thread(target=run_app)
    t.start()

    # Check initial state
    assert not app.running
    assert app.file_var.get() is not None  # Should have a selected file or empty string

    # Start the app
    app.toggle_running()
    assert app.running is True

    # Wait a bit to let clipboard loop run (optional)
    time.sleep(1)

    # Stop the app
    app.toggle_running()
    assert app.running is False

    # Wait for GUI to close
    t.join(timeout=3)
