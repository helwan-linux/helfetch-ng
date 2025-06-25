# display/formatter.py

import re
from display.ascii_art import COLORS # استيراد قاموس الألوان من ascii_art
from config.default_config import DEFAULT_COLORS # استيراد الألوان الافتراضية

# دالة مساعدة لإزالة أكواد ANSI من النص لحساب الطول المرئي
def clean_ansi(text):
    """Removes ANSI escape codes from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-9;]*[0-9A-Z])')
    return ansi_escape.sub('', text)

def create_progress_bar(percentage, bar_length=20, filled_char="█", empty_char="-", bar_color="green", empty_color="white"):
    """
    Creates an ASCII art progress bar based on a percentage.
    """
    if not 0 <= percentage <= 100:
        percentage = max(0, min(100, percentage))

    filled_chars_count = int(bar_length * percentage / 100)
    empty_chars_count = bar_length - filled_chars_count

    filled_bar = COLORS.get(bar_color, COLORS["reset"]) + (filled_char * filled_chars_count)
    empty_bar = COLORS.get(empty_color, COLORS["reset"]) + (empty_char * empty_chars_count)

    return f"[{filled_bar}{empty_bar}{COLORS['reset']}]"


def format_info_output(info_data, logo_lines=None, inspirational_quote="", info_key_color="light_yellow", info_value_color="white", recommendations=None):
    """
    Formats the system information as a clear, columnar table,
    then appends the ASCII art logo, inspirational quote, and recommendations at the bottom.

    Args:
        info_data (dict): A dictionary containing all the system information.
        logo_lines (list, optional): A list of strings representing the ASCII art logo, line by line.
                                     Defaults to None.
        inspirational_quote (str, optional): An inspirational quote to display. Defaults to "".
        info_key_color (str, optional): The color for the information keys. Defaults to "light_yellow".
        info_value_color (str, optional): The color for the information values. Defaults to "white".
        recommendations (list, optional): A list of strings for system recommendations. Defaults to None.
    """
    
    # Ensure recommendations is a list for easy iteration
    if recommendations is None:
        recommendations = []

    # Get colors from DEFAULT_COLORS
    info_key_color_code = COLORS.get(DEFAULT_COLORS.get("info_key_color"), COLORS["reset"])
    info_value_color_code = COLORS.get(DEFAULT_COLORS.get("info_value_color"), COLORS["reset"])
    logo_color_code = COLORS.get(DEFAULT_COLORS.get("logo_color"), COLORS["reset"]) # نحتاجها لتطبيقها هنا
    quote_color_code = COLORS.get(DEFAULT_COLORS.get("quote_color"), COLORS["reset"])
    recommendation_color_code = COLORS.get("yellow", COLORS["reset"]) # Color for recommendations

    output_lines = []

    # 1. Format Info Data as a Table-like Structure
    max_key_width = 0
    # First pass to find max key width, excluding "Top Processes" from main alignment
    for key in info_data.keys():
        if key != "Top Processes":
            max_key_width = max(max_key_width, len(clean_ansi(key)))
    
    for key, value in info_data.items():
        if key == "Top Processes":
            # Handle multi-line "Top Processes" separately
            output_lines.append(f"{info_key_color_code}{key}:{COLORS['reset']}")
            if value and value != "N/A":
                for line in value.split('\n'):
                    output_lines.append(f"  {info_value_color_code}{line.strip()}{COLORS['reset']}")
            else:
                output_lines.append(f"  {info_value_color_code}N/A{COLORS['reset']}")
        else:
            # For other info, format normally with padding for alignment
            visible_key_len = len(clean_ansi(key))
            padding = max_key_width - visible_key_len
            formatted_key = f"{info_key_color_code}{key}{' ' * padding}:{COLORS['reset']}"
            formatted_value = f"{info_value_color_code}{value}{COLORS['reset']}"
            output_lines.append(f"{formatted_key} {formatted_value}")
    
    # Add a blank line after info for separation
    output_lines.append("")

    # 2. Add Recommendations (if any)
    if recommendations:
        output_lines.append(f"{recommendation_color_code}--- System Recommendations ---{COLORS['reset']}")
        for rec in recommendations:
            output_lines.append(f"{recommendation_color_code}- {rec}{COLORS['reset']}")
        output_lines.append(f"{recommendation_color_code}----------------------------{COLORS['reset']}")
        output_lines.append("") # Blank line after recommendations

    # 3. Add the ASCII Art Logo (if any)
    if logo_lines:
        # Apply color and reset after each line, since the logo itself is now raw
        for line in logo_lines:
            output_lines.append(f"{logo_color_code}{line}{COLORS['reset']}") # هنا التغيير: نضيف الألوان مرة واحدة
        output_lines.append("") # Blank line after logo

    # 4. Add the Inspirational Quote
    if inspirational_quote:
        output_lines.append(f"{quote_color_code}\"{inspirational_quote}\"{COLORS['reset']}")
    

    return "\n".join(output_lines)

# For testing this module independently (تحديث الجزء الخاص بالاختبار)
if __name__ == "__main__":
    # هذا الجزء يستخدم لغرض الاختبار المباشر لـ formatter.py فقط
    # لا تعتمد عليه لإخراج Helfetch بالكامل
    example_info = {
        "User": "testuser",
        "Host": "testhost",
        "OS": "Test OS (Ver. 1.0)",
        "Kernel": "6.0.0",
        "Uptime": "1d 2h 30m",
        "Shell": "bash",
        "Terminal": "kitty",
        "Packages (Pacman)": "1234",
        "CPU": "Intel Core i7-10700K",
        "CPU Usage": "25.5%",
        "CPU Temp": "55.0°C",
        "RAM": "8.0Gi/16.0Gi",
        "RAM Usage %": "50%",
        "Disk": "35%",
        "Disk I/O": "R:100MB, W:50MB",
        "GPU": "NVIDIA GeForce RTX 3080 (Driver: 535.113.01, Mem: 2000/10240MiB)",
        "Battery": "80% (Discharging, Est. 3h 45m)",
        "Local IP": "192.168.1.100",
        "Public IP": "203.0.113.45",
        "ISP": "Test ISP",
        "City": "Test City",
        "Country": "Test Country",
        "Bandwidth Usage": "Sent: 1000MB, Recv: 2000MB",
        "Top Processes": "firefox (15.2% CPU, 5.1% RAM)\nnpm (8.3% CPU, 2.0% RAM)\npython (3.1% CPU, 1.5% RAM)"
    }

    from display.ascii_art import get_ascii_logo
    logo = get_ascii_logo("Helwan Linux")

    # Mock DEFAULT_COLORS for independent testing if default_config.py is not easily accessible
    class MockDefaultColors:
        DEFAULT_COLORS = {
            "info_key_color": "light_yellow",
            "info_value_color": "white",
            "logo_color": "light_cyan",
            "quote_color": "light_green"
        }
    
    # Temporarily override DEFAULT_COLORS for testing this file directly
    global DEFAULT_COLORS 
    DEFAULT_COLORS = MockDefaultColors.DEFAULT_COLORS

    # Example with recommendations
    example_recommendations = [
        "RAM usage is high. Consider closing unnecessary applications.",
        "Your system appears to be running optimally. Keep up the good work!"
    ]

    print("--- Test with Logo and Recommendations ---")
    formatted_output = format_info_output(
        info_data=example_info,
        logo_lines=logo,
        inspirational_quote="\"The only way to do great work is to love what you do.\"",
        recommendations=example_recommendations
    )
    print(formatted_output)

    print("\n--- Test without Logo, with Recommendations ---")
    formatted_output_no_logo = format_info_output(
        info_data=example_info,
        logo_lines=None,
        inspirational_quote="\"Simplicity is the soul of efficiency.\"",
        recommendations=example_recommendations
    )
    print(formatted_output_no_logo)

    print("\n--- Test with Logo, no Recommendations ---")
    formatted_output_no_rec = format_info_output(
        info_data=example_info,
        logo_lines=logo,
        inspirational_quote="\"Every line of code is a step towards a better future.\"",
        recommendations=[] # Empty list for no recommendations
    )
    print(formatted_output_no_rec)
