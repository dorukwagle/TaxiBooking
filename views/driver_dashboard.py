from tkinter import ttk
import tkinter as tk
import views.custom_widget as cw
from PIL import ImageTk, Image
from tkinter import messagebox


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

        ttk.Label(self.__profile_frame, text=user_info.get('full_name'), style="user_info.TLabel").pack()

        ttk.Label(self.__profile_frame, text=f"#driver@{user_info.get('username')}",
                  style="user_info.TLabel", foreground="gray").pack()

        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 60)).pack()

        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  **self.__button_config, command=controller.sign_out
                  ).pack(fill=tk.X, side=tk.BOTTOM)
        # update idletasks to update the base_frame height
        self.update_idletasks()
        self.pack()

        style = ttk.Style()
        style.layout("driver.TNotebook", [])
        style.configure("driver.TNotebook", highlightbackground="green", tabmargins=0)
        style.configure("driver.TNotebook.Tab", font=("", 13, "bold", "italic"), takefocus=0,
                        width=self.__parent.get_width_pct(80),
                        background="#299617", foreground="white", padding=10, focuscolor="#0a6522")
        style.map("driver.TNotebook.Tab", background=[("selected", "#0a6522")])

        tabs_holder = ttk.Notebook(self.base_frame, style="driver.TNotebook")
        tabs_holder.pack(fill=tk.BOTH, expand=True)
        tabs_holder.bind("<<NotebookTabChanged>>", lambda *a: self.__controller.tab_changed(tabs_holder))
        # create the frames/tabs
        upcoming_tab = ttk.Frame(tabs_holder)
        history_tab = ttk.Frame(tabs_holder)

        tabs_holder.add(upcoming_tab, text="Upcoming Trips")
        tabs_holder.add(history_tab, text="Trips History")

        scroller = cw.ScrollFrame(upcoming_tab)
        scroller.pack(fill=tk.BOTH, expand=True)
        self.upcoming_table = cw.Table(scroller, width=self.__parent.get_width_pct(80), fontsize=15)
        self.upcoming_table.set_columns_width({0: 100, 3: 180, 2: 250})
        self.upcoming_table.set_heading(["Trip Id", "Pick Up", "Drop Off", "Date", "Mark As"])
        self.upcoming_table.set_row_height(40)
        self.upcoming_table.pack()

        scroller = cw.ScrollFrame(history_tab)
        scroller.pack(fill=tk.BOTH, expand=True)
        self.history_table = cw.Table(scroller, width=self.__parent.get_width_pct(80), fontsize=15)
        self.history_table.set_columns_width({0: 190, 3: 180, 2: 250})
        self.history_table.set_heading(["Customer Name", "Pick Up", "Date", "status"])
        self.history_table.set_row_height(40)
        self.history_table.pack()

    @staticmethod
    def confirm_message():
        return messagebox.askyesno("Trip Completion", "Do you want to mark this trip as completed ?")

