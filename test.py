from tkinter import Tk, Label
from PIL import Image, ImageTk

root = Tk()

img = Image.open("res/taxi1.jpg")
imag = ImageTk.PhotoImage(file="res/taxi1.jpg")

label = Label(root, image=imag)
label.pack()

root.mainloop()

# tab control

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
