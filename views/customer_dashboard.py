import tkinter as tk
from tkinter import ttk


class CustomerDashboard(ttk.Frame):
    def __init__(self, controller, parent):

        super().__init__(parent.frame)
