#!/usr/bin/env python3

import sys
import argparse
import os
import concurrent.futures # استيراد المكتبة الجديدة للتعامل مع المهام المتوازية

# إضافة مسار مجلد السكريبت إلى sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# استيراد الدوال من وحدات جمع المعلومات
from core.system_info import get_system_info, get_inspirational_quote
from core.hardware_info import get_hardware_info
from core.desktop_info import get_desktop_info
from core.network_info import get_network_info

# استيراد وحدات العرض والتنسيق
from display.ascii_art import get_ascii_logo, COLORS
from display.formatter import format_info_output

# استيراد الإعدادات الافتراضية
from config.default_config import DEFAULT_COLORS

def main():
    """
    The main function to run Helfetch.
    It collects all system information, formats it with the logo, and prints it.
    Supports command-line arguments for customization.
    """
    parser = argparse.ArgumentParser(
        description="A custom system information fetcher for Helwan Linux."
    )
    parser.add_argument(
        "--no-logo",
        action="store_true",
        help="Do not display the Helwan Linux ASCII art logo."
    )
    args = parser.parse_args()

    # استخدام ThreadPoolExecutor لتشغيل دوال جمع المعلومات بالتوازي
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # إرسال كل دالة كـ "مهمة" إلى المجمع
        future_system_data = executor.submit(get_system_info)
        future_hardware_data = executor.submit(get_hardware_info)
        future_desktop_data = executor.submit(get_desktop_info)
        future_network_data = executor.submit(get_network_info)
        future_quote = executor.submit(get_inspirational_quote)

        # الانتظار حتى تكتمل جميع المهام وجمع النتائج
        system_data = future_system_data.result()
        hardware_data = future_hardware_data.result()
        desktop_data = future_desktop_data.result()
        network_data = future_network_data.result()
        inspirational_quote = future_quote.result()

    all_info = {
        **system_data,
        **hardware_data,
        **desktop_data,
        **network_data
    }

    helwan_logo = None
    if not args.no_logo:
        helwan_logo = get_ascii_logo("Helwan Linux")

    # تحديث الوسائط هنا لتتماشى مع التغييرات الأخيرة في formatter.py
    formatted_output = format_info_output(
        info_data=all_info,
        logo_lines=helwan_logo,
        inspirational_quote=inspirational_quote,
        # لم نعد نمرر هذه الألوان بشكل منفصل لأنها تُسحب من DEFAULT_COLORS داخل formatter.py
        # info_key_color=DEFAULT_COLORS["info_key_color"],
        # info_value_color=DEFAULT_COLORS["info_value_color"]
    )

    print(formatted_output)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"حدث خطأ: {e}", file=sys.stderr)
        sys.exit(1)
