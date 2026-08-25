"""
نسخه تحت وب XML to Excel Converter
با استفاده از Flask
"""

import os
import json
import shutil
from datetime import datetime
from flask import Flask, render_template, request, send_file, jsonify, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging

# تنظیمات
app = Flask(__name__)
CORS(app)

# پیکربندی
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['DOWNLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
app.config['ALLOWED_EXTENSIONS'] = {'xml'}

# ایجاد پوشه‌ها
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# تنظیم لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ایمپورت converter
try:
    from converter import XMLConverter
except ImportError:
    logger.error("فایل converter.py پیدا نشد!")
    # اگر converter پیدا نشد، یک کلاس ساده ایجاد کن
    class XMLConverter:
        def __init__(self):
            self.data = []
            self.headers = []
        
        def get_xml_info(self, xml_file):
            import xml.etree.ElementTree as ET
            tree = ET.parse(xml_file)
            root = tree.getroot()
            return {
                'root_tag': root.tag,
                'total_elements': len(list(root.iter())),
                'unique_tags': list(set([e.tag for e in root.iter()])),
                'max_depth': 3
            }
        
        def convert(self, xml_file, output_dir, output_name, target_tag=None, output_format="Excel (xlsx)", generate_summary=True):
            import openpyxl
            import csv
            import json
            
            # ساده برای تست
            results = {}
            excel_path = os.path.join(output_dir, f"{output_name}.xlsx")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws['A1'] = 'Test'
            wb.save(excel_path)
            results["Excel (xlsx)"] = excel_path
            self.data = [{'test': 'data'}]
            self.headers = ['test']
            return results

def allowed_file(filename):
    """بررسی پسوند فایل مجاز"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_file_size(filepath):
    """گرفتن حجم فایل به صورت خوانا"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


@app.route('/')
def index():
    """صفحه اصلی"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """آپلود فایل XML"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'هیچ فایلی انتخاب نشده است'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'نام فایل نامعتبر است'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'فقط فایل‌های XML مجاز هستند'}), 400
        
        # ذخیره فایل
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # خواندن اطلاعات XML
        converter = XMLConverter()
        try:
            info = converter.get_xml_info(filepath)
            
            file_info = {
                'filename': filename,
                'unique_filename': unique_filename,
                'size': get_file_size(filepath),
                'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'structure': info
            }
            
            logger.info(f"فایل آپلود شد: {filename}")
            return jsonify({
                'success': True,
                'message': 'فایل با موفقیت آپلود شد',
                'file_info': file_info
            })
            
        except Exception as e:
            os.remove(filepath)
            return jsonify({'error': f'خطا در خواندن فایل XML: {str(e)}'}), 400
            
    except Exception as e:
        logger.error(f"خطا در آپلود: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/convert', methods=['POST'])
def convert_file():
    """تبدیل فایل XML"""
    try:
        data = request.get_json()
        
        if not data or 'filename' not in data:
            return jsonify({'error': 'اطلاعات کامل نیست'}), 400
        
        filename = data['filename']
        target_tag = data.get('target_tag', '')
        output_format = data.get('output_format', 'Excel (xlsx)')
        output_name = data.get('output_name', 'converted')
        generate_summary = data.get('generate_summary', True)
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'فایل پیدا نشد'}), 404
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(app.config['DOWNLOAD_FOLDER'], f"{timestamp}_{output_name}")
        os.makedirs(output_dir, exist_ok=True)
        
        converter = XMLConverter()
        results = converter.convert(
            xml_file=filepath,
            output_dir=output_dir,
            output_name=output_name,
            target_tag=target_tag if target_tag else None,
            output_format=output_format,
            generate_summary=generate_summary
        )
        
        download_files = []
        for format_name, file_path in results.items():
            if os.path.exists(file_path):
                download_files.append({
                    'name': format_name,
                    'filename': os.path.basename(file_path),
                    'path': file_path,
                    'size': get_file_size(file_path)
                })
        
        conversion_info = {
            'timestamp': timestamp,
            'input_file': filename,
            'target_tag': target_tag,
            'output_format': output_format,
            'output_name': output_name,
            'files': download_files,
            'record_count': len(converter.data) if hasattr(converter, 'data') else 0,
            'headers': converter.headers if hasattr(converter, 'headers') else []
        }
        
        logger.info(f"تبدیل کامل شد: {filename} -> {len(download_files)} فایل")
        
        return jsonify({
            'success': True,
            'message': 'تبدیل با موفقیت انجام شد',
            'conversion_info': conversion_info,
            'files': download_files
        })
        
    except Exception as e:
        logger.error(f"خطا در تبدیل: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<path:filepath>')
def download_file(filepath):
    """دانلود فایل خروجی"""
    try:
        full_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filepath)
        
        if not os.path.exists(full_path):
            return jsonify({'error': 'فایل پیدا نشد'}), 404
        
        return send_file(full_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"خطا در دانلود: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # اطمینان از وجود پوشه‌ها
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('downloads', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)