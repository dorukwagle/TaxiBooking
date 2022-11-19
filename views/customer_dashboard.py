import tkinter as tk
from tkinter import ttk
import views.custom_widget as cw
from pathlib import Path
from PIL import ImageTk, Image


class CustomerDashboard(ttk.Frame):
    def __init__(self, controller, parent, user_info):
        self.__controller = controller
        self.__parent = parent
        super().__init__(self.__parent.frame)

        # configure styles for frames and labels
        style = ttk.Style()
        style.configure("profile.TFrame", background="#A3E3BE")
        style.configure("base.TFrame", background="#00ffff")
        style.configure("user_info.TLabel", background="#A3E3BE", font=("", 15, "italic", "bold"))

        # frame for holding profile, and left panel
        self.__profile_frame = ttk.Frame(self, width=parent.get_width_pct(25), height=parent.get_height_pct(100),
                                         style="profile.TFrame")
        self.__profile_frame.propagate(False)
        self.__profile_frame.grid(row=0, column=0, sticky=tk.W)

        # frame for holding booking, and trip details layout
        self.base_frame = ttk.Frame(self, width=parent.get_width_pct(75), height=parent.get_height_pct(100),
                                    style="base.TFrame")
        self.base_frame.propagate(False)
        self.base_frame.grid(row=0, column=1, sticky=tk.E)

        # create avatar
        avatar = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
            (int(parent.get_width_pct(15)), int(parent.get_height_pct(25)))
        ))
        ttk.Label(self.__profile_frame, image=avatar, background="#A3E3BE") \
            .pack(pady=parent.get_height_pct(5))

        ttk.Label(self.__profile_frame, text="Full Name", style="user_info.TLabel").pack()
        ttk.Label(self.__profile_frame, text="@username", style="user_info.TLabel", foreground="gray").pack()

        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 40)).pack()
        # booking button
        self.book_btn = cw.Button(self.__profile_frame, text="Book Trip",
                                  takefocus=0, font=("", 20, "bold", "italic"),
                                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927",
                                  )
        self.book_btn.pack(fill=tk.X, padx=parent.get_width_pct(5))
        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 10)).pack()

        # Trip details button
        self.details_btn = cw.Button(self.__profile_frame, text="Trip Details",
                                     takefocus=0, font=("", 20, "bold", "italic"),
                                     fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                                     bg_pressed="#043927"
                                     )
        self.details_btn.pack(fill=tk.X, padx=parent.get_width_pct(5))

        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  takefocus=0, font=("", 23, "bold"),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927"
                  ).pack(fill=tk.X, side=tk.BOTTOM)

        self.pack()
        parent.mainloop()
