from setuptools import setup, find_packages

setup(
    name="xml-to-excel-converter",
    version="1.0.0",
    author="دانشجو",
    description="ابزار تبدیل فایل‌های XML به Excel",
    packages=find_packages(),
    install_requires=[
        'pandas>=2.0.0',
        'openpyxl>=3.1.0',
        'lxml>=4.9.0',
        'xmltodict>=0.13.0'
    ],
    entry_points={
        'console_scripts': [
            'xml2excel=src.main:main',
        ],
    },
    python_requires='>=3.8',
)