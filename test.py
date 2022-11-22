#
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter_input_box.input_box import InputBox
#
# class BaseWindow(tk.Tk):
#     def __init__(self):
#         super(BaseWindow, self).__init__()
#         self.geometry("800x700")
#         self.title("test title")
#
#         frame = ttk.Frame(self)
#         frame.pack()
#         ttk.Label(frame, text="test label").pack()
#         self.__img = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
#             (200, 200)))
#         ttk.Label(frame, image=self.__img).pack()
#         InputBox(frame, placeholder="testing", placeholder_color="red", font_color="green").pack()
#         frame_parent = ttk.Frame(self)
#         frame_parent.pack()
#
#         ParentWindow(frame_parent, self)
#         # self.mainloop()
#
#
# class ParentWindow(ttk.Frame):
#     def __init__(self, parent, app):
#         super(ParentWindow, self).__init__(parent)
#         self.pack()
#         ttk.Label(self, text="parent label test").pack()
#
#         self.__img = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
#             (200, 200)))
#         ttk.Label(self, image=self.__img).pack()
#         ttk.Label(self, text="test label").pack()
#
#         frame_child = ttk.Frame(self)
#         frame_child.pack()
#
#         ChildWindow(frame_child, app)
#         # self.mainloop()
#         # app.mainloop()
#
#
# class ChildWindow(ttk.Frame):
#     def __init__(self, parent, app):
#         super(ChildWindow, self).__init__(parent)
#         self.pack()
#         ttk.Label(self, text="child label test").pack()
#
#         self.__img = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
#             (200, 200)))
#         ttk.Label(self, image=self.__img).pack()
#         ttk.Label(self, text="test label").pack()
#         # self.mainloop()
#         # app.mainloop()
#
#
# if __name__ == '__main__':
#     # BaseWindow().mainloop()
#     # BaseWindow().mainloop()
#
#     from tkinter import *
#     from tkinter.simpledialog import Dialog, SimpleDialog
#     from tkinter.messagebox import showinfo
#
#     # Create the root window
#     # with specified size and title
#     root = Tk()
#     root.title("Root Window")
#     root.geometry("450x300")
#
#     # Create label for root window
#     label1 = Label(root, text="This is the root window")
#
#     # SimpleDialog(root, "hello")
#     # define a function for 2nd toplevel
#     # window which is not associated with
#     # any parent windo
#     def exit_top():
#         top1.destroy()
#         top1.grab_release()
#     # define a function for 1st toplevel
#     # which is associated with root window.
#     def show_top():
#         open_Toplevel1()
#
#     def grab(**k):
#         top1.focus_set()
#         top1.grab_set()
#         top1.transient(root)
#         top1.wait_window(top1)
#         # print(k)
#
#     # grab(c="hello", aa="df", font=("as", 33))
#     def open_Toplevel1():
#         # Create widget
#         global top1
#         top1 = Toplevel(root)
#         top1.grab_set()
#         # Define title for window
#         top1.title("Toplevel1")
#
#         # specify size
#         top1.geometry("200x200")
#
#         # Create label
#         label = Label(top1,
#                       text="This is a Toplevel1 window")
#
#         # Create Exit button
#         button1 = Button(top1, text="Exit", command=exit_top)
#         button1 = Button(top1, text="disable parent", command=grab)
#
#         # create button to open toplevel2
#
#         label.pack()
#         button1.pack()
#
#         # Display until closed manually
#         # root.deiconify()
#
#
#     # Create button to open toplevel1
#     button = Button(root, text="open toplevel1",
#                     command=show_top)
#
#     label1.pack()
#
#     # position the button
#     button.place(x=155, y=50)
#
#     # Display until closed manually
#     root.mainloop()
#
# ################################################################################
import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView


import tkinter as tk


class MDLabel(tk.Frame):

    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent, bg=options["sc"])  # sc = shadow color
        self.label = tk.Label(self, text=options["text"], padx=15, pady=10, background="silver")
        self.label.pack(expand=1, fill="both", padx=(0, options["si"]), pady=(0, options["si"]))  # shadow intensity


root = tk.Tk()
root.geometry("600x300+900+200")

main_frame = tk.Frame(root, bg="white")
body_frame = tk.Frame(main_frame, bg="white")

for i in range(3):
    md_label = MDLabel(body_frame, sc="grey", si=2, text="Label " + str(i))
    md_label.pack(expand=1, fill="both", pady=10)

body_frame.pack(expand=1, fill="both", pady=10, padx=10)
main_frame.pack(expand=True, fill="both")

root.mainloop()