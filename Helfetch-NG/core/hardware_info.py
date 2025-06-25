# core/hardware_info.py

import subprocess
import re
import psutil # استيراد مكتبة psutil

def get_hardware_info():
    """
    Collects essential hardware information (CPU, RAM, Disk, GPU, Battery, CPU Usage, CPU Temp, Disk I/O).
    Utilizes psutil for efficient data collection and subprocess for less common info.
    """
    info = {}

    # 1. CPU Information (Name)
    try:
        # Get CPU model name from /proc/cpuinfo (usually stable and fast)
        with open('/proc/cpuinfo', 'r') as f:
            cpu_info_content = f.read()
            model_name_match = re.search(r'model name\s*:\s*(.*)', cpu_info_content)
            if model_name_match:
                info['CPU'] = model_name_match.group(1).strip()
            else:
                info['CPU'] = 'N/A'
    except FileNotFoundError:
        info['CPU'] = 'N/A'

    # 2. CPU Usage (using psutil)
    try:
        # interval=0.1 means it will block for 0.1 seconds to calculate usage
        # This is the trade-off: more accurate usage but adds a slight delay
        cpu_percent = psutil.cpu_percent(interval=0.1) 
        info['CPU Usage'] = f"{cpu_percent:.1f}%"
    except Exception:
        info['CPU Usage'] = 'N/A'
    
    # 3. CPU Temperature (requires psutil-sensors or specific Linux paths)
    # psutil.sensors_temperatures() requires psutil-sensors which is not default psutil
    # For simplicity, if your system doesn't expose it easily, it's safer to keep N/A or a more specific method.
    cpu_temp = 'N/A'
    try:
        # Example for Linux (might need adaptation for other systems)
        # Often found in /sys/class/thermal/thermal_zone*/temp
        temp_files = [f for f in os.listdir('/sys/class/thermal/') if f.startswith('thermal_zone')]
        for tf in temp_files:
            if 'temp' in os.listdir(os.path.join('/sys/class/thermal/', tf)):
                with open(os.path.join('/sys/class/thermal/', tf, 'temp'), 'r') as f:
                    temp_raw = int(f.read().strip())
                    # Temperatures are often in millidegrees Celsius
                    cpu_temp = f"{temp_raw / 1000.0:.1f}°C"
                    break # Take the first one found
    except Exception:
        pass # Keep N/A
    info['CPU Temp'] = cpu_temp


    # 4. RAM Information (Total, Used, Usage %) using psutil
    try:
        ram = psutil.virtual_memory()
        total_ram_gb = f"{(ram.total / (1024**3)):.1f}Gi"
        used_ram_gb = f"{(ram.used / (1024**3)):.1f}Gi"
        info['RAM'] = f"{used_ram_gb}/{total_ram_gb}" # e.g., 4.0Gi/15Gi
        info['RAM Usage %'] = f"{ram.percent:.1f}%"
    except Exception:
        info['RAM'] = 'N/A'
        info['RAM Usage %'] = 'N/A'

    # 5. Disk Usage (Root partition only for simplicity) using psutil
    try:
        # Use psutil.disk_usage for '/' (root partition)
        disk_usage = psutil.disk_usage('/')
        info['Disk'] = f"{disk_usage.percent:.0f}%" # e.g., 27%
    except Exception:
        info['Disk'] = 'N/A'

    # 6. Disk I/O (Read/Write) using psutil
    try:
        # Get overall disk I/O counters
        disk_io = psutil.disk_io_counters(perdisk=False) # False for total, True for per-disk
        if disk_io:
            read_mb = f"{(disk_io.read_bytes / (1024 * 1024)):.1f}MB"
            write_mb = f"{(disk_io.write_bytes / (1024 * 1024)):.1f}MB"
            info['Disk I/O'] = f"R:{read_mb}, W:{write_mb}"
        else:
            info['Disk I/O'] = 'N/A'
    except Exception:
        info['Disk I/O'] = 'N/A'

    # 7. GPU Information (still using lspci as psutil doesn't directly provide detailed GPU models)
    try:
        gpu_output = subprocess.check_output(['lspci', '-k'], text=True).strip()
        gpu_lines = []
        for line in gpu_output.split('\n'):
            if 'VGA compatible controller' in line or '3D controller' in line:
                gpu_lines.append(line.split(':', 2)[-1].strip()) # Extract description
        info['GPU'] = ", ".join(gpu_lines) if gpu_lines else 'N/A'

    except (subprocess.CalledProcessError, FileNotFoundError):
        info['GPU'] = 'N/A' # lspci might not be available or command fails


    # 8. Battery Information (using psutil)
    try:
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Charging" if battery.power_plugged else "Discharging"
            secs_left = battery.secsleft
            if secs_left == psutil.POWER_TIME_UNKNOWN:
                time_left = "N/A"
            elif secs_left == psutil.POWER_TIME_UNLIMITED:
                time_left = "Full"
            else:
                hours, rem = divmod(secs_left, 3600)
                minutes, seconds = divmod(rem, 60)
                time_left = f"Est. {int(hours)}h {int(minutes)}m"
            info['Battery'] = f"{battery.percent:.0f}% ({plugged}, {time_left})"
        else:
            info['Battery'] = 'N/A' # No battery found
    except Exception:
        info['Battery'] = 'N/A' # psutil.sensors_battery() might not be available or fails

    return info

# For testing this module independently
if __name__ == "__main__":
    hardware_data = get_hardware_info()
    print("\n--- Hardware Information ---")
    for key, value in hardware_data.items():
        print(f"{key}: {value}")
