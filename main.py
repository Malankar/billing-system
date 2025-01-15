import tkinter as tk
from src.billing_system import BillingSystem

def main():
    root = tk.Tk()
    app = BillingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()