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


class App(tkinter.Tk):

    APP_NAME = "map_view_demo.py"
    WIDTH = 800
    HEIGHT = 750

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Return>", self.search)

        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.search_bar = tkinter.Entry(self, width=50)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        self.search_bar_button = tkinter.Button(master=self, width=8, text="Search", command=self.search)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_bar_clear = tkinter.Button(master=self, width=8, text="Clear", command=self.clear)
        self.search_bar_clear.grid(row=0, column=2, pady=10, padx=10)

        self.map_widget = TkinterMapView(width=self.WIDTH, height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.marker_list_box = tkinter.Listbox(self, height=8)
        self.marker_list_box.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=10)

        self.listbox_button_frame = tkinter.Frame(master=self)
        self.listbox_button_frame.grid(row=2, column=1, sticky="nsew", columnspan=2)

        self.listbox_button_frame.grid_columnconfigure(0, weight=1)

        self.save_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="save current marker",
                                                 command=self.save_marker)
        self.save_marker_button.grid(row=0, column=0, pady=10, padx=10)

        self.clear_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="clear marker list",
                                                  command=self.clear_marker_list)
        self.clear_marker_button.grid(row=1, column=0, pady=10, padx=10)

        self.connect_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="connect marker with path",
                                                    command=self.connect_marker)
        self.connect_marker_button.grid(row=2, column=0, pady=10, padx=10)

        self.map_widget.set_address("NYC")

        self.marker_list = []
        self.marker_path = None

        self.search_marker = None
        self.search_in_progress = False

    def search(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_bar.get()
            self.search_marker = self.map_widget.set_address(address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False

    def save_marker(self):
        if self.search_marker is not None:
            self.marker_list_box.insert(tkinter.END, f" {len(self.marker_list)}. {self.search_marker.text} ")
            self.marker_list_box.see(tkinter.END)
            self.marker_list.append(self.search_marker)

    def clear_marker_list(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)

        self.marker_list_box.delete(0, tkinter.END)
        self.marker_list.clear()
        self.connect_marker()

    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def clear(self):
        self.search_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()