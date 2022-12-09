from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image


class AdminDashboard(ttk.Frame):
    def __init__(self, controller, parent):
        self.__window = parent
        self.__controller = controller
        super().__init__(parent)

        self.pack()