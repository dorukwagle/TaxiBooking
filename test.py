
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter_input_box.input_box import InputBox

class BaseWindow(tk.Tk):
    def __init__(self):
        super(BaseWindow, self).__init__()
        self.geometry("800x700")
        self.title("test title")

        frame = ttk.Frame(self)
        frame.pack()
        ttk.Label(frame, text="test label").pack()
        self.__img = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
            (200, 200)))
        ttk.Label(frame, image=self.__img).pack()
        InputBox(frame, placeholder="testing", placeholder_color="red", font_color="green").pack()
        frame_parent = ttk.Frame(self)
        frame_parent.pack()

        ParentWindow(frame_parent, self)
        # self.mainloop()


class ParentWindow(ttk.Frame):
    def __init__(self, parent, app):
        super(ParentWindow, self).__init__(parent)
        self.pack()
        ttk.Label(self, text="parent label test").pack()

        self.__img = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
            (200, 200)))
        ttk.Label(self, image=self.__img).pack()
        ttk.Label(self, text="test label").pack()

        frame_child = ttk.Frame(self)
        frame_child.pack()

        ChildWindow(frame_child, app)
        # self.mainloop()
        # app.mainloop()


class ChildWindow(ttk.Frame):
    def __init__(self, parent, app):
        super(ChildWindow, self).__init__(parent)
        self.pack()
        ttk.Label(self, text="child label test").pack()

        self.__img = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
            (200, 200)))
        ttk.Label(self, image=self.__img).pack()
        ttk.Label(self, text="test label").pack()
        # self.mainloop()
        # app.mainloop()


if __name__ == '__main__':
    # BaseWindow().mainloop()
    BaseWindow().mainloop()
