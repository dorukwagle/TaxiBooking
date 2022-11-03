import tkinter as tk
from tkinter import ttk
import views.custom_widget as cw
from PIL import ImageTk, Image
from pathlib import Path
from .base_window import BaseWindow


class LoginPage(ttk.Frame):
    def __init__(self, controller, parent):
        self.__controller = controller
        self.font = ("", 20)
        # create a style for the frame
        style = ttk.Style()
        style.configure("new.TFrame", background="#ffffff")
        super().__init__(parent.frame)

        # create canvas to hold background image and frames
        canvas = tk.Canvas(self, width=parent.get_width_pct(100), height=parent.get_height_pct(100))
        canvas.pack()
        # create image
        img = ImageTk.PhotoImage(Image.open(Path("res/taxi1.jpg")).resize(
            (int(parent.get_width_pct(100)), int(parent.get_height_pct(100))), Image.ANTIALIAS))
        # add image to canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=img)

        # frame to hold all the elements
        base_frame = ttk.Frame(self, style="new.TFrame")
        canvas.create_window(parent.get_width_pct(70), parent.get_height_pct(30), anchor=tk.NW, window=base_frame)

        # create intro label # Everything in life is somewhere else, and!! \n You get there in a cab!!!
        canvas.create_text(parent.get_width_pct(10), parent.get_height_pct(45),
                           text="now this is significantly insignificant", fill="white", font=("", 30, "bold"), anchor=tk.NW)
        canvas.create_text(parent.get_width_pct(20), parent.get_height_pct(51),
                           text="better luck nextTime", fill="white", font=("", 30, "bold"), anchor=tk.NW)

        style = ttk.Style()
        style.configure("TFrame", background="#d4d4d4")
        # create right frame to hold form box
        input_frame = ttk.Frame(base_frame, style="TFrame", padding=25)
        input_frame.pack()

        # create form elements
        self.username = cw.InputBox(input_frame, placeholder="Username", placeholder_color="#c3c3c3", font=self.font)
        self.username.pack()
        # add space
        ttk.Label(input_frame, text="", font=("", 5)).pack()
        self.password = cw.InputBox(input_frame, placeholder="Password", input_type="password",
                                    placeholder_color="#c3c3c3", font=self.font)
        self.password.pack()
        ttk.Label(input_frame, text="", font=("", 2)).pack()
        # display error message
        self.error_msg = ttk.Label(input_frame, text="error msg", font=("", 12), foreground="red")
        self.error_msg.pack()

        ttk.Label(input_frame, text="", font=("", 2)).pack()
        cw.Button(input_frame, text="Sign In", takefocus=0, width=15, font=("", 20),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927").pack()
        ttk.Label(input_frame, text="", font=("", 2)).pack()
        ttk.Label(input_frame, text="Don't have account ?", font=("", 15), foreground="#3d3935").pack()
        ttk.Label(input_frame, text="SignUp below", font=("", 15), foreground="#3d3935").pack()
        ttk.Label(input_frame, text="", font=("", 2)).pack()
        cw.Button(input_frame, text="Sign Up", takefocus=0, width=15, font=("", 20),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927").pack()

        self.pack()
        # start the event listener
        parent.mainloop()
