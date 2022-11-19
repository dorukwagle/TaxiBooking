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


class Point:

    def __init__(self, a, b):
        Point.instance = 1
        self.__iter_pos = 0
        self.__x = a
        self.__y = b

    def __dir__(self):
        return None

    def __str__(self):
        return f'Point{self.__x, self.__y}'

    def __eq__(self, obj):
        return self.__x == obj.__x and self.__y == obj.__y

    def __lt__(self, other):
        return self.__x < other.__x and self.__y < other.__y

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iter_pos == 0:
            self.__iter_pos += 1
            return self.__x, self.__y
        elif self.__iter_pos == 1:
            self.__iter_pos -= 1
            raise StopIteration

    def __ge__(self, other):
        return self.__x >= other.__x and self.__y >= other.__y

point_a = Point(9, 7)
point_b = Point(5, 6)
print(point_a == point_b)
print(point_a <= point_b)
print(point_a <= point_b)
print(point_a < point_b)
print(point_a > point_b)


class Set:
    def index(self, a):
        return a * 3

a = (3,5,6,7)
b = [3,4,5,6]
c = Set()

for cls in a, b, c:
    print(cls.index(5))


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
