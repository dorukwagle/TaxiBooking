import tkinter as tk
from tkinter import ttk
import views.custom_widget as cw
from PIL import ImageTk, Image
from tktimepicker import AnalogPicker, AnalogThemes, constants
from tkcalendar import Calendar
import tkintermapview as tkmap


class CustomerDashboard(ttk.Frame):
    # define button configuration
    button_args = dict(takefocus=0, font=("", 20, "bold", "italic"),
                       fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                       bg_pressed="#043927", cursor="hand2")

    def __init__(self, controller, parent, user_info):
        self.__controller = controller
        self.__parent = parent
        super().__init__(self.__parent.frame)
        # configure styles for frames and labels
        style = ttk.Style()
        style.configure("profile.TFrame", background="#A3E3BE")
        style.configure("base.TFrame", background="#ffffff")
        style.configure("user_info.TLabel", background="#A3E3BE", font=("", 15, "italic", "bold"))

        # frame for holding profile, and left panel
        self.__profile_frame = ttk.Frame(self, width=parent.get_width_pct(22), height=parent.get_height_pct(100),
                                         style="profile.TFrame")
        self.__profile_frame.pack_propagate(False)
        self.__profile_frame.grid_propagate(False)
        self.__profile_frame.grid(row=0, column=0, sticky=tk.W)

        # frame for holding booking, and trip details layout
        self.base_frame = ttk.Frame(self, width=parent.get_width_pct(78), height=parent.get_height_pct(100),
                                    style="base.TFrame")
        self.base_frame.pack_propagate(False)
        self.base_frame.grid_propagate(False)
        self.base_frame.grid(row=0, column=1, sticky=tk.E)

        # create avatar
        self.__avatar = ImageTk.PhotoImage(Image.open("res/male_avatar.png").resize(
            (int(parent.get_width_pct(15)), int(parent.get_height_pct(25)))
        ))
        ttk.Label(self.__profile_frame, image=self.__avatar, background="#A3E3BE") \
            .pack(pady=parent.get_height_pct(5))

        ttk.Label(self.__profile_frame, text="Full Name", style="user_info.TLabel").pack()
        ttk.Label(self.__profile_frame, text="@username", style="user_info.TLabel", foreground="gray").pack()

        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 40)).pack()
        # booking button
        self.book_btn = cw.Button(self.__profile_frame, text="Book Trip", **CustomerDashboard.button_args
                                  )
        self.book_btn.pack(fill=tk.X, padx=parent.get_width_pct(5))
        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 10)).pack()

        # Trip details button
        self.details_btn = cw.Button(self.__profile_frame, text="Trip Details", **CustomerDashboard.button_args
                                     )
        self.details_btn.pack(fill=tk.X, padx=parent.get_width_pct(5))

        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  **CustomerDashboard.button_args
                  ).pack(fill=tk.X, side=tk.BOTTOM)

        # update the idle tasks so the BookingSection can use actual width and height of the widgets in self
        self.update_idletasks()
        # BOOKING SECTION OR TRIPS DETAIL SECTION WILL BE MANUALLY ADDED BY THE CONTROLLER CLASS IN THE self.base_frame
        BookingSection(self.base_frame, controller, self.__parent)

        self.pack()


def hover_frame(frame):
    frame.configure(style="hover.TFrame")
    for child in frame.winfo_children():
        child.configure(style="hover.TLabel")


def leave_frame(frame):
    frame.configure(style="picker.TFrame")
    for child in frame.winfo_children():
        child.configure(style="picker.TLabel")


