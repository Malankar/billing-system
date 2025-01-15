"""
Configuration settings for the Billing System
"""

# Database Configuration
DB_NAME = 'billing_system.db'
DB_PATH = './'  # Database will be created in root directory

# Application Settings
APP_NAME = 'Billing System'
APP_VERSION = '1.0.0'
WINDOW_SIZE = '1200x700'

# GUI Configuration
FONT_FAMILY = 'times new roman'
TITLE_FONT_SIZE = 30
HEADER_FONT_SIZE = 15
NORMAL_FONT_SIZE = 12

# Colors
BG_COLOR = 'white'
FG_COLOR = 'black'
BUTTON_BG = 'lightgray'
BUTTON_FG = 'black'

# Product Categories and Tax Rates
PRODUCT_CATEGORIES = {
    'Electronics': 18,  # 18% tax
    'Clothing': 12,    # 12% tax
    'Groceries': 5,    # 5% tax
    'Books': 5         # 5% tax
}

# Bill Format Settings
BILL_WIDTH = 60  # Characters
BILL_HEADER = '\t\tBILL'
BILL_SEPARATOR = '=' * BILL_WIDTH

# File Save Settings
DEFAULT_SAVE_EXTENSION = '.txt'
FILE_TYPES = [
    ('Text files', '*.txt'),
    ('All files', '*.*')
]

# Database Tables
TABLES = {
    'bills': '''
        CREATE TABLE IF NOT EXISTS bills (
            bill_no TEXT PRIMARY KEY,
            customer_name TEXT,
            customer_phone TEXT,
            date TEXT,
            total_amount REAL
        )
    ''',
    'bill_items': '''
        CREATE TABLE IF NOT EXISTS bill_items (
            bill_no TEXT,
            product_name TEXT,
            category TEXT,
            price REAL,
            quantity INTEGER,
            tax REAL,
            FOREIGN KEY (bill_no) REFERENCES bills(bill_no)
        )
    '''
}

# Validation Settings
PHONE_LENGTH = 10
MAX_PRODUCT_QUANTITY = 1000
MIN_PRODUCT_PRICE = 0.01
MAX_PRODUCT_PRICE = 1000000

# Error Messages
ERROR_MESSAGES = {
    'required_fields': 'All fields are required!',
    'invalid_price': 'Invalid price entered!',
    'invalid_quantity': 'Invalid quantity entered!',
    'invalid_phone': 'Invalid phone number!',
    'duplicate_bill': 'Bill number already exists!',
    'no_bill': 'No bill to save!',
    'no_products': 'Please add products to the bill!',
    'db_error': 'Database error occurred: {}',
    'save_error': 'Error saving file: {}'
}

# Success Messages
SUCCESS_MESSAGES = {
    'bill_saved': 'Bill saved successfully!',
    'bill_printed': 'Bill saved for printing!',
    'fields_cleared': 'All fields cleared!'
}