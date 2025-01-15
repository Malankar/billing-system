import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import random
import os
from tkinter import filedialog

class BillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x700')
        self.root.title('Billing System')
        
        # Database initialization
        self.create_database()
        
        # Variables
        self.bill_no = tk.StringVar()
        self.bill_no.set(str(random.randint(1000, 9999)))
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.date = tk.StringVar()
        self.date.set(datetime.now().strftime("%d/%m/%Y"))
        
        self.product_category = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_price = tk.StringVar()
        self.product_qty = tk.StringVar()
        self.tax = tk.StringVar()
        
        self.total_list = []
        
        # GUI Components
        self.create_title_frame()
        self.create_customer_frame()
        self.create_product_frame()
        self.create_bill_frame()
        self.create_buttons_frame()
        
    def create_database(self):
        conn = sqlite3.connect('billing_system.db')
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills
            (bill_no TEXT PRIMARY KEY,
             customer_name TEXT,
             customer_phone TEXT,
             date TEXT,
             total_amount REAL)
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bill_items
            (bill_no TEXT,
             product_name TEXT,
             category TEXT,
             price REAL,
             quantity INTEGER,
             tax REAL,
             FOREIGN KEY (bill_no) REFERENCES bills(bill_no))
        ''')
        
        conn.commit()
        conn.close()
    
    def create_title_frame(self):
        title_frame = tk.Frame(self.root, bd=8, relief=tk.GROOVE, bg='white')
        title_frame.pack(fill=tk.X)
        
        title = tk.Label(title_frame, text='Billing System', 
                        font=('times new roman', 30, 'bold'),
                        bg='white', fg='black', pady=2)
        title.pack()
        
    def create_customer_frame(self):
        customer_frame = tk.LabelFrame(self.root, text='Customer Details',
                                     font=('times new roman', 15, 'bold'),
                                     bg='white', fg='black', bd=8, relief=tk.GROOVE)
        customer_frame.pack(fill=tk.X)
        
        # Labels and Entries
        tk.Label(customer_frame, text='Bill Number:', 
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=0, padx=20, pady=5)
        tk.Entry(customer_frame, textvariable=self.bill_no,
                font=('times new roman', 12), state='readonly').grid(row=0, column=1, padx=5)
        
        tk.Label(customer_frame, text='Customer Name:',
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=2, padx=20, pady=5)
        tk.Entry(customer_frame, textvariable=self.customer_name,
                font=('times new roman', 12)).grid(row=0, column=3, padx=5)
        
        tk.Label(customer_frame, text='Phone No:',
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=4, padx=20, pady=5)
        tk.Entry(customer_frame, textvariable=self.customer_phone,
                font=('times new roman', 12)).grid(row=0, column=5, padx=5)
        
        tk.Label(customer_frame, text='Date:',
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=6, padx=20, pady=5)
        tk.Entry(customer_frame, textvariable=self.date,
                font=('times new roman', 12), state='readonly').grid(row=0, column=7, padx=5)
    
    def create_product_frame(self):
        product_frame = tk.LabelFrame(self.root, text='Product Details',
                                    font=('times new roman', 15, 'bold'),
                                    bg='white', fg='black', bd=8, relief=tk.GROOVE)
        product_frame.pack(fill=tk.X)
        
        # Product Category
        categories = ['Electronics', 'Clothing', 'Groceries', 'Books']
        tk.Label(product_frame, text='Category:',
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=0, padx=20, pady=5)
        category_combo = ttk.Combobox(product_frame, textvariable=self.product_category,
                                    values=categories, state='readonly',
                                    font=('times new roman', 12))
        category_combo.grid(row=0, column=1, padx=5)
        category_combo.bind('<<ComboboxSelected>>', self.update_tax)
        
        # Product Details
        tk.Label(product_frame, text='Product Name:',
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=2, padx=20, pady=5)
        tk.Entry(product_frame, textvariable=self.product_name,
                font=('times new roman', 12)).grid(row=0, column=3, padx=5)
        
        tk.Label(product_frame, text='Price:',
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=4, padx=20, pady=5)
        tk.Entry(product_frame, textvariable=self.product_price,
                font=('times new roman', 12)).grid(row=0, column=5, padx=5)
        
        tk.Label(product_frame, text='Quantity:',
                font=('times new roman', 12, 'bold'),
                bg='white').grid(row=0, column=6, padx=20, pady=5)
        tk.Entry(product_frame, textvariable=self.product_qty,
                font=('times new roman', 12)).grid(row=0, column=7, padx=5)
        
        # Add Product Button
        tk.Button(product_frame, text='Add Product', command=self.add_product,
                 font=('times new roman', 12, 'bold'),
                 bg='lightgray', fg='black').grid(row=0, column=8, padx=20, pady=5)
    
    def create_bill_frame(self):
        bill_frame = tk.Frame(self.root, bd=8, relief=tk.GROOVE)
        bill_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bill Area
        bill_title = tk.Label(bill_frame, text='Bill Area',
                            font=('times new roman', 15, 'bold'),
                            bd=7, relief=tk.GROOVE)
        bill_title.pack(fill=tk.X)
        
        # Scrolled Text for Bill
        self.bill_area = tk.Text(bill_frame,
                                font=('times new roman', 12))
        self.bill_area.pack(fill=tk.BOTH, expand=True)
    
    def create_buttons_frame(self):
        buttons_frame = tk.Frame(self.root, bd=8, relief=tk.GROOVE, bg='white')
        buttons_frame.pack(fill=tk.X)
        
        # Buttons
        tk.Button(buttons_frame, text='Generate Bill',
                 command=self.generate_bill,
                 font=('times new roman', 12, 'bold'),
                 bg='lightgray', fg='black', pady=5).grid(row=0, column=0, padx=20, pady=5)
        
        tk.Button(buttons_frame, text='Save Bill',
                 command=self.save_bill,
                 font=('times new roman', 12, 'bold'),
                 bg='lightgray', fg='black', pady=5).grid(row=0, column=1, padx=20, pady=5)
        
        tk.Button(buttons_frame, text='Print',
                 command=self.print_bill,
                 font=('times new roman', 12, 'bold'),
                 bg='lightgray', fg='black', pady=5).grid(row=0, column=2, padx=20, pady=5)
        
        tk.Button(buttons_frame, text='Clear',
                 command=self.clear,
                 font=('times new roman', 12, 'bold'),
                 bg='lightgray', fg='black', pady=5).grid(row=0, column=3, padx=20, pady=5)
        
        tk.Button(buttons_frame, text='Search',
                 command=self.search_bill,
                 font=('times new roman', 12, 'bold'),
                 bg='lightgray', fg='black', pady=5).grid(row=0, column=4, padx=20, pady=5)
        
        tk.Button(buttons_frame, text='Exit',
                 command=self.root.destroy,
                 font=('times new roman', 12, 'bold'),
                 bg='lightgray', fg='black', pady=5).grid(row=0, column=5, padx=20, pady=5)
    
    def update_tax(self, event=None):
        category = self.product_category.get()
        tax_rates = {
            'Electronics': 18,
            'Clothing': 12,
            'Groceries': 5,
            'Books': 5
        }
        self.tax.set(tax_rates.get(category, 0))
    
    def add_product(self):
        if not all([self.product_category.get(), self.product_name.get(),
                   self.product_price.get(), self.product_qty.get()]):
            messagebox.showerror('Error', 'All product fields are required!')
            return
        
        try:
            price = float(self.product_price.get())
            qty = int(self.product_qty.get())
            tax_rate = float(self.tax.get())
            
            tax_amount = (price * qty * tax_rate) / 100
            total = price * qty + tax_amount
            
            product_info = {
                'category': self.product_category.get(),
                'name': self.product_name.get(),
                'price': price,
                'quantity': qty,
                'tax': tax_amount,
                'total': total
            }
            
            self.total_list.append(product_info)
            self.update_bill_area()
            
            # Clear product entries
            self.product_name.set('')
            self.product_price.set('')
            self.product_qty.set('')
            
        except ValueError:
            messagebox.showerror('Error', 'Invalid price or quantity!')
    
    def update_bill_area(self):
        self.bill_area.delete(1.0, tk.END)
        self.bill_area.insert(tk.END, '\t\tBILL\n')
        self.bill_area.insert(tk.END, f'\nBill No: {self.bill_no.get()}')
        self.bill_area.insert(tk.END, f'\nCustomer Name: {self.customer_name.get()}')
        self.bill_area.insert(tk.END, f'\nPhone No: {self.customer_phone.get()}')
        self.bill_area.insert(tk.END, f'\nDate: {self.date.get()}\n')
        self.bill_area.insert(tk.END, '\n' + '=' * 60)
        self.bill_area.insert(tk.END, '\nProduct\t\tQty\tPrice\tTax\tTotal')
        self.bill_area.insert(tk.END, '\n' + '=' * 60)
        
        total_amount = 0
        for item in self.total_list:
            self.bill_area.insert(tk.END, f'\n{item["name"]}\t\t{item["quantity"]}\t'
                                        f'{item["price"]}\t{item["tax"]:.2f}\t{item["total"]:.2f}')
            total_amount += item["total"]
        
        self.bill_area.insert(tk.END, '\n' + '=' * 60)
        self.bill_area.insert(tk.END, f'\nTotal Amount: Rs. {total_amount:.2f}')
    
    def generate_bill(self):
        if not self.customer_name.get() or not self.customer_phone.get() or not self.total_list:
            messagebox.showerror('Error', 'Please add customer details and products!')
            return
        self.update_bill_area()
    
    def save_bill(self):
        if not self.total_list:
            messagebox.showerror('Error', 'No bill to save!')
            return
        
        try:
            conn = sqlite3.connect('billing_system.db')
            cursor = conn.cursor()
            
            # Check for duplicate bill number
            cursor.execute('SELECT bill_no FROM bills WHERE bill_no=?', (self.bill_no.get(),))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Bill number already exists!')
                return
            
            # Calculate total amount
            total_amount = sum(item['total'] for item in self.total_list)
            
            # Save bill header
            cursor.execute('''INSERT INTO bills (bill_no, customer_name, customer_phone, date, total_amount)
                            VALUES (?, ?, ?, ?, ?)''',
                         (self.bill_no.get(), self.customer_name.get(),
                          self.customer_phone.get(), self.date.get(), total_amount))
            
            # Save bill items
            for item in self.total_list:
                cursor.execute('''INSERT INTO bill_items 
                                (bill_no, product_name, category, price, quantity, tax)
                                VALUES (?, ?, ?, ?, ?, ?)''',
                             (self.bill_no.get(), item['name'], item['category'],
                              item['price'], item['quantity'], item['tax']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo('Success', 'Bill saved successfully!')
            self.clear()
            
        except sqlite3.Error as e:
            messagebox.showerror('Database Error', f'Error saving bill: {str(e)}')
            
    def print_bill(self):
        if not self.total_list:
            messagebox.showerror('Error', 'No bill to print!')
            return
        
        bill_text = self.bill_area.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
            initialfile=f'Bill_{self.bill_no.get()}.txt'
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(bill_text)
                messagebox.showinfo('Success', 'Bill saved for printing!')
            except Exception as e:
                messagebox.showerror('Error', f'Error saving bill: {str(e)}')
    
    def search_bill(self):
        search_window = tk.Toplevel(self.root)
        search_window.title('Search Bills')
        search_window.geometry('1000x600')
        
        # Search frame
        search_frame = tk.LabelFrame(search_window, text='Search Criteria',
                                  font=('times new roman', 12, 'bold'),
                                  bd=8, relief=tk.GROOVE)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Search inputs
        search_vars = {
            'Bill No': tk.StringVar(),
            'Customer Name': tk.StringVar(),
            'Phone': tk.StringVar()
        }
        
        # Create search fields
        for i, (label, var) in enumerate(search_vars.items()):
            tk.Label(search_frame, text=f'{label}:',
                    font=('times new roman', 12)).grid(row=0, column=i*2, padx=5, pady=5)
            entry = tk.Entry(search_frame, textvariable=var,
                    font=('times new roman', 12))
            entry.grid(row=0, column=i*2+1, padx=5, pady=5)
            # Add binding to trigger search on key release
            entry.bind('<KeyRelease>', lambda e: self.perform_search(result_tree, search_vars))
        
        # Search and Reset buttons
        tk.Button(search_frame, text='Search',
                command=lambda: self.perform_search(result_tree, search_vars),
                font=('times new roman', 12, 'bold'),
                bg='lightgray', fg='black').grid(row=0, column=6, padx=5, pady=5)
        
        tk.Button(search_frame, text='Reset',
                command=lambda: self.reset_search(result_tree, search_vars),
                font=('times new roman', 12, 'bold'),
                bg='lightgray', fg='black').grid(row=0, column=7, padx=5, pady=5)
        
        # Results frame
        result_frame = tk.LabelFrame(search_window, text='Bill Records',
                                  font=('times new roman', 12, 'bold'),
                                  bd=8, relief=tk.GROOVE)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results tree view with more details
        columns = ('Bill No', 'Customer', 'Phone', 'Date', 'Amount', 'Total Items')
        result_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        result_tree.heading('Bill No', text='Bill No')
        result_tree.heading('Customer', text='Customer Name')
        result_tree.heading('Phone', text='Phone')
        result_tree.heading('Date', text='Date')
        result_tree.heading('Amount', text='Total Amount')
        result_tree.heading('Total Items', text='Total Items')
        
        # Set column widths
        result_tree.column('Bill No', width=100)
        result_tree.column('Customer', width=200)
        result_tree.column('Phone', width=150)
        result_tree.column('Date', width=150)
        result_tree.column('Amount', width=150)
        result_tree.column('Total Items', width=100)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_tree.yview)
        x_scrollbar = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=result_tree.xview)
        result_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack tree and scrollbars
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        result_tree.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons frame
        button_frame = tk.Frame(search_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add buttons
        tk.Button(button_frame, text='View Details',
                command=lambda: self.show_bill_details(result_tree.selection()[0]) if result_tree.selection() else None,
                font=('times new roman', 12, 'bold'),
                bg='lightgray', fg='black').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text='Refresh',
                command=lambda: self.load_all_bills(result_tree),
                font=('times new roman', 12, 'bold'),
                bg='lightgray', fg='black').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text='Close',
                command=search_window.destroy,
                font=('times new roman', 12, 'bold'),
                bg='lightgray', fg='black').pack(side=tk.RIGHT, padx=5)
        
        # Load all bills initially
        self.load_all_bills(result_tree)
        
        # Bind double-click event
        result_tree.bind('<Double-1>', lambda e: self.show_bill_details(result_tree.selection()[0]) if result_tree.selection() else None)

    def perform_search(self, result_tree, search_vars):
        # Clear previous results
        for item in result_tree.get_children():
            result_tree.delete(item)
        
        try:
            conn = sqlite3.connect('billing_system.db')
            cursor = conn.cursor()
            
            # Build search query
            query = '''
                SELECT b.bill_no, b.customer_name, b.customer_phone, b.date, b.total_amount,
                      COUNT(bi.product_name) as total_items
                FROM bills b
                LEFT JOIN bill_items bi ON b.bill_no = bi.bill_no
                WHERE 1=1
            '''
            params = []
            
            if search_vars['Bill No'].get():
                query += ' AND b.bill_no LIKE ?'
                params.append(f'%{search_vars["Bill No"].get()}%')
            
            if search_vars['Customer Name'].get():
                query += ' AND LOWER(b.customer_name) LIKE LOWER(?)'
                params.append(f'%{search_vars["Customer Name"].get()}%')
            
            if search_vars['Phone'].get():
                query += ' AND b.customer_phone LIKE ?'
                params.append(f'%{search_vars["Phone"].get()}%')
            
            query += ' GROUP BY b.bill_no ORDER BY b.date DESC'
            
            cursor.execute(query, params)
            bills = cursor.fetchall()
            
            for bill in bills:
                # Format the amount to 2 decimal places
                formatted_bill = list(bill)
                formatted_bill[4] = f"₹{formatted_bill[4]:.2f}"  # Format amount with rupee symbol
                result_tree.insert('', tk.END, bill[0], values=formatted_bill)
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror('Database Error', f'Error searching bills: {str(e)}')

    def reset_search(self, result_tree, search_vars):
        # Clear search fields
        for var in search_vars.values():
            var.set('')
        
        # Reload all bills
        self.load_all_bills(result_tree)

    def load_all_bills(self, result_tree):
        # Clear previous results
        for item in result_tree.get_children():
            result_tree.delete(item)
        
        try:
            conn = sqlite3.connect('billing_system.db')
            cursor = conn.cursor()
            
            # Get bills with total items count
            cursor.execute('''
                SELECT b.bill_no, b.customer_name, b.customer_phone, b.date, b.total_amount,
                      COUNT(bi.product_name) as total_items
                FROM bills b
                LEFT JOIN bill_items bi ON b.bill_no = bi.bill_no
                GROUP BY b.bill_no
                ORDER BY b.date DESC
            ''')
            
            bills = cursor.fetchall()
            
            for bill in bills:
                # Format the amount to 2 decimal places
                formatted_bill = list(bill)
                formatted_bill[4] = f"₹{formatted_bill[4]:.2f}"  # Format amount with rupee symbol
                result_tree.insert('', tk.END, bill[0], values=formatted_bill)
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror('Database Error', f'Error loading bills: {str(e)}')

    def show_bill_details(self, bill_no):
        try:
            conn = sqlite3.connect('billing_system.db')
            cursor = conn.cursor()
            
            # Get bill header
            cursor.execute('''SELECT * FROM bills WHERE bill_no = ?''', (bill_no,))
            bill = cursor.fetchone()
            
            if not bill:
                messagebox.showerror('Error', 'Bill not found!')
                return
            
            # Get bill items
            cursor.execute('''SELECT * FROM bill_items WHERE bill_no = ?''', (bill_no,))
            items = cursor.fetchall()
            
            # Create bill details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f'Bill Details - {bill_no}')
            details_window.geometry('600x800')
            
            # Add a frame for the bill content
            content_frame = tk.Frame(details_window, bd=8, relief=tk.GROOVE)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Bill text area
            bill_text = tk.Text(content_frame, font=('times new roman', 12))
            bill_text.pack(fill=tk.BOTH, expand=True)
            
            # Add scrollbar
            scrollbar = tk.Scrollbar(bill_text)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            bill_text.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=bill_text.yview)
            
            # Format bill content
            bill_text.insert(tk.END, '\n\t\t   BILL DETAILS\n')
            bill_text.insert(tk.END, '\t\t   ============\n\n')
            bill_text.insert(tk.END, f'Bill No: {bill[0]}\n')
            bill_text.insert(tk.END, f'Customer Name: {bill[1]}\n')
            bill_text.insert(tk.END, f'Phone No: {bill[2]}\n')
            bill_text.insert(tk.END, f'Date: {bill[3]}\n')
            bill_text.insert(tk.END, '\n' + '=' * 60 + '\n')
            bill_text.insert(tk.END, f'{"Product":<20} {"Qty":>8} {"Price":>10} {"Tax":>10} {"Total":>10}\n')
            bill_text.insert(tk.END, '=' * 60 + '\n')
            
            total_items = 0
            for item in items:
                total_items += item[4]  # Add quantity
                subtotal = item[3] * item[4] + item[5]  # price * quantity + tax
                bill_text.insert(tk.END, f'{item[1]:<20} {item[4]:>8} {item[3]:>10.2f} {item[5]:>10.2f} {subtotal:>10.2f}\n')
            
            bill_text.insert(tk.END, '\n' + '=' * 60 + '\n')
            bill_text.insert(tk.END, f'Total Items: {total_items}\n')
            bill_text.insert(tk.END, f'Total Amount: ₹{bill[4]:.2f}\n')
            
            # Button frame
            button_frame = tk.Frame(details_window)
            button_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Add Print and Close buttons
            tk.Button(button_frame, text='Print Bill',
                    command=lambda: self.print_bill_details(bill_text.get(1.0, tk.END), bill_no),
                    font=('times new roman', 12, 'bold'),
                    bg='lightgray', fg='black').pack(side=tk.LEFT, padx=5)
            
            tk.Button(button_frame, text='Close',
                    command=details_window.destroy,
                    font=('times new roman', 12, 'bold'),
                    bg='lightgray', fg='black').pack(side=tk.RIGHT, padx=5)
            
            bill_text.config(state=tk.DISABLED)
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror('Database Error', f'Error showing bill details: {str(e)}')

    def print_bill_details(self, bill_text, bill_no):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')],
            initialfile=f'Bill_{bill_no}.txt'
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(bill_text)
                messagebox.showinfo('Success', 'Bill saved for printing!')
            except Exception as e:
                messagebox.showerror('Error', f'Error saving bill: {str(e)}')
    def clear(self):
        # Clear customer details
        self.bill_no.set(str(random.randint(1000, 9999)))
        self.customer_name.set('')
        self.customer_phone.set('')
        self.date.set(datetime.now().strftime("%d/%m/%Y"))
        
        # Clear product details
        self.product_category.set('')
        self.product_name.set('')
        self.product_price.set('')
        self.product_qty.set('')
        self.tax.set('')
        
        # Clear bill list and area
        self.total_list = []
        self.bill_area.delete(1.0, tk.END)
        
        messagebox.showinfo('Success', 'All fields cleared!')