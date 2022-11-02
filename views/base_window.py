import tkinter as tk
from tkinter import ttk


class BaseWindow(tk.Tk):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BaseWindow, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # create app object and create some variables
        super().__init__()
        # create theme
        style = ttk.Style(self)
        style.theme_use("alt")
        # application window total size in percent
        self.__app_size_percent = 85

        # total height and width of the screen (screen resolution)
        self.__scr_height = self.winfo_screenheight()
        self.__scr_width = self.winfo_screenwidth()
        # height and width of the application window
        self.__app_width = int(self.__scr_width * self.__app_size_percent / 100)
        self.__app_height = int(self.__scr_height * self.__app_size_percent / 100)

        self.title("Taxi Booking")
        self.geometry("%dx%d" % (self.__app_width, self.__app_height))
        self.resizable(False, False)

        # configure rows and columns to allow frames to cover whole parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create a style for the frame
        style = ttk.Style()
        style.configure("new.TFrame", background="#ffffff")
        # create a frame in the root window equal to the size of window
        self.__frame = ttk.Frame(self, width=self.__app_width, height=self.__app_height, style="new.TFrame")

        self.__frame.grid(row=0, column=0, sticky="nsew")

    def __destroy_view(self):
        for child in self.__frame.winfo_children():
            child.destroy()

    @property
    def frame(self):
        # return empty frame
        self.__destroy_view()
        return self.__frame

    # return the x percent width of the app
    def get_width_pct(self, x):
        return self.__app_width * x / 100

    # return the x percent height of the app
    def get_height_pct(self, x):
        return self.__app_height * x / 100

