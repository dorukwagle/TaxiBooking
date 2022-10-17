import tkinter as tk
from tkinter import ttk


class BaseWindow(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BaseWindow, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # create app object and create some variables
        self.__root = tk.Tk()

        # application window total size in percent
        self.__app_size_percent = 75

        # total height and width of the screen (screen resolution)
        self.__scr_height = self.__root.winfo_height()
        self.__scr_width = self.__root.winfo_width()

        # height and width of the application window
        self.__app_width =  self.__scr_width * self.__app_size_percent / 100
        self.__app_height =  self.__scr_height * self.__app_size_percent / 100

        self.__root.title("Taxi Booking")
        self.__root.geometry(f"{self.__app_height}x{self.__app_width}")

        # create congiguration of style
        # create a frame in the root window equal to the size of window
        self.__frame = ttk.Frame(self.__root, width=self.__app_width, height=self.__app_height)
        self.__frame.pack()

    def __destroy_view(self):
        for child in self.__frame.winfo_children():
            child.destroy()

    @property
    def frame(self):
        # return empty frame
        self.__destroy_view()
        return self.__frame

    def mainloop(self):
        self.__root.mainloop()

    # return the x percent width of the app
    def get_width_pct(self, x):
        return self.__app_width * x / 100

    # return the x percent height of the app
    def get_height_pct(self, x):
        return self.__app_height * x / 100