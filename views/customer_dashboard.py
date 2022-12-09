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
        self.__base_window = parent
        super().__init__(self.__base_window.frame)
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
        self.details_btn = cw.Button(self.__profile_frame, text="Trip Details", **CustomerDashboard.button_args)
        self.details_btn.pack(fill=tk.X, padx=parent.get_width_pct(5))

        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  **CustomerDashboard.button_args
                  ).pack(fill=tk.X, side=tk.BOTTOM)

        # update the idle tasks so the BookingSection can use actual width and height of the widgets in self
        self.update_idletasks()
        # # BOOKING SECTION OR TRIPS DETAIL SECTION WILL BE MANUALLY ADDED BY THE CONTROLLER CLASS IN THE self.base_frame
        booking_section = BookingSection(self.base_frame, controller, self.__base_window)
        booking_section.pack()
        controller.add_view("booking_section", booking_section)

        # TripDetailsSection(self.base_frame, controller, self.__base_window).pack()
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
    def __init__(self, container, controller, base_window):
        self.__base_window = base_window
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
        self.map_style = ttk.Combobox(self.__panel_frame, values=["Normal View", "Satellite View"],
                                      takefocus=0, state="readonly", font=("", 12, "bold", "italic"))
        self.map_style.set("<<Choose Map View>>")
        self.map_style.pack(fill=tk.X, padx=5)
        self.map_style.bind("<<ComboboxSelected>>", controller.change_map_tiles)

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
        self.map.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style

        self.map.pack(fill=tk.BOTH)

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
        top.transient(self.__base_window)
        top.grab_set()
        top.focus_set()

    def __date_picker(self, _):
        top = tk.Toplevel(self.__panel_frame)
        top.geometry(f'{int(self.__base_window.get_width_pct(25))}x{int(self.__base_window.get_height_pct(30))}')
        top.title("Date Picker")
        calendar = Calendar(top, selectmode="day")
        calendar.pack(fill=tk.BOTH)
        btn = cw.Button(top, text="Select Date", **CustomerDashboard.button_args,
                        command=lambda *a: self.__pick_date(calendar.get_date(), top))
        btn.pack(side="bottom", fill=tk.X)
        top.transient(self.__base_window)
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
    def __init__(self, container, controller, base_window):
        self.__base_window = base_window
        style = ttk.Style()
        style.configure("trips.TFrame", background="#ffffff")
        style.configure("trips.TLabel", background="#ffffff")
        style.configure("control.TFrame", background="#ace1af")
        style.configure("labelt.TLabel", background="#ace1af", font=("", 13, "italic"))
        style.configure("pickert.TLabel", background="silver", font=("", 13, "italic"))
        style.configure("pickert.TFrame", background="silver")
        style.configure("hovert.TFrame", background="grey")
        style.configure("hovert.TLabel", background="grey")
        super().__init__(container)
        # define width of map and panel
        self.__trips_width = container.winfo_width() * 0.7
        self.__control_width = container.winfo_width() - self.__trips_width
        self.__height = container.winfo_height()

        self.__trips_frame = ttk.Frame(self, width=self.__trips_width, height=self.__height, style="trips.TFrame")
        self.__trips_frame.propagate(False)

        self.__trips_frame.grid(row=0, column=0, sticky=tk.W)

        self.__control_frame = ttk.Frame(self, width=self.__control_width, height=self.__height,
                                         style="control.TFrame")
        self.__control_frame.propagate(False)
        self.__control_frame.grid(row=0, column=1, sticky=tk.E)
        # add space
        ttk.Label(self.__control_frame, text="", style="user_info.TLabel", font=("", 10)).pack()
        # add history filter box
        self.history_filter = ttk.Combobox(self.__control_frame, values=["Active Trips", "Trips History"],
                                           takefocus=0, state="readonly", font=("", 15, "bold", "italic"))
        self.history_filter.current(0)
        self.history_filter.pack(fill=tk.X, padx=5)
        self.history_filter.bind("<<ComboboxSelected>>", self.handle_combo)
        # add scroller
        self.__s = scroll = cw.ScrollFrame(self.__trips_frame)
        scroll.pack(fill=tk.BOTH, expand=True)

        # create frame to hold all the active bookings
        self.active_holder = ttk.Frame(scroll.frame, style="trips.TFrame")
        # create a table to store all the history
        self.history_table = cw.Table(scroll.frame, width=self.__trips_width, fontsize=15)
        self.history_table.set_columns_width({0: 80, 1: 180})
        self.history_table.set_row_height(50)
        self.history_table.set_heading(["id", "name", "address", "phone", "mobile", "permanent"])
        rows = []
        for i in range(100):
            rows.append([f"data {i ** 4},{j ** 4}" for j in range(6)])
            # self.history_table.add_rows([[f"data {i ** 4},{j ** 4}" for j in range(6)]])
        self.history_table.add_rows(rows)

        # self.history_table.pack(fill=tk.BOTH, expand=True)
        self.active_holder.pack(fill=tk.BOTH, expand=True)

        card = CreateCard(self.active_holder, self.__trips_width, [[], [], [], [], []], height=250)
        card.pack()
        card.add_card([])

    def handle_combo(self, _):
        if self.history_filter.get() == "Active Trips":
            self.__s.reset_view()
            self.history_table.pack_forget()
            self.active_holder.pack(fill=tk.BOTH, expand=True)
            return
        self.__s.reset_view()
        self.active_holder.pack_forget()
        self.history_table.pack(fill=tk.BOTH, expand=True)


