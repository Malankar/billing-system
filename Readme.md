# Billing System

A desktop application built with Python and Tkinter for managing bills and invoices. This system allows businesses to create, manage, and track bills with an easy-to-use graphical interface.

## Features

- **Customer Management**
  - Add customer details
  - Store customer information with bills
  - Quick customer lookup

- **Product Management**
  - Multiple product categories
  - Automatic tax calculation based on category
  - Real-time price calculation

- **Billing Features**
  - Generate new bills
  - Automatic tax calculation
  - Add multiple items to a bill
  - Calculate total amount
  - Print bills
  - Save bills for future reference

- **Search and Records**
  - Search bills by:
    - Bill number
    - Customer name
    - Phone number
  - View complete bill history
  - Print old bills
  - Detailed bill view

## Technical Requirements

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Required Libraries
```
pillow==11.1.0
tk==0.1.0
```

## Project Structure
```
billing_system/
│
├── assets/           # For images and icons
│   └── icon.png
│
├── database/         # Database directory
│   └── .gitkeep
│
├── src/
│   ├── __init__.py      # Package initialization
│   ├── billing_system.py # Main application code
│   └── config.py        # Configuration settings
│
├── requirements.txt  # Project dependencies
└── main.py          # Application entry point
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/malankar/billing-system.git
cd billing-system
```

2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python main.py
```

## Usage Guide

### 1. Creating a New Bill
- Enter customer details (name, phone)
- Select product category
- Enter product details (name, price, quantity)
- Click "Add Product" to add items
- Click "Generate Bill" to create the bill

### 2. Managing Bills
- Save bills using "Save Bill" button
- Print bills using "Print" button
- Clear form using "Clear" button
- Search old bills using "Search" button

### 3. Searching Bills
- Click "Search" to open search window
- Enter search criteria (bill number, customer name, or phone)
- View results in the table
- Double-click any bill to view details

### 4. Viewing Bill Details
- Shows complete bill information
- Displays all items with quantities and prices
- Shows tax calculations
- Option to print bill

## Database Structure

The application uses SQLite with two main tables:

1. **bills** table
```sql
CREATE TABLE bills (
    bill_no TEXT PRIMARY KEY,
    customer_name TEXT,
    customer_phone TEXT,
    date TEXT,
    total_amount REAL
)
```

2. **bill_items** table
```sql
CREATE TABLE bill_items (
    bill_no TEXT,
    product_name TEXT,
    category TEXT,
    price REAL,
    quantity INTEGER,
    tax REAL,
    FOREIGN KEY (bill_no) REFERENCES bills(bill_no)
)
```

## Tax Rates

Default tax rates by category:
- Electronics: 18%
- Clothing: 12%
- Groceries: 5%
- Books: 5%

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues and Solutions

1. **Tkinter not found**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS
brew install python-tk
```

2. **Database permission errors**
- Ensure write permissions in the database directory
- Check if database file is not locked

3. **Print functionality not working**
- Check write permissions in the output directory
- Ensure proper file extension is selected

## License

This project is licensed under the MIT License - see the LICENSE file for details