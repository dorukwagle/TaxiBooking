from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import views.custom_widget as cw
from views.register import DriverRegistration


class AdminDashboard(ttk.Frame):
    def __init__(self, parent, controller, user):
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
        self.__avatar = ImageTk.PhotoImage(Image.open("res/admin_icon.png").resize(
            (int(self.__parent.get_width_pct(13)), int(self.__parent.get_height_pct(23)))
        ))
        ttk.Label(self.__profile_frame, image=self.__avatar, background="#A3E3BE") \
            .pack(pady=self.__parent.get_height_pct(5))

        ttk.Label(self.__profile_frame, text=user.get("full_name"), style="user_info.TLabel").pack()
        ttk.Label(self.__profile_frame, text=f"#admin@{user.get('username')}", style="user_info.TLabel",
                  foreground="gray").pack()

        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 60)).pack()

        # add search bar
        # self.search_bar = cw.InputBox(self.__profile_frame, placeholder_color="silver", placeholder="Search/filter",
        #                               font=("", 15, "bold", "italic"))
        # self.search_bar.pack()
        # # add space
        # ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 5)).pack()
        #
        # self.search_btn = cw.Button(self.__profile_frame, text="Search",
        #                               **{k: v for k, v in self.__button_config.items() if k != 'font'},
        #                               font=("", 15, 'bold', 'italic'), )
        # self.search_btn.pack(fill=tk.X, padx=15)
        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  **self.__button_config,
                  command=controller.logout).pack(fill=tk.X, side=tk.BOTTOM)
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
        tabs_holder.bind("<<NotebookTabChanged>>", lambda *a: self.__controller.tab_changed(tabs_holder))
        # create the frames/tabs
        request_tab = ttk.Frame(tabs_holder)
        confirmed_tab = ttk.Frame(tabs_holder)
        drivers_tab = ttk.Frame(tabs_holder)
        register_tab = tk.Frame(tabs_holder, background="white")
        history_tab = ttk.Frame(tabs_holder)

        # add all the frames/tabs to the notebook
        tabs_holder.add(request_tab, text="Trip Requests")
        tabs_holder.add(confirmed_tab, text="Confirmed Trips")
        tabs_holder.add(drivers_tab, text="View Drivers")
        tabs_holder.add(register_tab, text="Register Drivers")
        tabs_holder.add(history_tab, text="Trips History")

        # update idealtasks before adding other widgets
        frame.update_idletasks()

        # create trip details table
        scroller = cw.ScrollFrame(request_tab)
        scroller.pack(fill=tk.BOTH, expand=True)
        self.requests_v = TripRequests(scroller.frame, self.__controller, width=frame.winfo_width())

        # create confirmed trips table
        scroller = cw.ScrollFrame(confirmed_tab)
        scroller.pack(fill=tk.BOTH, expand=True)
        self.confirmed_v = ConfirmedTrips(scroller.frame, self.__controller, width=frame.winfo_width())

        # create View drivers table
        scroller = cw.ScrollFrame(drivers_tab)
        scroller.pack(fill=tk.BOTH, expand=True)
        self.drivers_v = ViewDrivers(scroller.frame, self.__controller, width=frame.winfo_width())

        # create trips history table
        scroller = cw.ScrollFrame(history_tab)
        scroller.pack(fill=tk.BOTH, expand=True)
        self.history_v = TripsHistory(scroller.frame, self.__controller, width=frame.winfo_width())

        # create driver registration tab
        self.register_v = DriverRegistration(register_tab, self.__controller)
        self.register_v.pack(pady=100)

    def show_available_drivers(self, data):
        available = tk.Toplevel(self.__parent)
        available.title("Drivers for the trip")
        # create a table to hold drivers list
        scroller = cw.ScrollFrame(available)
        scroller.pack(fill="both", expand=True)
        available_drivers = cw.Table(scroller, width=1000, fontsize=15)
        available_drivers.set_columns_width({0: 150, 3: 150})
        available_drivers.set_heading(["driver id", "Full Name", "License Id", "Assign"])

        available_drivers.set_row_height(40)
        available_drivers.pack()
        # fill the table
        available_drivers.reset()
        available_drivers.add_rows(data)

        cw.Button(available, text="Done",
                  **self.__button_config,
                  command=available.destroy).pack(fill='x', expand=True)
        available.transient(self.__parent)
        available.grab_set()
        available.focus_set()


class TripRequests:
    def __init__(self, parent, controller, width):
        self.__parent = parent
        self.__controller = controller

        # create a table to hold trip requests
        self.trips_request_table = cw.Table(parent, width=width, fontsize=15)
        self.trips_request_table.set_columns_width({0: 80, 1: 190, 4: 180, 3: 250})
        self.trips_request_table.set_heading(["trip_id", "Customer Name", "Pick Up", "Date", "Driver"])
        self.trips_request_table.set_row_height(40)
        self.trips_request_table.pack()


class ConfirmedTrips:
    def __init__(self, parent, controller, width):
        self.__parent = parent
        self.__controller = controller

        # create a table to hold confirmed trips
        self.confirmed_trips_table = cw.Table(parent, width=width, fontsize=15)
        self.confirmed_trips_table.set_columns_width({0: 200, 1: 190, 5: 180, 3: 250})
        self.confirmed_trips_table.set_heading(["Customer Name", "Telephone", "Pick Up", "Date", "Driver", "Status"])
        self.confirmed_trips_table.set_row_height(40)
        self.confirmed_trips_table.pack()


class ViewDrivers:
    def __init__(self, parent, controller, width):
        self.__parent = parent
        self.__controller = controller

        # create a table to hold drivers list
        self.drivers_table = cw.Table(parent, width=width, fontsize=15)
        self.drivers_table.set_columns_width({0: 100})
        self.drivers_table.set_heading(["driver id", "Full Name", "License Id"])
        self.drivers_table.set_row_height(40)
        self.drivers_table.pack()


class TripsHistory:
    def __init__(self, parent, controller, width):
        self.__parent = parent
        self.__controller = controller

        # create a table to hold trips history
        self.trips_history_table = cw.Table(parent, width=width, fontsize=15)
        self.trips_history_table.set_columns_width({0: 240, 4: 200, 3: 250, 2: 200})
        self.trips_history_table.set_heading(["Customer Name", "Pick Up", "Date", "Driver", "Status"])
        self.trips_history_table.set_row_height(40)
        self.trips_history_table.pack()
