# core/system_info.py

import platform
import subprocess
import os
import re
import random # استيراد مكتبة random لاختيار الرسائل عشوائيا
import psutil # For running processes

# استيراد قائمة الرسائل من ملف quotes.py
from config.quotes import QUOTES

def get_running_processes():
    """
    Gets the top 5 running processes by CPU usage.
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                # Add a small delay for cpu_percent to be meaningful
                proc.cpu_percent(interval=0.01) # Small interval to get CPU usage
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort by CPU usage and get top 5
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top_processes = [f"{p['name']} ({p['cpu_percent']:.1f}% CPU, {p['memory_percent']:.1f}% RAM)" for p in processes[:5]]
        return "\n    ".join(top_processes) if top_processes else "N/A"
    except Exception:
        return "N/A"

def get_system_info():
    """
    Collects basic system-related information.
    """
    info = {}

    # 1. User
    try:
        info['User'] = os.getlogin()
    except OSError:
        info['User'] = os.getenv('USER') or os.getenv('USERNAME') or 'N/A'

    # 2. Host
    info['Host'] = platform.node()

    # 3. OS
    os_name = 'N/A'
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    os_name = line.strip().split('=')[1].strip('\"')
                    break
        if "Arch Linux" in os_name:
            os_name = os_name.replace("Arch Linux", "Helwan Linux")
            # يمكنك إضافة إصدار مخصص لـ Helwan Linux هنا
            # os_name += " (Ver. 1.0 'Phoenix')"
    except FileNotFoundError:
        os_name = platform.system()
        if os_name == "Windows":
            os_name = "Windows"
    info['OS'] = os_name

    # 4. Kernel
    info['Kernel'] = platform.release()

    # 5. Uptime
    uptime_val = 'N/A'
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            minutes, seconds = divmod(int(uptime_seconds), 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)

            if days > 0:
                uptime_val = f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                uptime_val = f"{hours}h {minutes}m"
            else:
                uptime_val = f"{minutes}m"
    except (FileNotFoundError, ValueError): # هذا هو السطر 85
        uptime_val = 'N/A'
    info['Uptime'] = uptime_val

    # 6. Shell
    shell_val = 'N/A'
    try:
        shell_val = os.getenv('SHELL')
        if shell_val:
            shell_val = os.path.basename(shell_val)
    except Exception:
        pass
    info['Shell'] = shell_val

    # 7. Terminal
    terminal_val = 'N/A'
    try:
        terminal_val = os.getenv('TERM') or os.getenv('COLORTERM')
    except Exception:
        pass
    info['Terminal'] = terminal_val

    # 8. Packages (Pacman, apt, etc.)
    packages_val = 'N/A'
    package_manager = 'N/A'
    
    # Try Pacman (Arch-based)
    try:
        pacman_count = subprocess.run(['pacman', '-Qq'], capture_output=True, text=True, check=True).stdout.count('\n')
        if pacman_count > 0:
            packages_val = str(pacman_count)
            package_manager = 'Pacman'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Try DPKG (Debian-based)
    if package_manager == 'N/A':
        try:
            dpkg_count = subprocess.run(['dpkg', '-l'], capture_output=True, text=True, check=True).stdout.count('\n')
            # dpkg -l includes header, subtract 5-6 lines for accuracy
            if dpkg_count > 0:
                packages_val = str(max(0, dpkg_count - 5))
                package_manager = 'DPKG'
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
    # Try RPM (RedHat-based)
    if package_manager == 'N/A':
        try:
            rpm_count = subprocess.run(['rpm', '-qa'], capture_output=True, text=True, check=True).stdout.count('\n')
            if rpm_count > 0:
                packages_val = str(rpm_count)
                package_manager = 'RPM'
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    if package_manager != 'N/A':
        info[f'Packages ({package_manager})'] = packages_val
    else:
        info['Packages'] = 'N/A' # Fallback if no known package manager is found

    # 9. Top Running Processes
    info['Top Processes'] = get_running_processes()


    return info

def get_inspirational_quote():
    """
    Returns a random inspirational quote from the QUOTES list.
    """
    return random.choice(QUOTES)

# For testing this module independently
if __name__ == "__main__":
    system_data = get_system_info()
    for key, value in system_data.items():
        print(f"{key}: {value}")
    print(f"\nInspirational Quote: {get_inspirational_quote()}")
