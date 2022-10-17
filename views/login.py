from tkinter import ttk


class LoginPage(ttk.Frame):
    def __init__(self, controller,  parent):
        self.__controller = controller
        super().__init__(parent)

