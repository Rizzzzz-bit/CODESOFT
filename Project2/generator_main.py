from tkinter import *
from tkinter import messagebox
import argparse
import secrets
import string
from random import SystemRandom
class PasswordGenerator:
    def __init__(self):
        self.root  = Tk()
        self.root.title("Password Generator")
        self.root.configure(background="#4e696f")
        self.root.geometry("800x500")
        self.root.iconbitmap("resources/favicon (3).ico")
        self.output_text = StringVar()
        #setting default password length to 8
        self.length = IntVar(value=8)
        #for the checkboxes's for setting value's
        self.uppercase = BooleanVar(value=True)
        self.lowercase = BooleanVar(value=True)
        self.numbers = BooleanVar(value=True)
        self.symbols = BooleanVar(value=False)
        self.system_random = SystemRandom()
        self.Frame()


        self.root.mainloop()

    def Frame(self):

        Heading = Label(self.root, text="Password Generator", font=("calibri", 18, "bold"))
        Heading.pack(pady=20)
        Heading.configure(background="#4e696f")

        display_frame = Frame(self.root,bg="#f0f0f0")
        display_frame.pack(fill='x', pady=5)

        length_frame = Frame(self.root,bg="#f0f0f0", relief='groove', borderwidth=3)
        length_frame.pack(pady= 5 ,padx=10,fill="x")

        label0 = Label(length_frame, text="Password Length", font=("calibri", 15), bg="#4e696f")
        label0.pack(side = "left")

        length_input = Spinbox(length_frame, from_=4, to=32,textvariable=self.length,width=5)
        length_input.pack(side = "left",padx = 5)

        options_frame = Frame(self.root, bg="#f0f0f0", relief='groove', borderwidth=3)
        options_frame.pack(pady=10, padx=5, fill='x')

        uppercase_check = Checkbutton(options_frame, text="Include Uppercase (A-Z)", variable=self.uppercase,bg="#f0f0f0")
        uppercase_check.pack(anchor="w", padx=10)

        lowercase_check = Checkbutton(options_frame, text="Include Lowercase (a-z)", variable=self.lowercase,bg="#f0f0f0")
        lowercase_check.pack(anchor="w", padx=10)

        numbers_check = Checkbutton(options_frame, text="Include Numbers (0-9)",variable=self.numbers,bg="#f0f0f0")
        numbers_check.pack(anchor="w", padx=10)

        symbols_check = Checkbutton(options_frame, text="Include Symbols (!@#$)", variable=self.symbols,bg="#f0f0f0")
        symbols_check.pack(anchor="w", padx=10)

        generate_button = Button(self.root, text="Generate Password", font=("Helvetica", 10, "bold"),command=self.generate)
        generate_button.pack(pady=10)

        self.output_text = StringVar()
        output_label = Label(self.root,text = "",textvariable = self.output_text , font=("Calibri", 18, "bold"),bg = "#4e696f")
        output_label.pack(pady=10)

        self.copy_button = Button(self.root,text = "Want to copy!", font=("calibri", 10),command=self.copy)
        self.copy_button.pack(pady=10)

    def generate(self):
        length = self.length.get()
        uppercase = self.uppercase.get()
        lowercase = self.lowercase.get()
        numbers = self.numbers.get()
        symbols = self.symbols.get()
        choices  = []
        empty = ""

        if not(uppercase or lowercase or numbers or symbols):
            messagebox.showerror("Input Error", "Please select a input")
            return

        if uppercase:
            choices.append(secrets.choice(string.ascii_uppercase))
            empty += string.ascii_uppercase
        if lowercase:
            choices.append(secrets.choice(string.ascii_lowercase))
            empty += string.ascii_lowercase
        if numbers:
            choices.append(secrets.choice(string.digits))
            empty += string.digits
        if symbols:
            choices.append(secrets.choice(string.punctuation))
            empty += string.punctuation

        if length < len(choices):
            messagebox.showerror("Input Error", " Length is too short to include one of each selected character type.")

        remaining = length - len(choices)
        for _ in range(remaining):
            choices.append(secrets.choice(empty))

        for i in range(len(choices)-1,0,-1):
            j = secrets.randbelow(i+1)
            choices[i] ,choices[j] = choices[j],choices[i]

        self.final_password = ''.join(choices)
        self.output_text.set(self.final_password)

    def copy(self):
        password = self.output_text.get()
        if password and "Click 'Generate Password'" not in password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.copy_button.config(text="Copied to clipboard",state = "disabled")
            self.root.after(2000, self.reset_copy)

    def reset_copy(self):
        self.copy_button.config(text="Copy",state = "normal")




























































































































gen = PasswordGenerator()