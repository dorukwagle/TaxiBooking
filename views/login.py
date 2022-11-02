from tkinter import ttk
from .input_box import InputBox
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

        img = ImageTk.PhotoImage(Image.open(Path("res/taxi1.jpg")).resize(
            (int(parent.get_width_pct(100)), int(parent.get_height_pct(100))), Image.ANTIALIAS
        ))
        image = ttk.Label(self, image=img)
        image.place(x=0, y=0)
        # image.pack()

        # create left frame to hold text
        label = ttk.Button(self, text="Now this is significantly insignificant...")
        label.pack(side="left")

        inp = InputBox(self, placeholder="password", input_type="pass", show="%", font_color="red",
                       placeholder_color="", font=("", 30))
        inp.pack(side="top")
        self.pack()

        # start the event listener
        parent.mainloop()

