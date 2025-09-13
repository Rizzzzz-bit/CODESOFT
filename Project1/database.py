import json
import os
from tkinter import messagebox
import shutil
class Database :
    def __init__(self):
        self.contact_id = 0
        self.contacts = {}
        self.selected_contact = None
        self.listbox_map = []
        self.filename = "contacts.json"

    def load_contact(self) :
        try :
            with open(self.filename,'r') as f :
                self.contacts = json.load(f)
                if self.contacts :
                    max_id = max(int(k) for k in self.contacts.keys())
                    self.contact_id = max_id + 1
                else :
                    self.contact_id = 1
        except FileNotFoundError :
            self.contacts = {}
            self.contact_id = 1
        except json.JSONDecodeError :
            messagebox.showerror(" Load Error", "No contacts file found")

    def save_contact(self) :
        if os.path.exists(self.filename) :
            shutil.copy(self.filename,self.filename + ".backup")

        try :
            with open(self.filename,'w') as f :
                json.dump(self.contacts,f,indent = 4)
        except IOError as e  :
            messagebox.showerror("Save Error", "could not save contacts file")




