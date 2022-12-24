import tkinter as tk
from tkinter import ttk
import views.custom_widget as cw
from PIL import ImageTk, Image
from pathlib import Path
from tkinter.messagebox import showinfo

def combo_select(combobox):
    combobox["foreground"] = "black"


class RegistrationPage(ttk.Frame):
    def __init__(self, parent, controller):
        self.__parent = parent
        # create a style for the frame
        style = ttk.Style()
        style.configure("new.TFrame", background="#ffffff")
        super().__init__(self.__parent.frame)

        # create canvas to hold background image and frames
        self.__canvas = tk.Canvas(self, width=self.__parent.get_width_pct(100),
                                  height=self.__parent.get_height_pct(100))
        self.__canvas.pack()
        # create images
        self.__bg_img = ImageTk.PhotoImage(Image.open(Path("res/taxi2.jpg")).resize(
            (int(self.__parent.get_width_pct(100)), int(self.__parent.get_height_pct(100))), Image.ANTIALIAS))

        # add background image to canvas
        self.__canvas.create_image(0, 0, anchor=tk.NW, image=self.__bg_img)

        # frame to hold all the elements
        self.base_frame = ttk.Frame(self, style="new.TFrame")
        self.__canvas.create_window(self.__parent.get_width_pct(70), self.__parent.get_height_pct(10), anchor=tk.NW,
                                    window=self.base_frame)

        # create back button
        back = cw.Button(self, text="< Back", takefocus=0, font=("", 15),
                         fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927",
                         command=controller.open_login)
        self.__canvas.create_window(2, 2, window=back, anchor=tk.NW)

        # create intro label
        self.__text1 = self.__canvas.create_text(self.__parent.get_width_pct(3), self.__parent.get_height_pct(45),
                                                 text="Fast and reliable rides at your fingertips!!", fill="white",
                                                 font=("", 30, "bold"), anchor=tk.NW)
        self.__text2 = self.__canvas.create_text(self.__parent.get_width_pct(6), self.__parent.get_height_pct(51),
                                                 text="Get where you need to go with ease!!!", fill="white",
                                                 font=("", 30, "bold"), anchor=tk.NW)
        # add registration page to the base frame
        self.pack()


class CustomerRegistration(ttk.Frame):
    def __init__(self, parent, controller):
        self.font = ("", 20)
        style = ttk.Style()
        style.configure("TFrame", background="#d4d4d4")
        # create right frame to hold form box
        super().__init__(parent, style="TFrame", padding=25)

        # create form elements
        self.full_name = cw.InputBox(self, placeholder="Full Name", placeholder_color="#c3c3c3", font=self.font)
        # self.username.bind("<Tab>", self.tab_handler)
        self.full_name.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()
        self.gender = ttk.Combobox(self, values=["Male", "Female"], background="white", font=("", 15), state="readonly")
        self.gender.set("<<Select Gender>>")
        self.gender.pack(expand=1, fill="both")
        self.gender.bind("<<ComboboxSelected>>", lambda event: combo_select(self.gender))
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.email_address = cw.InputBox(self, placeholder="Email Address", placeholder_color="#c3c3c3", font=self.font)
        self.email_address.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.address = cw.InputBox(self, placeholder="Address", placeholder_color="#c3c3c3", font=self.font)
        self.address.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.telephone = cw.InputBox(self, placeholder="Telephone", placeholder_color="#c3c3c3", font=self.font)
        self.telephone.pack()
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
        self.error_msg = ttk.Label(self, text="", font=("", 12), foreground="red")
        self.error_msg.pack()

        ttk.Label(self, text="", font=("", 2)).pack()

        cw.Button(self, text="Sign Up", takefocus=0, width=15, font=("", 20),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927",
                  command=controller.sign_up).pack()


class DriverRegistration(ttk.Frame):
    def __init__(self, parent, controller):
        self.__parent = parent
        self.font = ("", 20)
        style = ttk.Style()
        style.configure("driver.TFrame", background="#d4d4d4")
        # create right frame to hold form box
        super().__init__(self.__parent, style="driver.TFrame", padding=25)

        # create form elements
        self.full_name = cw.InputBox(self, placeholder="Full Name", placeholder_color="#c3c3c3", font=self.font)
        self.full_name.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.gender = ttk.Combobox(self, values=["Male", "Female"], background="white", font=("", 15), state="readonly")
        self.gender.set("<<Select Gender>>")
        self.gender.bind("<<ComboboxSelected>>", lambda event: combo_select(self.gender))
        self.gender.pack(expand=1, fill="both")
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.address = cw.InputBox(self, placeholder="Address", placeholder_color="#c3c3c3", font=self.font)
        self.address.pack()
        # add space
        ttk.Label(self, text="", font=("", 2)).pack()

        self.license_id = cw.InputBox(self, placeholder="License ID", placeholder_color="#c3c3c3", font=self.font)
        self.license_id.pack()
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
        self.error_msg = ttk.Label(self, text="", font=("", 12), foreground="red")
        self.error_msg.pack()

        ttk.Label(self, text="", font=("", 2)).pack()

        cw.Button(self, text="Sign Up", takefocus=0, width=15, font=("", 20),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927",
                  command=controller.register_driver).pack()

    @staticmethod
    def successful():
        showinfo("Successful", "Driver Registered Completed")
