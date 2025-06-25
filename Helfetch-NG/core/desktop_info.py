# core/desktop_info.py

import os
import subprocess
import re
def get_desktop_info():
    """
    Collects information about the Desktop Environment (DE), Window Manager (WM),
    GTK/Qt themes, icons, and fonts.
    """
    info = {}

    # 1. Desktop Environment (DE)
    # XDG_CURRENT_DESKTOP is the most reliable way on modern Linux DEs.
    info['Desktop Environment'] = os.getenv('XDG_CURRENT_DESKTOP') or 'N/A'

    # 2. Window Manager (WM)
    # WM usually corresponds to the DE, but can be separate (e.g., i3, bspwm).
    # This is often found in the WM_NAME property via xprop, or specific env vars.
    # We'll try to get it from XDG_CURRENT_DESKTOP first, then fallback to xprop if needed.
    wm_name = 'N/A'
    try:
        # Check if a specific WM environment variable exists (e.g., for i3)
        if os.getenv('I3SOCK'):
            wm_name = 'i3'
        elif os.getenv('BSPWM_SOCKET'):
            wm_name = 'bspwm'
        # More robust way using xprop (requires xorg-xprop package)
        elif os.getenv('DISPLAY'): # Only run if a display is available
            wm_output = subprocess.check_output(
                ['xprop', '-root', '-notype', '_NET_WM_NAME'],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            # Example: _NET_WM_NAME(UTF8) = "GNOME Shell"
            match = re.search(r'\"([^\"]+)\"', wm_output)
            if match:
                wm_name = match.group(1)
        
        # If the DE itself is a WM (like GNOME Shell, KWin for KDE)
        if info['Desktop Environment'] and 'GNOME' in info['Desktop Environment']:
            wm_name = 'GNOME Shell'
        elif info['Desktop Environment'] and 'KDE' in info['Desktop Environment']:
            wm_name = 'KWin'
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass # xprop not found or display not available

    info['Window Manager'] = wm_name

    # 3. GTK Theme (for GTK-based DEs like GNOME, XFCE, Cinnamon, MATE)
    gtk_theme = 'N/A'
    try:
        # Check ~/.config/gtk-3.0/settings.ini
        gtk3_config_path = os.path.expanduser('~/.config/gtk-3.0/settings.ini')
        if os.path.exists(gtk3_config_path):
            with open(gtk3_config_path, 'r') as f:
                for line in f:
                    if 'gtk-theme-name=' in line:
                        gtk_theme = line.split('=')[1].strip()
                        break
        if gtk_theme == 'N/A': # Fallback for GTK2 or if not in settings.ini
            # Attempt to use 'gsettings' for GNOME/Cinnamon/MATE
            if os.getenv('XDG_CURRENT_DESKTOP') in ['GNOME', 'Cinnamon', 'MATE']:
                gtk_theme = subprocess.check_output(
                    ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
                    text=True, stderr=subprocess.DEVNULL
                ).strip().strip("'")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    info['GTK Theme'] = gtk_theme if gtk_theme else 'N/A'


    # 4. Icon Theme
    icon_theme = 'N/A'
    try:
        # Check ~/.config/gtk-3.0/settings.ini for GTK icon theme
        gtk3_config_path = os.path.expanduser('~/.config/gtk-3.0/settings.ini')
        if os.path.exists(gtk3_config_path):
            with open(gtk3_config_path, 'r') as f:
                for line in f:
                    if 'gtk-icon-theme-name=' in line:
                        icon_theme = line.split('=')[1].strip()
                        break
        if icon_theme == 'N/A': # Fallback using gsettings for GNOME-like DEs
            if os.getenv('XDG_CURRENT_DESKTOP') in ['GNOME', 'Cinnamon', 'MATE']:
                icon_theme = subprocess.check_output(
                    ['gsettings', 'get', 'org.gnome.desktop.interface', 'icon-theme'],
                    text=True, stderr=subprocess.DEVNULL
                ).strip().strip("'")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    info['Icons'] = icon_theme if icon_theme else 'N/A'


    # 5. Font (GTK/System Font)
    font_name = 'N/A'
    try:
        # Check ~/.config/gtk-3.0/settings.ini for GTK font
        gtk3_config_path = os.path.expanduser('~/.config/gtk-3.0/settings.ini')
        if os.path.exists(gtk3_config_path):
            with open(gtk3_config_path, 'r') as f:
                for line in f:
                    if 'gtk-font-name=' in line:
                        font_name = line.split('=')[1].strip()
                        break
        if font_name == 'N/A': # Fallback using gsettings for GNOME-like DEs
            if os.getenv('XDG_CURRENT_DESKTOP') in ['GNOME', 'Cinnamon', 'MATE']:
                font_name = subprocess.check_output(
                    ['gsettings', 'get', 'org.gnome.desktop.interface', 'font-name'],
                    text=True, stderr=subprocess.DEVNULL
                ).strip().strip("'")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    info['Font'] = font_name if font_name else 'N/A'

    # Note: Getting accurate info for Qt themes, cursor, or specific details for
    # non-GTK/GNOME environments (like pure Plasma/KDE without GTK apps) might
    # require parsing different config files or using qt5ct/qt6ct settings.
    # This current implementation focuses on common GTK-based setups.

    return info

# For testing this module independently
if __name__ == "__main__":
    desktop_data = get_desktop_info()
    print("\n--- Desktop Information ---")
    for key, value in desktop_data.items():
        print(f"{key}: {value}")
