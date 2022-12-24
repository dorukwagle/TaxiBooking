from tkinter import ttk
import tkinter as tk
import views.custom_widget as cw
from PIL import ImageTk, Image


class DriverDashboard(tk.Frame):
    def __init__(self, parent, controller, user_info):
        self.__parent = parent
        self.__controller = controller

        super().__init__(self.__parent.frame)
        # define button arguments
        self.__button_config = dict(takefocus=0, font=("", 20, "bold", "italic"),
                                    fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                                    bg_pressed="#043927", cursor="hand2")
        style = ttk.Style()
        style.configure("profile.TFrame", background="#A3E3BE")
        style.configure("base.TFrame", background="#ffffff")
        style.configure("user_info.TLabel", background="#A3E3BE", font=("", 15, "italic", "bold"))

        # frame for holding profile, and left panel
        self.__profile_frame = ttk.Frame(self, width=self.__parent.get_width_pct(20),
                                         height=self.__parent.get_height_pct(100),
                                         style="profile.TFrame")
        self.__profile_frame.pack_propagate(False)
        self.__profile_frame.grid_propagate(False)
        self.__profile_frame.grid(row=0, column=0, sticky=tk.W)

        # frame for holding all the admin pages
        self.base_frame = ttk.Frame(self, width=self.__parent.get_width_pct(80),
                                    height=self.__parent.get_height_pct(100),
                                    style="base.TFrame")
        self.base_frame.pack_propagate(False)
        self.base_frame.grid_propagate(False)
        self.base_frame.grid(row=0, column=1, sticky=tk.E)

        # create avatar
        self.__avatar = ImageTk.PhotoImage(Image.open("res/driver.png").resize(
            (int(self.__parent.get_width_pct(13)), int(self.__parent.get_height_pct(23)))
        ))
        ttk.Label(self.__profile_frame, image=self.__avatar, background="#A3E3BE") \
            .pack(pady=self.__parent.get_height_pct(5))

        ttk.Label(self.__profile_frame, text="Full Name", style="user_info.TLabel").pack()
        ttk.Label(self.__profile_frame, text="#driver@username", style="user_info.TLabel", foreground="gray").pack()

        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 60)).pack()

        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  **self.__button_config
                  ).pack(fill=tk.X, side=tk.BOTTOM)
        # update idletasks to update the base_frame height
        self.update_idletasks()
        self.pack()
