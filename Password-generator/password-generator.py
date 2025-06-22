import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip  # You may need to install: pip install pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Generator")
        self.root.geometry("450x400")
        self.root.config(bg="#222831")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Password Generator", font=("Arial", 20, "bold"), bg="#222831", fg="#FFD369")
        title.pack(pady=20)

        # Password length
        tk.Label(self.root, text="Password Length:", font=("Arial", 12), bg="#222831", fg="white").pack(pady=(10, 0))
        self.length_var = tk.IntVar(value=12)
        tk.Scale(self.root, from_=6, to=32, variable=self.length_var, orient=tk.HORIZONTAL, length=300, bg="#393E46", fg="white", troughcolor="#FFD369").pack()

        # Checkbuttons
        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        options_frame = tk.Frame(self.root, bg="#222831")
        options_frame.pack(pady=10)

        tk.Checkbutton(options_frame, text="Include Uppercase", variable=self.include_upper, bg="#222831", fg="green", selectcolor="#FFD369").grid(row=0, column=0, padx=10, sticky="w")
        tk.Checkbutton(options_frame, text="Include Lowercase", variable=self.include_lower, bg="#222831", fg="green", selectcolor="#FFD369").grid(row=1, column=0, padx=10, sticky="w")
        tk.Checkbutton(options_frame, text="Include Digits", variable=self.include_digits, bg="#222831", fg="green", selectcolor="#FFD369").grid(row=0, column=1, padx=10, sticky="w")
        tk.Checkbutton(options_frame, text="Include Symbols", variable=self.include_symbols, bg="#222831", fg="green", selectcolor="#FFD369").grid(row=1, column=1, padx=10, sticky="w")

        # Generate button
        tk.Button(self.root, text="Generate Password", command=self.generate_password, font=("Arial", 12, "bold"), bg="#00ADB5", fg="white", padx=10, pady=5).pack(pady=10)

        # Output
        self.password_output = tk.Entry(self.root, font=("Arial", 14), justify="center", bd=0, bg="#EEEEEE")
        self.password_output.pack(pady=10, ipady=5, ipadx=5)

        # Copy button
        tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard, bg="#FFD369", fg="black", font=("Arial", 10, "bold")).pack(pady=5)

    def generate_password(self):
        length = self.length_var.get()
        characters = ""

        if self.include_upper.get():
            characters += string.ascii_uppercase
        if self.include_lower.get():
            characters += string.ascii_lowercase
        if self.include_digits.get():
            characters += string.digits
        if self.include_symbols.get():
            characters += string.punctuation

        if not characters:
            messagebox.showwarning("Warning", "Please select at least one character type.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_output.delete(0, tk.END)
        self.password_output.insert(0, password)

    def copy_to_clipboard(self):
        password = self.password_output.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
