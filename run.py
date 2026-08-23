#!/usr/bin/env python
"""
فایل اجرای اصلی برنامه
"""

import sys
import os

# اضافه کردن مسیر پروژه
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import run_app

if __name__ == "__main__":
    run_app()