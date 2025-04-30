import tkinter as tk
from tkinter import messagebox, filedialog

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Calculator with History")

        # Input fields
        self.num1_entry = tk.Entry(root, width=10)
        self.num2_entry = tk.Entry(root, width=10)
        self.num1_entry.grid(row=0, column=1, padx=5, pady=5)
        self.num2_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Number 1:").grid(row=0, column=0)
        tk.Label(root, text="Number 2:").grid(row=1, column=0)

        # Buttons for operations
        tk.Button(root, text="Add", command=self.add).grid(row=2, column=0)
        tk.Button(root, text="Subtract", command=self.subtract).grid(row=2, column=1)
        tk.Button(root, text="Multiply", command=self.multiply).grid(row=3, column=0)
        tk.Button(root, text="Divide", command=self.divide).grid(row=3, column=1)

        # History Text Area
        self.history_area = tk.Text(root, height=10, width=40, state="normal")
        self.history_area.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Buttons for file operations
        tk.Button(root, text="Save History", command=self.save_history).grid(row=5, column=0)
        tk.Button(root, text="Load History", command=self.load_history).grid(row=5, column=1)

    def get_numbers(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            return num1, num2
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numbers.")
            return None, None

    def add(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            result = num1 + num2
            self.log_history(f"{num1} + {num2} = {result}")

    def subtract(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            result = num1 - num2
            self.log_history(f"{num1} - {num2} = {result}")

    def multiply(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            result = num1 * num2
            self.log_history(f"{num1} * {num2} = {result}")

    def divide(self):
        num1, num2 = self.get_numbers()
        if num1 is not None:
            if num2 == 0:
                messagebox.showerror("Math error", "Cannot divide by zero.")
                return
            result = num1 / num2
            self.log_history(f"{num1} / {num2} = {result}")

    def log_history(self, text):
        self.history_area.insert(tk.END, text + "\n")
        self.history_area.see(tk.END)

    def save_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.history_area.get("1.0", tk.END))

    def load_history(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.history_area.delete("1.0", tk.END)
                self.history_area.insert(tk.END, content)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
