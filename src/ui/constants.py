import os

COLORS = {
    'bg_primary': '#1e1e2f',
    'bg_secondary': '#2e2e3f',
    'bg_card': '#2a2a3a',
    'text_primary': '#ffffff',
    'text_secondary': '#aaaaaa',
    'accent_gold': '#d4af37',
    'accent_blue': '#3a8ee6',
    'accent_red': '#ff5c57',
    'success': '#28a745',
    'danger': '#dc3545',
    'accent_green': '#4caf50',
}

FILTERS_FOLDER = os.path.join(os.path.expanduser("~"), ".clippertool_filters")

# Make sure the filters folder exists
os.makedirs(FILTERS_FOLDER, exist_ok=True)