class CreateCard(tk.Frame):
    def __init__(self, parent, width, data,
                 height=0, space=2):
        self.__width = width - 20
        self.__height = int(self.__width / 2.7) if not height else height
        self.__space = space
        self.__bg_img = ImageTk.PhotoImage(Image.open("res/card.png").resize((int(self.__width), self.__height)))
        self.__card_list = []  # a list to hold the reference of all card frames

        super().__init__(parent, background="white", borderwidth=0)  # sc = shadow color
        self.__create_cards(data)

    # create cards recursively
    def __create_cards(self, datalist):
        for data in datalist:
            self.__card_list.append(tk.Frame(self, background="white"))
            tk.Label(self.__card_list[-1], text="", font=("", self.__space), background="white").pack()
            cnv = tk.Canvas(self.__card_list[-1], width=self.__width, height=self.__height - 5,
                            background="white", bd=0, highlightthickness=0, relief="ridge")
            cnv.pack()
            cnv.create_image(0, 0, image=self.__bg_img, anchor=tk.NW)
            # create frame to hold all the elements in the card
            frame = tk.Frame(self.__card_list[-1], width=self.__width-40, height=self.__height-35, background="#ebf2f2")
            frame.pack_propagate(False)
            # create a frame to hold labels
            frame_l = tk.Frame(frame, background="#ebf2f2")
            frame_l.grid_propagate(False)
            frame_l.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # create a frame to hold buttons
            frame_b = tk.Frame(frame, background="#ebf2f2")
            frame_b.pack_propagate(False)
            frame_b.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            cnv.create_window(20, 15, window=frame, anchor=tk.NW)
            # create labels to add in frame
            font = ("", 13, "bold", "italic")
            tk.Label(frame_l, text="TripID: ", font=font, justify=tk.LEFT, background="#ebf2f2")\
                .grid(columnspan=5, row=0, column=0)
            tk.Label(frame_l, text="DateTime: ", font=font, justify=tk.LEFT, background="#ebf2f2")\
                .grid(row=0, column=5, columnspan=5)
            tk.Label(frame_l, text="From: ", font=font, justify=tk.LEFT, background="#ebf2f2")\
                .grid(row=1, column=0, columnspan=5)
            tk.Label(frame_l, text="To: ", font=font, justify=tk.LEFT, background="#ebf2f2")\
                .grid(row=1, column=5, columnspan=5)
            tk.Label(frame_l, text="Status: ", font=font, justify=tk.LEFT, background="#ebf2f2")\
                .grid(row=2, column=0, columnspan=5)

            cw.Button(frame_b, text="Payment", font=font,
                      **{k: v for k, v in CustomerDashboard.button_args.items() if k != "font"}
                      ).pack(side=tk.RIGHT, anchor=tk.SE, padx=5)
            cw.Button(frame_b, text="Cancel", font=font,
                      **{k: v for k, v in CustomerDashboard.button_args.items() if k != "font"}
                      ).pack(side=tk.RIGHT, anchor=tk.SE, padx=5)
            self.__card_list[-1].pack()

    # add a new card
    def add_card(self, data):
        # add cards individually from here
        # upcoming bookings will have <cancel> and <details> button
        # completed bookings will have <details> and <payment> button
        # event binding will send back the id of the booking to the function
        self.__create_cards([data])
