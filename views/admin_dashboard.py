from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import views.custom_widget as cw


class AdminDashboard(ttk.Frame):
    def __init__(self, controller, parent):
        self.__window = parent
        self.__controller = controller
        super().__init__(parent.frame)
        # define button arguments
        self.__button_config = dict(takefocus=0, font=("", 20, "bold", "italic"),
                                    fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                                    bg_pressed="#043927", cursor="hand2")
        style = ttk.Style()
        style.configure("profile.TFrame", background="#A3E3BE")
        style.configure("base.TFrame", background="#ffffff")
        style.configure("user_info.TLabel", background="#A3E3BE", font=("", 15, "italic", "bold"))

        # frame for holding profile, and left panel
        self.__profile_frame = ttk.Frame(self, width=parent.get_width_pct(20), height=parent.get_height_pct(100),
                                         style="profile.TFrame")
        self.__profile_frame.pack_propagate(False)
        self.__profile_frame.grid_propagate(False)
        self.__profile_frame.grid(row=0, column=0, sticky=tk.W)

        # frame for holding all the admin pages
        self.base_frame = ttk.Frame(self, width=parent.get_width_pct(80), height=parent.get_height_pct(100),
                                    style="base.TFrame")
        self.base_frame.pack_propagate(False)
        self.base_frame.grid_propagate(False)
        self.base_frame.grid(row=0, column=1, sticky=tk.E)

        # create avatar
        self.__avatar = ImageTk.PhotoImage(Image.open("res/admin_icon.png").resize(
            (int(parent.get_width_pct(13)), int(parent.get_height_pct(23)))
        ))
        ttk.Label(self.__profile_frame, image=self.__avatar, background="#A3E3BE") \
            .pack(pady=parent.get_height_pct(5))

        ttk.Label(self.__profile_frame, text="Full Name", style="user_info.TLabel").pack()
        ttk.Label(self.__profile_frame, text="#admin@username", style="user_info.TLabel", foreground="gray").pack()

        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 40)).pack()

        # add search bar
        self.search_bar = cw.InputBox(self.__profile_frame, placeholder_color="silver", placeholder="Search/filter",
                                      font=("", 15, "bold", "italic"))
        self.search_bar.pack()

        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  **self.__button_config
                  ).pack(fill=tk.X, side=tk.BOTTOM)
        # update idletasks to update the base_frame height
        self.update_idletasks()
        # now create the tabs for holding all the admin control pages
        self.__add_tabs()
        self.pack()

    # method to create and add all the tabs
    def __add_tabs(self):
        frame = self.base_frame
        # configure the styles for the tabs
        style = ttk.Style()
        style.layout("TNotebook", [])
        style.configure("TNotebook", highlightbackground="green", tabmargins=0)
        style.configure("TNotebook.Tab", font=("", 13, "bold", "italic"), takefocus=0, width=frame.winfo_width(),
                        background="#299617", foreground="white", padding=10, focuscolor="#0a6522")
        style.map("TNotebook.Tab", background=[("selected", "#0a6522")])

        tabs_holder = ttk.Notebook(frame)
        tabs_holder.pack(fill=tk.BOTH, expand=True)

        # create the frames/tabs
        request_tab = ttk.Frame(tabs_holder)
        confirmed_tab = ttk.Frame(tabs_holder)
        drivers_tab = ttk.Frame(tabs_holder)
        register_tab = ttk.Frame(tabs_holder)
        history_tab = ttk.Frame(tabs_holder)

        # add all the frames/tabs to the notebook
        tabs_holder.add(request_tab, text="Trip Requests")
        tabs_holder.add(confirmed_tab, text="Confirmed Trips")
        tabs_holder.add(drivers_tab, text="View Drivers")
        tabs_holder.add(register_tab, text="Register Drivers")
        tabs_holder.add(history_tab, text="Trips History")


