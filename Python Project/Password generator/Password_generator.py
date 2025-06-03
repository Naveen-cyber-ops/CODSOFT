import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        master.geometry("350x200")
        master.resizable(False, False)

        self.length_label = tk.Label(master, text="Password Length:")
        self.length_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.length_entry = tk.Entry(master, width=10)
        self.length_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.length_entry.insert(0, "12")  # Default length

        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.password_label = tk.Label(master, text="Generated Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.password_display = tk.Label(master, text="", width=30, relief="sunken", borderwidth=2, anchor="w")
        self.password_display.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length <= 0:
                messagebox.showerror("Error", "Password length must be a positive integer.")
                return

            characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_display.config(text=password)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for the password length.")

if __name__ == "__main__":
    root = tk.Tk()
    password_generator = PasswordGeneratorGUI(root)
    root.mainloop()