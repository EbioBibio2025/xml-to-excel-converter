"""
استایل‌های رابط کاربری - راست‌چین
"""

MAIN_STYLE = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #667eea, stop:1 #764ba2);
}

QWidget {
    font-family: 'Segoe UI', 'Arial';
}

QFrame#main_frame {
    background-color: white;
    border-radius: 15px;
    padding: 20px;
}

QLabel#title_label {
    font-size: 28px;
    font-weight: bold;
    color: #2c3e50;
    padding: 10px;
}

QLabel#subtitle_label {
    font-size: 14px;
    color: #7f8c8d;
    padding-bottom: 15px;
}

QGroupBox {
    font-size: 14px;
    font-weight: bold;
    color: #2c3e50;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    margin-top: 10px;
    padding-top: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 10px 0 10px;
}

QLabel {
    color: #2c3e50;
    font-size: 12px;
}

QLineEdit {
    padding: 8px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 12px;
    background-color: #f8f9fa;
}

QLineEdit:focus {
    border-color: #667eea;
    background-color: white;
}

QPushButton {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: bold;
    color: white;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #667eea, stop:1 #764ba2);
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #5a67d8, stop:1 #6b46a1);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #4c51bf, stop:1 #553c9a);
}

QPushButton#danger_btn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #e74c3c, stop:1 #c0392b);
}

QPushButton#danger_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #c0392b, stop:1 #a93226);
}

QPushButton#success_btn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #27ae60, stop:1 #229954);
}

QPushButton#success_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #229954, stop:1 #1e8449);
}

QComboBox {
    padding: 8px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 12px;
    background-color: #f8f9fa;
    min-width: 150px;
}

QComboBox:hover {
    border-color: #667eea;
}

QComboBox:focus {
    border-color: #667eea;
    background-color: white;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #667eea;
    margin-right: 10px;
}

QProgressBar {
    border: none;
    border-radius: 10px;
    background-color: #f0f0f0;
    height: 20px;
}

QProgressBar::chunk {
    border-radius: 10px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #667eea, stop:1 #764ba2);
}

QTextEdit {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Consolas', monospace;
    font-size: 11px;
    background-color: #f8f9fa;
}

QTextEdit:focus {
    border-color: #667eea;
}

QCheckBox {
    font-size: 12px;
    color: #2c3e50;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #e0e0e0;
    background-color: white;
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #667eea, stop:1 #764ba2);
    border-color: #667eea;
}

QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #667eea, stop:1 #764ba2);
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QMessageBox {
    background-color: white;
}

QMessageBox QPushButton {
    min-width: 80px;
    padding: 8px 15px;
}
"""

LOG_STYLE = """
QTextEdit {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 2px solid #333;
    font-family: 'Consolas', monospace;
    font-size: 11px;
}

QTextEdit[logLevel="INFO"] {
    color: #4fc3f7;
}

QTextEdit[logLevel="SUCCESS"] {
    color: #81c784;
}

QTextEdit[logLevel="WARNING"] {
    color: #ffb74d;
}

QTextEdit[logLevel="ERROR"] {
    color: #e57373;
}
"""