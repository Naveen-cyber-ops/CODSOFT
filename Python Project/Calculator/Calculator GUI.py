import tkinter as tk
from tkinter import messagebox

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple Calculator")
        master.geometry("300x250") # Set a fixed size for the window
        master.resizable(False, False) # Make window non-resizable

        # --- Input Fields ---
        self.label_num1 = tk.Label(master, text="First Number:")
        self.label_num1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_num1 = tk.Entry(master, width=20)
        self.entry_num1.grid(row=0, column=1, padx=10, pady=5)
        self.entry_num1.focus_set() # Set focus to the first entry field

        self.label_num2 = tk.Label(master, text="Second Number:")
        self.label_num2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_num2 = tk.Entry(master, width=20)
        self.entry_num2.grid(row=1, column=1, padx=10, pady=5)

        # --- Operation Buttons ---
        self.button_add = tk.Button(master, text="+", width=5, command=lambda: self.calculate("add"))
        self.button_add.grid(row=2, column=0, padx=5, pady=10)

        self.button_subtract = tk.Button(master, text="-", width=5, command=lambda: self.calculate("subtract"))
        self.button_subtract.grid(row=2, column=1, padx=5, pady=10)

        self.button_multiply = tk.Button(master, text="*", width=5, command=lambda: self.calculate("multiply"))
        self.button_multiply.grid(row=3, column=0, padx=5, pady=5)

        self.button_divide = tk.Button(master, text="/", width=5, command=lambda: self.calculate("divide"))
        self.button_divide.grid(row=3, column=1, padx=5, pady=5)

        # --- Result Display ---
        self.label_result_text = tk.Label(master, text="Result:")
        self.label_result_text.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.label_result = tk.Label(master, text="", width=20, anchor="w", relief="sunken", borderwidth=2)
        self.label_result.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

    def get_numbers(self):
        """
        Retrieves numbers from the entry fields and validates them.
        Returns (num1, num2) if valid, None otherwise.
        """
        try:
            num1 = float(self.entry_num1.get())
            num2 = float(self.entry_num2.get())
            return num1, num2
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in both fields.")
            return None, None

    def calculate(self, operation):
        """
        Performs the calculation based on the selected operation.
        Updates the result label or shows an error message.
        """
        num1, num2 = self.get_numbers()
        if num1 is None or num2 is None:
            self.label_result.config(text="") # Clear previous result on error
            return

        result = None
        op_symbol = ""

        if operation == "add":
            result = num1 + num2
            op_symbol = "+"
        elif operation == "subtract":
            result = num1 - num2
            op_symbol = "-"
        elif operation == "multiply":
            result = num1 * num2
            op_symbol = "*"
        elif operation == "divide":
            if num2 == 0:
                messagebox.showerror("Calculation Error", "Cannot divide by zero!")
                self.label_result.config(text="")
                return
            result = num1 / num2
            op_symbol = "/"

        # Display the result
        if result is not None:
            self.label_result.config(text=f"{result:.2f}") # Format to 2 decimal places

# Main part of the script
if __name__ == "__main__":
    root = tk.Tk()
    my_calculator = CalculatorGUI(root)
    root.mainloop()
