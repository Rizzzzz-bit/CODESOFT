from tkinter import *
from tkinter import messagebox
from PIL import Image
from customtkinter import *
from tkcalendar import Calendar


class ToDoListApp:
    def __init__ (self):
        self.root = CTk()
        self.root.title("To-do List")
        self.root.geometry("800x600")
        self.root.iconbitmap("resources/favicon (4).ico")
        self.root.configure(background="#282828")
        self.Home()
        self.task = []
        self. update_task_list()


        self.root.mainloop()

    def Home(self):

        header_frame = CTkFrame(self.root,fg_color ="transparent")
        header_frame.pack(side = "top", fill = "x", padx=10, pady=5)

        heading = CTkLabel(header_frame, text = "To do List ",font = ("calibri",30,"bold"),text_color="#8892d5")
        heading.pack(pady = (15,15))

        home_img = CTkImage(Image.open("resources/home.png").resize((25,25)))

        image_label = CTkLabel(header_frame,
                            image=home_img,
                            text = "")
        image_label.pack(pady = (10,15))

        input_frame = CTkFrame(self.root,fg_color ="transparent")
        input_frame.pack(fill = "x", padx=20, pady=20)
        self.task_entry = CTkEntry(
            input_frame,
            placeholder_text="Add a new Task...",
            height = 40,
            font = ("calibri",14),
            corner_radius=10,
            fg_color="#3c3c3c",
            border_color="#8892d5",)
        self.task_entry.pack(side = "left", fill  = "x",expand = True)
        self.task_entry.bind("<Return>",lambda event: self.AddTask())

        calandar_button = CTkButton(
            input_frame,
            text = "📅",
            width = 40,
            height = 40,
            font = ("calibri",14),
            command= self.open_calender,
            fg_color = "#3c3c3c",
            hover_color = "#4c4c4c",
            text_color_disabled= "grey"
        )
        calandar_button.pack(side= "right",padx = (10,10))

        button_frame = CTkFrame(self.root, fg_color="transparent")
        button_frame.pack(pady=10)

        add_button = CTkButton(button_frame,text ="+ Add Task",font=( "calibri",14,"bold"),fg_color = "#8892d5",command=self.AddTask)
        add_button.pack(side = "left" , padx = 5)

        self.task_frame = CTkScrollableFrame(self.root,fg_color="#3c3c3c",label_text="Task List")
        self.task_frame.pack(fill ="both",expand = True,padx =20,pady =10)

    def open_calender(self):
        calendar_window = CTkToplevel(self.root)
        calendar_window.resizable(False,False)
        calendar_window.title("Select a date")
        calendar_window.configure(bg = "#282828")
        calendar_window.grab_set()

        app_x = self.root.winfo_x()
        app_y = self.root.winfo_y()
        calendar_window.geometry(f"300x200+{app_x+ 250}+{app_y + 150}")

        calender = Calendar(calendar_window,selectmode="day",date_pattern = "dd/MM/yyyy",)
        calender.pack(pady = 10,padx = 10,fill = "both",expand = True)

        def grab_date():
            selected_date = calender.get_date()
            self.task_entry.delete(0,"end")
            self.task_entry.insert(0,f" Task for {selected_date}")
            calendar_window.destroy()

        select_button = CTkButton(calendar_window,text="Select Date", command = grab_date)
        select_button.pack(pady = 10)

        self.update_task_list()

    def AddTask(self):
        task_text = self.task_entry.get().strip()

        if task_text :
            self.task.append(task_text)
            self.task_entry.delete(0,"end")
            self.update_task_list()
        else :
            messagebox.showerror("Warning","Task not found")

    def DeleteTask(self,task_to_delete):
        self.task.remove(task_to_delete)
        self.update_task_list()

    def update_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in self.task:
            task_container = CTkFrame(self.task_frame)
            task_container.pack(fill = "x",pady = 5)

            task_label = CTkLabel(task_container,text=task,font=("Calibri", 14))
            task_label.pack(side = "left", fill = "x",expand = True,padx = 10)

            delete_button = CTkButton(
                task_container,
                text = "Delete",
                width = 40,
                fg_color="#c14444",
                hover_color="#a33a3a",
                command=lambda t=task: self.DeleteTask(t)
            )

            delete_button.pack(side ="right",padx = 10)



















































app = ToDoListApp()
