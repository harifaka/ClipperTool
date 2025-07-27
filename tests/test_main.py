import time
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import ClipperTool

@pytest.fixture
def app():
    app_instance = ClipperTool()
    yield app_instance
    if hasattr(app_instance, 'root'):
        app_instance.root.destroy()

@pytest.mark.skipif(os.getenv('CI') == 'true', reason="Skip GUI tests on CI")
def test_app_starts_and_stops(app):
    # Initially, app should not be running
    assert app.running is False, "App should start in stopped state"

    # Check initial file_var value (assuming it's a StringVar)
    initial_file_var = app.file_var.get()
    assert initial_file_var is not None, "file_var should be initialized"

    # Schedule app to quit mainloop after 2 seconds
    app.root.after(2000, app.root.quit)

    # Start the app (toggle running state)
    app.toggle_running()
    assert app.running is True, "App should be running after toggle"

    # Run mainloop on the main thread (this will block for ~2 seconds)
    app.root.mainloop()

    # After mainloop exits, stop the app (toggle running state off)
    app.toggle_running()
    assert app.running is False, "App should be stopped after toggle"

    # Optionally check clipboard monitor flag if exists
    if hasattr(app, 'clipboard_monitor_active'):
        assert app.clipboard_monitor_active is False
