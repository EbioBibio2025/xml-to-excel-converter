"""
برنامه اصلی تبدیل XML به Excel
این برنامه یک رابط کاربری خط فرمان برای تبدیل فایل‌های XML به Excel فراهم می‌کند.
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# اضافه کردن مسیر src به sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.xml_parser import XMLParser
from src.excel_generator import ExcelGenerator

# تنظیم لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def validate_xml_file(file_path: str) -> bool:
    """
    اعتبارسنجی فایل XML
    
    Args:
        file_path (str): مسیر فایل
        
    Returns:
        bool: معتبر بودن فایل
    """
    if not os.path.exists(file_path):
        logger.error(f"فایل {file_path} وجود ندارد")
        return False
    
    if not file_path.lower().endswith('.xml'):
        logger.error(f"فایل {file_path} پسوند XML ندارد")
        return False
    
    return True


def main():
    """
    تابع اصلی برنامه
    """
    # تعریف آرگومان‌های خط فرمان
    parser = argparse.ArgumentParser(
        description='تبدیل فایل XML به Excel با استفاده از پایتون',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
مثال‌های استفاده:
  python main.py -i data/sample.xml -o output.xlsx
  python main.py -i data/sample.xml -t food -s
  python main.py -i data/sample.xml -f openpyxl
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='مسیر فایل XML ورودی'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='converted.xlsx',
        help='نام فایل Excel خروجی (پیش‌فرض: converted.xlsx)'
    )
    
    parser.add_argument(
        '-t', '--tag',
        default=None,
        help='تگ هدف برای استخراج داده (اختیاری)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['pandas', 'openpyxl', 'both'],
        default='pandas',
        help='روش تولید Excel (پیش‌فرض: pandas)'
    )
    
    parser.add_argument(
        '-s', '--summary',
        action='store_true',
        help='تولید گزارش خلاصه همراه با فایل اصلی'
    )
    
    parser.add_argument(
        '--output-dir',
        default='data/output',
        help='دایرکتوری خروجی (پیش‌فرض: data/output)'
    )
    
    # پردازش آرگومان‌ها
    args = parser.parse_args()
    
    try:
        # 1. اعتبارسنجی فایل ورودی
        if not validate_xml_file(args.input):
            return 1
        
        # 2. ایجاد دایرکتوری خروجی
        os.makedirs(args.output_dir, exist_ok=True)
        
        logger.info("=" * 60)
        logger.info("شروع فرآیند تبدیل XML به Excel")
        logger.info(f"فایل ورودی: {args.input}")
        logger.info(f"تگ هدف: {args.tag if args.tag else 'همه'}")
        logger.info(f"روش خروجی: {args.format}")
        logger.info("=" * 60)
        
        # 3. پارس کردن XML
        logger.info("مرحله 1: پارس کردن فایل XML...")
        xml_parser = XMLParser(args.input)
        
        # نمایش اطلاعات ساختار
        structure = xml_parser.get_structure_info()
        logger.info(f"ساختار XML:")
        logger.info(f"  - تگ ریشه: {structure['root_tag']}")
        logger.info(f"  - تعداد کل المان‌ها: {structure['total_elements']}")
        logger.info(f"  - تگ‌های منحصر‌به‌فرد: {structure['unique_tags']}")
        logger.info(f"  - حداکثر عمق: {structure['max_depth']}")
        
        # 4. استخراج داده‌ها
        logger.info("مرحله 2: استخراج داده‌ها...")
        data = xml_parser.extract_flat_data(args.tag)
        
        if not data:
            logger.warning("هیچ داده‌ای برای تبدیل یافت نشد!")
            return 1
        
        logger.info(f"{len(data)} رکورد استخراج شد")
        
        # نمایش نمونه داده
        if data:
            logger.info("نمونه داده (اولین رکورد):")
            for key, value in data[0].items():
                logger.info(f"  {key}: {value}")
        
        # 5. تولید فایل Excel
        logger.info("مرحله 3: تولید فایل Excel...")
        excel_gen = ExcelGenerator(args.output_dir)
        
        output_files = []
        
        if args.format in ['pandas', 'both']:
            pandas_file = excel_gen.generate_with_pandas(data, args.output)
            output_files.append(pandas_file)
        
        if args.format in ['openpyxl', 'both']:
            styled_name = f"styled_{args.output}"
            openpyxl_file = excel_gen.generate_with_openpyxl(data, styled_name)
            output_files.append(openpyxl_file)
        
        # 6. تولید گزارش خلاصه (اختیاری)
        if args.summary:
            logger.info("مرحله 4: تولید گزارش خلاصه...")
            summary_file = excel_gen.generate_summary_report(data, f"summary_{args.output}")
            output_files.append(summary_file)
        
        # 7. نمایش نتایج
        logger.info("=" * 60)
        logger.info("✅ فرآیند تبدیل با موفقیت انجام شد!")
        logger.info("فایل‌های ایجاد شده:")
        for file_path in output_files:
            logger.info(f"  📁 {file_path}")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ خطا در اجرای برنامه: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())