class BookingSection(ttk.Frame):
    def __init__(self, container, controller, parent):
        self.__parent = parent
        style = ttk.Style()
        style.configure("map.TFrame", background="#ffffff")
        style.configure("panel.TFrame", background="#ace1af")
        style.configure("label.TLabel", background="#ace1af", font=("", 13, "italic"))
        style.configure("picker.TLabel", background="silver", font=("", 13, "italic"))
        style.configure("picker.TFrame", background="silver")
        style.configure("hover.TFrame", background="grey")
        style.configure("hover.TLabel", background="grey")
        super().__init__(container)
        # define width of map and panel
        self.__map_width = container.winfo_width() * 0.77
        self.__panel_width = container.winfo_width() - self.__map_width
        self.__height = container.winfo_height()

        self.__map_frame = ttk.Frame(self, width=self.__map_width, height=self.__height, style="map.TFrame")
        self.__map_frame.propagate(False)

        self.__map_frame.grid(row=0, column=0, sticky=tk.W)

        self.__panel_frame = ttk.Frame(self, width=self.__panel_width, height=self.__height,
                                       style="panel.TFrame")
        self.__panel_frame.propagate(False)
        self.__panel_frame.grid(row=0, column=1, sticky=tk.E)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 10)).pack()
        # add search bar and button
        search_frame = ttk.Frame(self.__panel_frame)
        search_frame.pack(fill=tk.X)
        self.search_box = cw.InputBox(search_frame, font=("", 15, "bold", "italic"), width=17,
                                      placeholder="Search Address", placeholder_color="silver")
        self.search_box.pack(side="left")
        search_btn = cw.Button(search_frame, text="Go",
                               **{k: v for k, v in CustomerDashboard.button_args.items() if k != "font"},
                               font=("", 15, "bold", "italic"),
                               command=lambda *a: controller.search_map())
        search_btn.pack(side="right")
        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 5)).pack()
        map_style = ttk.Combobox(self.__panel_frame, values=["Normal View", "Satellite View"],
                                 takefocus=0, state="readonly", font=("", 12, "bold", "italic"))
        map_style.set("<<Choose Map View>>")
        map_style.pack(fill=tk.X, padx=5)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 30)).pack()

        self.pick_label = ttk.Label(self.__panel_frame, text="<<Select Pick Up >>",
                                    justify=tk.LEFT, relief="raised",
                                    wraplength=self.__panel_width * 0.9,
                                    width=self.__panel_width * 0.9, style="label.TLabel")
        self.pick_label.pack()

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 10)).pack()
        cw.Button(self.__panel_frame, text="Set Pickup",
                  **CustomerDashboard.button_args) \
            .pack(padx=self.__panel_width * 0.1, fill=tk.X)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 25)).pack()
        self.drop_label = ttk.Label(self.__panel_frame, text="<<Select Drop Off>>",
                                    justify=tk.LEFT, relief="raised",
                                    wraplength=self.__panel_width * 0.9,
                                    width=self.__panel_width * 0.9, style="label.TLabel")
        self.drop_label.pack()

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 10)).pack()
        cw.Button(self.__panel_frame, text="Set DropOff", **CustomerDashboard.button_args) \
            .pack(padx=self.__panel_width * 0.1, fill=tk.X)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 40)).pack()

        # add date picker
        self.__create_date_picker()
        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 5)).pack()
        # add time picker
        self.__create_time_picker()
        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 40)).pack()
        # ttk.Label(self.__map_frame, image=tk.PhotoImage(file="res/clock_icon.png")).pack()
        cw.Button(self.__panel_frame, text="Confirm Trip", **CustomerDashboard.button_args).pack(fill=tk.X)

        # ----------------------------Add Map-------------------------------------
        self.update_idletasks()
        self.map = tkmap.TkinterMapView(self.__map_frame, width=self.__map_width,
                                        height=self.__height, corner_radius=0)
        # google normal tile server
        self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        # google satellite tile server
        # self.map.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # self.map.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style

        self.map.pack(fill=tk.BOTH)

        self.pack()

    def __create_date_picker(self):
        self.__img_calendar = ImageTk.PhotoImage(Image.open("res/calendar_icon.png").resize((30, 30)))
        dframe = ttk.Frame(self.__panel_frame, style="picker.TFrame", cursor="hand2")
        dframe.pack(padx=self.__panel_width * 0.1, fill=tk.X)

        self.date_input = ttk.Label(dframe, text="<<Select Date>>",
                                    font=("", 15), style="picker.TLabel")
        self.date_input.pack(side="left")
        img = ttk.Label(dframe, image=self.__img_calendar, style="picker.TLabel")
        img.pack(side="right")
        # add action listener to all the three widgets
        self.date_input.bind("<ButtonRelease>", self.__date_picker)
        img.bind("<ButtonRelease>", self.__date_picker)
        dframe.bind("<ButtonRelease>", self.__date_picker)
        dframe.bind("<Enter>", lambda *a: hover_frame(dframe))
        dframe.bind("<Leave>", lambda *a: leave_frame(dframe))

    def __create_time_picker(self):
        self.__img_clock = ImageTk.PhotoImage(Image.open("res/clock_icon.png").resize((30, 30)))
        dframe = ttk.Frame(self.__panel_frame, style="picker.TFrame", cursor="hand2")
        dframe.pack(padx=self.__panel_width * 0.1, fill=tk.X)

        self.time_input = ttk.Label(dframe, text="<<Select Time>>",
                                    font=("", 15), style="picker.TLabel")
        self.time_input.pack(side="left")
        img = ttk.Label(dframe, image=self.__img_clock, style="picker.TLabel")
        img.pack(side="right")
        # add action listener to all three widgets
        self.time_input.bind("<ButtonRelease>", self.__time_picker)
        img.bind("<ButtonRelease>", self.__time_picker)
        dframe.bind("<ButtonRelease>", self.__time_picker)
        dframe.bind("<Enter>", lambda *a: hover_frame(dframe))
        dframe.bind("<Leave>", lambda *a: leave_frame(dframe))

    def __time_picker(self, _):
        top = tk.Toplevel(self.__panel_frame)
        time_input = AnalogPicker(top, type=constants.HOURS12)
        time_input.pack()
        AnalogThemes(time_input).setNavyBlue()
        btn = cw.Button(top, text="Select Time",
                        **CustomerDashboard.button_args,
                        command=lambda *a: self.__pick_time(time_input.time(), top))
        btn.pack(side="bottom", fill=tk.X)
        top.transient(self.__parent)
        top.grab_set()
        top.focus_set()

    def __date_picker(self, _):
        top = tk.Toplevel(self.__panel_frame)
        top.geometry(f'{int(self.__parent.get_width_pct(25))}x{int(self.__parent.get_height_pct(30))}')
        top.title("Date Picker")
        calendar = Calendar(top, selectmode="day")
        calendar.pack(fill=tk.BOTH)
        btn = cw.Button(top, text="Select Date", **CustomerDashboard.button_args,
                        command=lambda *a: self.__pick_date(calendar.get_date(), top))
        btn.pack(side="bottom", fill=tk.X)
        top.transient(self.__parent)
        top.grab_set()
        top.focus_set()

    def __pick_time(self, time, dialog):
        text = f'{time[0]} : {time[1]} : {time[2]}'
        self.time_input.config(text=text)
        dialog.destroy()

    def __pick_date(self, date, dialog):
        self.date_input.config(text=date)
        dialog.destroy()


class TripDetailsSection(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
