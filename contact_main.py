from tkinter import *
from tkinter import messagebox
import re
import os

from database import Database


class contactsApp :
    def __init__(self):
        self.root = Tk()
        self.db = Database()
        self.root.title("Contact Book")
        self.root.configure(background="#4e696f")
        self.root.geometry("800x600")
        self.root.iconbitmap("resources/favicon (2).ico")
        self.db.load_contact()
        self.widgets()
        self.update_listbox()


        self.root.mainloop()

    def widgets(self):
        #adding up the frames...

        header_frame = Frame(self.root,bg="#4e696f")
        header_frame.pack(side = "top" ,fill = "x")

        content_frame = Frame(self.root,bg="#f0f0f0")
        content_frame.pack(fill = "both",expand = True,padx = 10,pady = 10)

        left_frame = Frame(content_frame,bg="#d9d9d9")
        left_frame.pack(side = "left",fill = "y",padx =(0,10))

        display_frame = Frame(content_frame,bg="#d9d9d9")
        display_frame.pack(side = "right",fill = "both",expand = True)

        status_frame = Frame(content_frame,bg="#4e696f")
        status_frame.pack(side = "bottom",fill = "x")

        #adding heading..

        heading = Label(header_frame, text = "Contact Book ",font = ("calibri",18),bg="#4e696f")
        heading.pack(side = "top",fill = "x")

        #settingup the input frame

        input_frame = Frame(left_frame,bg="#d9d9d9")
        input_frame.pack(side = "bottom",fill = "x")

        #adding labels and the entry box the frame..

        label0 = Label(input_frame, text="Name:", font = ("calibri",15),bg="#4e696f")
        label0.grid(row=0, column=0, sticky="w", pady=2)

        self.name_enter = Entry(input_frame, width=30)
        self.name_enter.grid(row=0, column=1, sticky="w", pady=2)
        self.name_enter.focus()

        label1 = Label(input_frame,text = "Phone :",font = ("calibri",15),bg="#4e696f")
        label1.grid(row=1, column=0, sticky="w", pady=2)

        self.phone_enter = Entry(input_frame,width = 30)
        self.phone_enter.grid(row = 1,column = 1,sticky = "w",pady = 2)

        label2 = Label(input_frame, text="Email :", font = ("calibri",15),bg="#4e696f")
        label2.grid(row=2, column=0, sticky="w", pady=2)

        self.email_enter = Entry(input_frame, width=30)
        self.email_enter.grid(row=2, column=1, sticky="w", pady=2)

        label3 = Label(input_frame, text="Address:",font = ("calibri",15),bg="#4e696f")
        label3.grid(row=3, column=0, sticky="w", pady=2)

        self.address_enter = Text(input_frame, width=22, height=3) #for multiline input...
        self.address_enter.grid(row=3, column=1, sticky="w", pady=2)

        # setting the button frame

        btn_frame = Frame(left_frame,bg="#d9d9d9")
        btn_frame.pack(padx = 10, pady = 10 ,fill = "x")
        #adding buttons to that frame
        add_contact_btn = Button(btn_frame, text="Add Contact",command = self.add_contacts)
        add_contact_btn.pack(side="left", expand=True, padx=2)

        update_contact_btn = Button(btn_frame, text="Update Contact",command = self.update_contacts)
        update_contact_btn.pack(side="left", expand=True, padx=2)

        delete_contact_btn = Button(btn_frame, text="Delete Contact",command = self.delete_contact)
        delete_contact_btn.pack(side="left", expand=True, padx=2)

        clear_btn = Button(btn_frame, text="Clear",command = self.clear_fields)
        clear_btn.pack(side="left", expand=True, padx=2)

        #Adding the label

        label4 = Label(display_frame, text = "Saved Contacts",font = ("calibri",14),bg="#4e696f")
        label4.pack(pady=(0, 3))

        #search frame...

        search_frame = Frame(display_frame,bg="#d9d9d9")
        search_frame.pack(fill = "x",padx = 5,pady = (0,5))

        label5 = Label(search_frame,text = "Search",bg="#4e696f")
        label5.pack(side ="left",pady=(0,5))

        self.search_enter = Entry(search_frame,width = 30)
        self.search_enter.pack(side="left",fill = "x",expand = True)

        self.search_enter.bind("<KeyRelease>",self.search_contact)
        self.search_enter.focus()

        #adding scrollbar

        List_scroll_frame= Frame(display_frame,bg="#d9d9d9")
        List_scroll_frame.pack(fill = "both",expand = True,padx = 5,pady = 5)

        self.scrollbar = Scrollbar(List_scroll_frame)
        self.scrollbar.pack(side = "right",fill = "y")

        self.contact_listbox = Listbox(List_scroll_frame, yscrollcommand = self.scrollbar.set)
        self.contact_listbox.pack(side = "left",fill = "both",expand = True)

        self.scrollbar.config(command = self.contact_listbox.yview)
        self.contact_listbox.bind("<<ListboxSelect>>",self.contact_select)

        self.status_label = Label(status_frame,text = "Welcome",font = ("calibri",9),bg="#4e696f",fg="white")
        self.status_label.pack(pady = 3)

    def update_listbox(self):
        self.contact_listbox.delete(0,END)

        sorted_contacts = sorted(self.db.contacts.items(), key = lambda item: item[1]["name"])
        for contact_id ,details in sorted_contacts:
            self.contact_listbox.insert(END,f"{details["name"]}-{details['phone']}")
            self.db.listbox_map.append(contact_id)

    def contact_select(self,event) :
        selection_indices = self.contact_listbox.curselection()
        if not selection_indices:
            return

        selected_index = selection_indices[0]
        try :
           contact_id = self.db.listbox_map[selected_index]
        except IndexError:
            return

        if contact_id in self.db.contacts:
            self.db.selected_contact = contact_id
            contact = self.db.contacts[contact_id]


            # self.name_enter.delete(0, END)
            # self.phone_enter.delete(0, END)
            # self.email_enter.delete(0, END)
            # self.address_enter.delete("1.0",END)
            self.clear_fields()

            self.name_enter.insert(0,contact.get("name",""))
            self.phone_enter.insert(0,contact.get("phone",""))
            self.email_enter.insert(0,contact.get("email",""))
            self.address_enter.insert("1.0",contact.get("address",""))

            self.status_label.configure(text = f"selected : {contact.get('name',"")}")

    def validate_input(self,name,phone,email) :
        if name == "" :
            messagebox.showerror("Name Error", "Please enter a name")
            return False
        if not re.match(r"^\+?[\d\s-]{7,15}$", phone) :
            messagebox.showerror("Phone Error", "Please enter a valid phone number")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email) :
            messagebox.showerror("Email Error", "Please enter a valid email")
            return False
        return True

    def add_contacts(self):
        name = self.name_enter.get().strip()
        phone = self.phone_enter.get().strip()
        email = self.email_enter.get().strip()
        # here we need to pass the start pos("1.0",END)(line1,char0,end) beacuse its a multiline
        #input and we weed to tell .get() the range of text you want by start and end position...
        address = self.address_enter.get("1.0",END).strip()

        if not self.validate_input(name,phone,email) :
            return

        contact_id = str(self.db.contact_id)
        self.db.contacts[contact_id] = {
            "name" : name,
            "phone" : phone,
            "email" : email,
            "address" : address,

        }
        self.db.contact_id += 1
        self.db.save_contact()
        self.update_listbox()
        self.clear_fields()
        self.status_label.config(text=f"Added: {name}")

    def update_contacts(self) :
        if self.db.selected_contact is None :
            messagebox.showerror("Select Contact", "Please Select a Contact")
            return

        name = self.name_enter.get().strip()
        phone = self.phone_enter.get().strip()
        email = self.email_enter.get().strip()
        address = self.address_enter.get("1.0",END).strip()

        if not self.validate_input(name,phone,email) :
            return

        self.db.contacts[self.db.selected_contact] = {
            "name" : name,
            "phone" : phone,
            "email" : email,
            "address" : address,

        }

        self.db.save_contact()
        self.update_listbox()
        self.clear_fields()
        self.status_label.config(text=f"Updated: {name}")

    def delete_contact(self) :

        #print(f"Delete button clicked. The current selected_contact_id is: {self.db.selected_contact}")

        if self.db.selected_contact is None :
            messagebox.showerror("Delete Info", "Please Select a Contact")
            return

        name = self.db.contacts[self.db.selected_contact]["name"]
        if messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?"):
            del self.db.contacts[self.db.selected_contact]

            self.db.save_contact()
            self.update_listbox()
            self.clear_fields()
            self.status_label.config(text=f"Deleted: {name}")

    def clear_fields(self) :
        self.name_enter.delete(0,END)
        self.phone_enter.delete(0,END)
        self.email_enter.delete(0,END)
        self.address_enter.delete("1.0",END)
        # self.db.selected_contact = None
        # self.contact_listbox.delete(0,END)
        self.status_label.configure(text = "Welcome")

    def search_contact(self,event = None) :
        query = self.search_enter.get().lower().strip()

        self.contact_listbox.delete(0,END)
        self.db.listbox_map.clear()

        sorted_contact = sorted(self.db.contacts.items(),key = lambda x : x[1]["name"])
        for contact_id,details in sorted_contact :
            name = details.get("name","").lower()
            phone = details.get("phone","").lower()
            if not query or query in name or query in phone:
                display = f"{name} - {phone}"
                self.contact_listbox.insert(END,display)
                self.db.listbox_map.append(contact_id)




















































































































contact = contactsApp()



