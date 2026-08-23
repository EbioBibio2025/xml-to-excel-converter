"""
ماژول پارس کردن فایل‌های XML
این ماژول مسئول خواندن و استخراج داده‌ها از فایل‌های XML است.
"""

import xml.etree.ElementTree as ET
import xmltodict
import json
from typing import Dict, List, Any, Optional
import logging

# تنظیم لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XMLParser:
    """
    کلاس اصلی برای پارس کردن فایل‌های XML با روش‌های مختلف
    """
    
    def __init__(self, file_path: str):
        """
        سازنده کلاس
        
        Args:
            file_path (str): مسیر فایل XML
        """
        self.file_path = file_path
        self.tree = None
        self.root = None
        self._load_xml()
    
    def _load_xml(self) -> None:
        """
        بارگذاری فایل XML و ایجاد درخت
        """
        try:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            logger.info(f"فایل XML با موفقیت بارگذاری شد: {self.file_path}")
        except ET.ParseError as e:
            logger.error(f"خطا در پارس کردن XML: {e}")
            raise
        except FileNotFoundError as e:
            logger.error(f"فایل پیدا نشد: {e}")
            raise
    
    def parse_with_etree(self, target_tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        پارس کردن XML با استفاده از ElementTree
        
        Args:
            target_tag (str): نام تگ هدف برای استخراج داده‌ها
            
        Returns:
            List[Dict]: لیست دیکشنری‌های حاوی داده‌ها
        """
        data = []
        
        # اگر تگ هدف مشخص نشده، از ریشه استفاده کن
        if target_tag is None:
            elements = [self.root]
        else:
            elements = self.root.findall(f'.//{target_tag}')
        
        for element in elements:
            row = self._element_to_dict(element)
            data.append(row)
        
        logger.info(f"{len(data)} رکورد با استفاده از ElementTree استخراج شد")
        return data
    
    def _element_to_dict(self, element: ET.Element) -> Dict[str, Any]:
        """
        تبدیل یک المان XML به دیکشنری
        
        Args:
            element (ET.Element): المان XML
            
        Returns:
            Dict: دیکشنری شامل داده‌های المان
        """
        row = {}
        
        # اضافه کردن ویژگی‌های المان
        for attr_name, attr_value in element.attrib.items():
            row[f'@{attr_name}'] = attr_value
        
        # اضافه کردن زیرالمان‌ها
        for child in element:
            if len(child) == 0:  # المان برگ (بدون زیرالمان)
                row[child.tag] = child.text
            else:
                # اگر زیرالمان دارد، به صورت بازگشتی پردازش کن
                # اما اگر چندین زیرالمان با تگ یکسان داریم (مثل ingredients/item)
                if child.tag in row:
                    # اگر قبلاً این تگ وجود دارد، آن را به لیست تبدیل کن
                    if not isinstance(row[child.tag], list):
                        row[child.tag] = [row[child.tag]]
                    row[child.tag].append(self._element_to_dict(child))
                else:
                    row[child.tag] = self._element_to_dict(child)
        
        # اضافه کردن متن اصلی المان (اگر وجود داشته باشد و ویژگی نداشته باشد)
        if element.text and element.text.strip() and not element.attrib:
            row['text'] = element.text.strip()
        
        return row
    
    def parse_with_xmltodict(self) -> Dict:
        """
        پارس کردن XML با استفاده از کتابخانه xmltodict (ساده‌تر)
        
        Returns:
            Dict: دیکشنری کامل XML
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
                data = xmltodict.parse(xml_content)
                logger.info("XML با موفقیت به دیکشنری تبدیل شد")
                return data
        except Exception as e:
            logger.error(f"خطا در تبدیل XML با xmltodict: {e}")
            raise
    
    def extract_flat_data(self, target_tag: str) -> List[Dict]:
        """
        استخراج داده‌های مسطح از XML (مناسب برای تبدیل به جدول)
        
        Args:
            target_tag (str): نام تگ هدف
            
        Returns:
            List[Dict]: لیست دیکشنری‌های مسطح شده
        """
        data = self.parse_with_etree(target_tag)
        flat_data = []
        
        for item in data:
            flat_row = self._flatten_dict(item)
            flat_data.append(flat_row)
        
        return flat_data
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """
        مسطح کردن یک دیکشنری تو در تو
        
        Args:
            d (Dict): دیکشنری تو در تو
            parent_key (str): کلید والد
            sep (str): جداکننده
            
        Returns:
            Dict: دیکشنری مسطح شده
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # برای لیست‌ها، آنها را به رشته تبدیل می‌کنیم
                # اگر لیست شامل دیکشنری باشد، آن را به صورت جداگانه پردازش کن
                if v and isinstance(v[0], dict):
                    # برای هر آیتم در لیست، یک رکورد جدید ایجاد کن
                    for idx, item in enumerate(v):
                        if isinstance(item, dict):
                            for sub_k, sub_v in self._flatten_dict(item, f"{new_key}_{idx+1}", sep=sep).items():
                                items.append((sub_k, sub_v))
                else:
                    items.append((new_key, ', '.join(str(item) for item in v)))
            else:
                items.append((new_key, v))
        return dict(items)
    
    def get_structure_info(self) -> Dict:
        """
        دریافت اطلاعات ساختاری XML (برای نمایش به کاربر)
        
        Returns:
            Dict: اطلاعات ساختار
        """
        structure = {
            'root_tag': self.root.tag,
            'total_elements': len(list(self.root.iter())),
            'unique_tags': set(),
            'max_depth': 0
        }
        
        def traverse(element, depth=0):
            structure['unique_tags'].add(element.tag)
            structure['max_depth'] = max(structure['max_depth'], depth)
            for child in element:
                traverse(child, depth + 1)
        
        traverse(self.root)
        structure['unique_tags'] = list(structure['unique_tags'])
        
        return structure


if __name__ == "__main__":
    # تست ماژول
    parser = XMLParser('../data/sample.xml')
    print("ساختار XML:")
    print(parser.get_structure_info())
    print("\nداده‌های استخراج شده:")
    data = parser.extract_flat_data('food')
    for row in data:
        print(row)