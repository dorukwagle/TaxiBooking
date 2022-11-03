import tkinter as tk
from tkinter import ttk
import views.custom_widget as cw
from PIL import ImageTk, Image
from pathlib import Path
import time
from .base_window import BaseWindow


def combo_select(combobox):
    combobox["foreground"] = "black"


class RegistrationPage(ttk.Frame):
    def __init__(self, controller, parent):
        self.__controller = controller
        self.__parent = parent
        # create a style for the frame
        style = ttk.Style()
        style.configure("new.TFrame", background="#ffffff")
        super().__init__(parent.frame)

        # create canvas to hold background image and frames
        self.__canvas = tk.Canvas(self, width=parent.get_width_pct(100), height=parent.get_height_pct(100))
        self.__canvas.pack()
        # create images
        bg_img = ImageTk.PhotoImage(Image.open(Path("res/taxi2.jpg")).resize(
            (int(self.__parent.get_width_pct(100)), int(self.__parent.get_height_pct(100))), Image.ANTIALIAS))

        # add background image to canvas
        self.__bg_img = self.__canvas.create_image(0, 0, anchor=tk.NW, image=bg_img)

        # frame to hold all the elements
        base_frame = ttk.Frame(self, style="new.TFrame")
        self.__canvas.create_window(parent.get_width_pct(70), parent.get_height_pct(10), anchor=tk.NW,
                                    window=base_frame)

        # create intro label
        self.__text1 = self.__canvas.create_text(parent.get_width_pct(10), parent.get_height_pct(45),
                                                 text="", fill="white",
                                                 font=("", 30, "bold"),
                                                 anchor=tk.NW)
        self.__text2 = self.__canvas.create_text(parent.get_width_pct(20), parent.get_height_pct(51),
                                                 text="", fill="white", font=("", 30, "bold"),
                                                 anchor=tk.NW)

        style = ttk.Style()
        # style.map("TNotebook.Tab", background=[("", "white")])
        style.configure('TNotebook.Tab', background="grey", foreground="black", padding=[25, 8], font=("", 13, "bold"))
        style.configure('TNotebook', padding=[10, 10], background="grey")
        # create a Notebook to hold both registration form
        self.tab_control = ttk.Notebook(base_frame, takefocus=0)
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # create tabs
        customer_tab = ttk.Frame(self.tab_control)
        driver_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(customer_tab, text="Customer SignUp")
        self.tab_control.add(driver_tab, text="Driver SignUp")
        self.tab_control.pack(expand=1, fill="both")

        # add respective pages to the tabs
        CustomerRegistration(customer_tab).pack()
        DriverRegistration(driver_tab).pack()

        self.pack()
        # start the event listener
        parent.mainloop()

    def create_image(self, path):
        img = ImageTk.PhotoImage(Image.open(Path(path)).resize(
            (int(self.__parent.get_width_pct(100)), int(self.__parent.get_height_pct(100))), Image.ANTIALIAS))
        return img

    def on_tab_change(self, *args):

        tab = self.tab_control.tab(self.tab_control.select(), "text")

        if tab == "Driver SignUp":
            # Get Yourself to Work!! \n We Value Your Work!!!
            self.__canvas.itemconfig(self.__text1, text="Register your skill to crash")
            self.__canvas.itemconfig(self.__text2, text="Get the car smashed")
        else:
            # Taxi at your fingertip! \n Book a trip now!!!
            self.__canvas.itemconfig(self.__text1, text="We guarantee you the deadliest crash")
            self.__canvas.itemconfig(self.__text2, text="Experience the death")


class CustomerRegistration(ttk.Frame):
    def __init__(self, container):
        self.font = ("", 20)
        style = ttk.Style()
        style.configure("TFrame", background="#d4d4d4")
        # create right frame to hold form box
        super().__init__(container, style="TFrame", padding=25)

        # create form elements
        self.username = cw.InputBox(self, placeholder="Full Name", placeholder_color="#c3c3c3", font=self.font)
        # self.username.bind("<Tab>", self.tab_handler)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()
        self.gender = ttk.Combobox(self, values=["Male", "Female"], background="white", font=("", 15), state="readonly")
        self.gender.set("<<Select Gender>>")
        self.gender.pack(expand=1, fill="both")
        self.gender.bind("<<ComboboxSelected>>", lambda event: combo_select(self.gender) )
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.username = cw.InputBox(self, placeholder="Email Address", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.username = cw.InputBox(self, placeholder="Address", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.username = cw.InputBox(self, placeholder="Telephone", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()
        self.payment_method = ttk.Combobox(self, values=["Credit Card", "Bank Transfer", "Cash"], background="white",
                                           font=("", 15), state="readonly")
        self.payment_method.set("<<Payment Method>>")
        self.payment_method.bind("<<ComboboxSelected>>", lambda event: combo_select(self.payment_method))
        self.payment_method.pack(expand=1, fill="both")
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()
        self.username = cw.InputBox(self, placeholder="Username", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()
        self.password = cw.InputBox(self, placeholder="Password", input_type="password",
                                    placeholder_color="#c3c3c3", font=self.font)
        self.password.pack()

        ttk.Label(self, text="", font=("", 2)).pack()
        self.confirm_password = cw.InputBox(self, placeholder="Confirm Password", input_type="password",
                                            placeholder_color="#c3c3c3", font=self.font)
        self.confirm_password.pack()

        ttk.Label(self, text="", font=("", 2)).pack()
        # display error message
        self.error_msg = ttk.Label(self, text="error msg", font=("", 12), foreground="red")
        self.error_msg.pack()

        ttk.Label(self, text="", font=("", 2)).pack()

        cw.Button(self, text="Sign Up", takefocus=0, width=15, font=("", 20),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927").pack()


class DriverRegistration(ttk.Frame):
    def __init__(self, container):
        self.font = ("", 20)
        style = ttk.Style()
        style.configure("TFrame", background="#d4d4d4")
        # create right frame to hold form box
        super().__init__(container, style="TFrame", padding=25)

        # create form elements
        self.username = cw.InputBox(self, placeholder="Full Name", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.gender = ttk.Combobox(self, values=["Male", "Female"], background="white", font=("", 15), state="readonly")
        self.gender.set("<<Select Gender>>")
        self.gender.bind("<<ComboboxSelected>>", lambda event: combo_select(self.gender))
        self.gender.pack(expand=1, fill="both")
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.username = cw.InputBox(self, placeholder="Email Address", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.username = cw.InputBox(self, placeholder="Address", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.username = cw.InputBox(self, placeholder="License ID", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.username = cw.InputBox(self, placeholder="Username", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()
        self.password = cw.InputBox(self, placeholder="Password", input_type="password",
                                    placeholder_color="#c3c3c3", font=self.font)
        self.password.pack()

        ttk.Label(self, text="", font=("", 2)).pack()
        self.confirm_password = cw.InputBox(self, placeholder="Confirm Password", input_type="password",
                                            placeholder_color="#c3c3c3", font=self.font)
        self.confirm_password.pack()

        ttk.Label(self, text="", font=("", 2)).pack()
        # display error message
        self.error_msg = ttk.Label(self, text="error msg", font=("", 12), foreground="red")
        self.error_msg.pack()

        ttk.Label(self, text="", font=("", 2)).pack()

        cw.Button(self, text="Sign Up", takefocus=0, width=15, font=("", 20),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927").pack()
