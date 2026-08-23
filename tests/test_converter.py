import unittest
import os
import tempfile
import shutil
from src.xml_parser import XMLParser
from src.excel_generator import ExcelGenerator


class TestXMLToExcel(unittest.TestCase):
    
    def setUp(self):
        """تنظیمات اولیه قبل از هر تست"""
        self.test_dir = tempfile.mkdtemp()
        self.xml_content = """<?xml version="1.0"?>
        <test>
            <item id="1">
                <name>Test1</name>
                <value>100</value>
            </item>
            <item id="2">
                <name>Test2</name>
                <value>200</value>
            </item>
        </test>
        """
        
        self.xml_file = os.path.join(self.test_dir, 'test.xml')
        with open(self.xml_file, 'w', encoding='utf-8') as f:
            f.write(self.xml_content)
    
    def tearDown(self):
        """پاکسازی بعد از هر تست"""
        shutil.rmtree(self.test_dir)
    
    def test_xml_parser(self):
        """تست پارسر XML"""
        parser = XMLParser(self.xml_file)
        data = parser.extract_flat_data('item')
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['@id'], '1')
        self.assertEqual(data[0]['name'], 'Test1')
    
    def test_excel_generator(self):
        """تست تولید Excel"""
        test_data = [
            {'نام': 'محصول 1', 'قیمت': 100},
            {'نام': 'محصول 2', 'قیمت': 200}
        ]
        
        generator = ExcelGenerator(self.test_dir)
        filepath = generator.generate_with_pandas(test_data, 'test.xlsx')
        
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(filepath.endswith('.xlsx'))


if __name__ == '__main__':
    unittest.main()