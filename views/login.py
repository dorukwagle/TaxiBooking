import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
from .base_window import BaseWindow


class LoginPage(ttk.Frame):
    def __init__(self, controller,  parent):
        self.__controller = controller
        # create a style for the frame
        style = ttk.Style()
        style.configure("new.TFrame", background="#ffffff")
        super().__init__(parent.frame, style="new.TFrame")

        # img = ImageTk.PhotoImage(Image.open(Path("res/taxibooking.jpg")).resize(
        #     (int(parent.get_width_pct(70)), int(parent.get_height_pct(100))), Image.ANTIALIAS
        # ))
        # image = ttk.Label(self, image=img)
        # image.pack(side="left")
        label = ttk.Label(self, text="Now this is significantly insignificant...")
        label.pack(side="left")

        self.pack()

        # start the event listener
        parent.mainloop()

