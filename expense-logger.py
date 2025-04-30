import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

FILE_NAME = "expenses.txt"

class ExpenseLogger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Daily Expense Logger")
        self.geometry("400x600")

        # Input Fields
        tk.Label(self, text="Amount ($)").pack(pady=5)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack(pady=5)

        tk.Label(self, text="Category").pack(pady=5)
        self.category_entry = tk.Entry(self)
        self.category_entry.pack(pady=5)

        tk.Label(self, text="Date (MM-DD-YYYY)").pack(pady=5)
        self.date_entry = tk.Entry(self)
        self.date_entry.pack(pady=5)

        # Add Expense Button
        tk.Button(self, text="Add Expense", command=self.add_expense).pack(pady=10)

        # Filter by Date
        tk.Label(self, text="Filter by Date (MM-DD-YYYY)").pack(pady=5)
        self.filter_date_entry = tk.Entry(self)
        self.filter_date_entry.pack(pady=5)
        tk.Button(self, text="Apply Filter", command=self.filter_by_date).pack(pady=5)
        tk.Button(self, text="Clear Filter", command=self.clear_filter).pack(pady=5)

        # Total Display
        self.total_label = tk.Label(self, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=10)

        # Recent Expenses Display
        tk.Label(self, text="Most Recent Expenses:").pack()
        self.recent_expenses = tk.Text(self, height=10, width=45)
        self.recent_expenses.pack(pady=10)
        self.recent_expenses.config(state="disabled")

        self.update_display()

    def add_expense(self):
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        date_input = self.date_entry.get().strip()

        if not amount or not category or not date_input:
            messagebox.showwarning("Missing Info", "All fields must be filled.")
            return

        try:
            amount_float = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return

        try:
            # Convert MM-DD-YYYY to YYYY-MM-DD for consistent internal storage
            date_obj = datetime.strptime(date_input, "%m-%d-%Y")
            date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date must be in MM-DD-YYYY format.")
            return

        with open(FILE_NAME, "a") as file:
            file.write(f"{amount},{category},{date}\n")

        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

        self.update_display()

    def update_display(self, filter_date=None):
        total = 0.0
        entries = []

        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                for line in file:
                    try:
                        amount, category, date = line.strip().split(",")
                        if filter_date:
                            date_obj = datetime.strptime(date, "%Y-%m-%d")
                            if date_obj.strftime("%m-%d-%Y") != filter_date:
                                continue
                        total += float(amount)
                        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d-%Y")
                        entries.append(f"${amount} | {category} | {formatted_date}")
                    except ValueError:
                        continue

        self.total_label.config(text=f"Total: ${total:.2f}")

        self.recent_expenses.config(state="normal")
        self.recent_expenses.delete("1.0", tk.END)
        for entry in entries[-10:]:  # show last 10
            self.recent_expenses.insert(tk.END, entry + "\n")
        self.recent_expenses.config(state="disabled")

    def filter_by_date(self):
        filter_date = self.filter_date_entry.get().strip()
        if not filter_date:
            messagebox.showwarning("Input Needed", "Please enter a date to filter.")
            return
        try:
            datetime.strptime(filter_date, "%m-%d-%Y")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date must be in MM-DD-YYYY format.")
            return
        self.update_display(filter_date=filter_date)

    def clear_filter(self):
        self.filter_date_entry.delete(0, tk.END)
        self.update_display()

if __name__ == "__main__":
    app = ExpenseLogger()
    app.mainloop()