# display/ascii_art.py

# ANSI escape codes for colors
COLORS = {
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\033[0;34m",
    "magenta": "\033[0;35m",
    "cyan": "\033[0;36m",
    "white": "\033[0;37m",
    "light_red": "\033[1;31m",
    "light_green": "\033[1;32m",
    "light_yellow": "\033[1;33m",
    "light_blue": "\033[1;34m",
    "light_magenta": "\033[1;35m",
    "light_cyan": "\033[1;36m",
    "light_white": "\033[1;37m",
    "reset": "\033[0m" # Reset color to default
}

# Helwan Linux ASCII Art (Raw, no colors here)
# Your unique Helwan Linux logo!
HELWAN_LOGO = r"""
▖▖   ▜
▙▌█▌▐ ▌▌▌▀▌▛▌
▌▌▙▖▐▖▚▚▘█▌▌▌
"""

def get_ascii_logo(os_name):
    """
    Returns the ASCII art logo based on the OS name.
    """
    if "Helwan Linux" in os_name:
        # Splitlines will correctly handle the raw string
        return HELWAN_LOGO.strip().splitlines()
    # Add more logos here later for other OSes if needed
    return None
