import tkinter
from tkinter import Tk, Label
from PIL import Image, ImageTk

# root = Tk()
#
# img = Image.open("res/taxi1.jpg")
# imag = ImageTk.PhotoImage(file="res/taxi1.jpg")
#
# label = Label(root, image=imag)
# label.pack()
#
# root.mainloop()


from tkinter import *
import tkinter as tk
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes, constants, SpinTimePickerOld, SpinTimePickerModern

# Create Object
root = Tk()

# Set geometry
root.geometry("700x600")
root.propagate(False)

# # Add Calendar
# cal = Calendar(root, selectmode='day')
#
# cal.pack()
#
#
# def grad_date():
#     date.config(text="Selected Date is: " + cal.get_date())
#
#
# # Add Button and Label
# Button(root, text="Get Date",
#        command=grad_date).pack(pady=20)
#
# date = Label(root, text="")
# date.pack()


time_lbl = tk.Label(root, text="Time:")
time_lbl.pack()


def updateTime(time):
    time_lbl.configure(text="{}:{} {}".format(*time))


time_picker = SpinTimePickerModern(root)
time_picker.pack()
time_picker.addAll(constants.HOURS12, constants.AM)  # adds hours clock, minutes and period
time_picker.addMinutes()

time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                        hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
time_picker.configure_separator(bg="#404040", fg="#ffffff")
# theme = AnalogThemes(time_picker)
# theme.setDracula()
# theme.setNavyBlue()
# theme.setPurple()
ok_btn = tk.Button(root, text="ok", command=lambda: updateTime(time_picker.time()))
ok_btn.pack()

# Execute Tkinter
root.mainloop()

#
# class Point:
#
#     def __init__(self, a, b):
#         Point.instance = 1
#         self.__iter_pos = 0
#         self.__x = a
#         self.__y = b
#
#     def __dir__(self):
#         return None
#
#     def __str__(self):
#         return f'Point{self.__x, self.__y}'
#
#     def __eq__(self, obj):
#         return self.__x == obj.__x and self.__y == obj.__y
#
#     def __lt__(self, other):
#         return self.__x < other.__x and self.__y < other.__y
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.__iter_pos == 0:
#             self.__iter_pos += 1
#             return self.__x, self.__y
#         elif self.__iter_pos == 1:
#             self.__iter_pos -= 1
#             raise StopIteration
#
#     def __ge__(self, other):
#         return self.__x >= other.__x and self.__y >= other.__y
#
# point_a = Point(9, 7)
# point_b = Point(5, 6)
# print(point_a == point_b)
# print(point_a <= point_b)
# print(point_a <= point_b)
# print(point_a < point_b)
# print(point_a > point_b)
#
#
# class Set:
#     def index(self, a):
#         return a * 3
#
# a = (3,5,6,7)
# b = [3,4,5,6]
# c = Set()
#
# for cls in a, b, c:
#     print(cls.index(5))


# style = ttk.Style()
# # style.map("TNotebook.Tab", background=[("", "white")])
# style.configure('TNotebook.Tab', background="grey", foreground="black", padding=[25, 8], font=("", 13, "bold"))
# style.configure('TNotebook', padding=[10, 10], background="grey")
# create a Notebook to hold both registration form
# self.tab_control = ttk.Notebook(base_frame, takefocus=0)
# self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)
# create tabs
# customer_tab = ttk.Frame(self.tab_control)
# driver_tab = ttk.Frame(self.tab_control)
#
# self.tab_control.add(customer_tab, text="Customer SignUp")
# self.tab_control.add(driver_tab, text="Driver SignUp")
# self.tab_control.pack(expand=1, fill="both")
