import tkinter as tk
from tkinter import ttk, messagebox

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
        img_path = "res/male_avatar.png" if user_info.get("gender") == "male" else "res/female_avatar.png"
        self.__avatar = ImageTk.PhotoImage(Image.open(img_path).resize(
            (int(parent.get_width_pct(15)), int(parent.get_height_pct(25)))
        ))
        ttk.Label(self.__profile_frame, image=self.__avatar, background="#A3E3BE") \
            .pack(pady=parent.get_height_pct(5))

        ttk.Label(self.__profile_frame, text=user_info.get("full_name"), style="user_info.TLabel").pack()
        ttk.Label(self.__profile_frame, text='@' + user_info.get("username"),
                  style="user_info.TLabel", foreground="gray").pack()

        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 40)).pack()
        # booking button
        self.book_btn = cw.Button(self.__profile_frame, text="Book Trip", **CustomerDashboard.button_args,
                                  command=self.__controller.booking_view)
        self.book_btn.pack(fill=tk.X, padx=parent.get_width_pct(5))
        # add space
        ttk.Label(self.__profile_frame, text="", style="user_info.TLabel", font=("", 10)).pack()

        # Trip details button
        self.details_btn = cw.Button(self.__profile_frame, text="Trip Details", **CustomerDashboard.button_args,
                                     command=self.__controller.trips_view)
        self.details_btn.pack(fill=tk.X, padx=parent.get_width_pct(5))
        # sign out button
        cw.Button(self.__profile_frame, text="Sign Out",
                  **CustomerDashboard.button_args, command=self.__controller.logout
                  ).pack(fill=tk.X, side=tk.BOTTOM)

        # update the idle tasks so the BookingSection can use actual width and height of the widgets in self
        self.update_idletasks()
        self.pack()

    @staticmethod
    def show_error():
        messagebox.showerror("Request Timeout", "Check your internet connection")


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
        self.__controller = controller
        style = ttk.Style()
        style.configure("map.TFrame", background="#ffffff")
        style.configure("panel.TFrame", background="#ace1af")
        style.configure("label.TLabel", background="#ace1af", font=("", 10, "italic"))
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
                               command=self.__controller.search_map)
        search_btn.pack(side="right")
        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 5)).pack()
        self.map_style = ttk.Combobox(self.__panel_frame, values=["Normal View", "Satellite View"],
                                      takefocus=0, state="readonly", font=("", 12, "bold", "italic"))
        self.map_style.set("<<Choose Map View>>")
        self.map_style.pack(fill=tk.X, padx=5)
        self.map_style.bind("<<ComboboxSelected>>", self.__controller.change_map_tiles)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 30)).pack()

        self.pick_label = ttk.Label(self.__panel_frame, text="<<Select Pick Up >>",
                                    justify=tk.LEFT, relief="raised", wraplength=self.__panel_width * 0.9,
                                    width=self.__panel_width * 0.9, style="label.TLabel")
        self.pick_label.pack()

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 10)).pack()
        self.pickup_btn = cw.Button(self.__panel_frame, text="Set Pickup",
                                    **CustomerDashboard.button_args, command=self.__controller.select_pickup_address)
        self.pickup_btn.pack(padx=self.__panel_width * 0.1, fill=tk.X)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 25)).pack()
        self.drop_label = ttk.Label(self.__panel_frame, text="<<Select Drop Off>>",
                                    justify=tk.LEFT, relief="raised", wraplength=self.__panel_width * 0.9,
                                    width=self.__panel_width * 0.9, style="label.TLabel")
        self.drop_label.pack()

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 10)).pack()
        self.dropoff_btn = cw.Button(self.__panel_frame, text="Set DropOff",
                                     **CustomerDashboard.button_args, command=self.__controller.select_dropoff_address)
        self.dropoff_btn.pack(padx=self.__panel_width * 0.1, fill=tk.X)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 20)).pack()

        # add date picker
        self.__create_date_picker()
        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 5)).pack()
        # add time picker
        self.__create_time_picker()
        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 20)).pack()
        cw.Button(self.__panel_frame, text="Confirm Trip", **CustomerDashboard.button_args,
                  command=self.__controller.confirm_booking).pack(fill=tk.X, side=tk.BOTTOM)
        self.error_msg = ttk.Label(self.__panel_frame, text="", style="label.TLabel", foreground="red", font=("", 15))
        self.error_msg.pack(fill=tk.X, side=tk.BOTTOM)

        # ----------------------------Add Map-------------------------------------
        self.update_idletasks()
        self.map = tkmap.TkinterMapView(self.__map_frame, width=self.__map_width,
                                        height=self.__height, corner_radius=0)
        self.map.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        self.map.add_left_click_map_command(self.__controller.set_marker)
        self.map.pack(fill=tk.BOTH)
        # create some location icons for marker
        self.pickup_mark = ImageTk.PhotoImage(Image.open("res/green_location.png").resize(
            (60, 90)
        ))
        self.dropoff_mark = ImageTk.PhotoImage(Image.open("res/red_location.png").resize(
            (60, 90)
        ))
        self.temp_mark = ImageTk.PhotoImage(Image.open("res/blue_location.png").resize(
            (60, 70)
        ))

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
        top.title("Select Time")
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
        top.title("Select Date")
        calendar = Calendar(top, selectmode="day", date_pattern="YYYY-MM-DD")
        calendar.pack(fill=tk.BOTH)
        btn = cw.Button(top, text="Select Date", **CustomerDashboard.button_args,
                        command=lambda *a: self.__pick_date(calendar.get_date(), top))
        btn.pack(side="bottom", fill=tk.X)
        top.transient(self.__base_window)
        top.grab_set()
        top.focus_set()

    def __pick_time(self, time, dialog):
        # function to convert hour to 24 hours format
        def converted(_hour):
            return int(_hour) + 12 if int(hour) < 12 else _hour

        hour = time[0] if len(str(time[0])) == 2 else f"0{time[0]}"
        minute = time[1] if len(str(time[1])) == 2 else f"0{time[1]}"
        second = "00"
        # convert to 24 hours format
        hour = converted(hour) if time[2].lower() == "pm" else hour
        text = f'{hour}:{minute}:{second}'
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
        self.__trips_width = container.winfo_width() * 0.85
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
        self.history_filter.bind("<<ComboboxSelected>>", controller.handle_combo)
        # add scroller
        self.scroll = scroll = cw.ScrollFrame(self.__trips_frame)
        scroll.pack(fill=tk.BOTH, expand=True)

        # create frame to hold all the active bookings
        self.active_holder = ttk.Frame(scroll.frame, style="trips.TFrame")
        # create a table to store all the history
        self.history_table = cw.Table(scroll.frame, width=self.__trips_width, fontsize=15)
        self.history_table.set_columns_width({0: 60, 1: 250, 3: 205, 4: 150})
        self.history_table.set_heading(["id", "Driver", "Drop Off", "Date", "Status"])
        self.history_table.set_row_height(40)
        self.active_holder.pack(fill=tk.BOTH, expand=True)

        self.card = CreateCard(self.active_holder, self.__trips_width, height=280)
        self.card.set_cancel_cb(controller.cancel_booking)
        self.card.set_payment_cb(controller.payment_info)
        self.card.pack()

    def trip_information(self, data):
        top = tk.Toplevel(self.__trips_frame)
        top.title("Payment Information")

        btn_pay = cw.Button(top, text="Select Time",
                            **CustomerDashboard.button_args,
                            )
        btn_pay.pack(side="bottom", fill=tk.X)
        cw.Button(top, text="Select Time",
                  **CustomerDashboard.button_args,
                  command=top.destroy).pack(side="bottom", fill=tk.X)
        top.transient(self.__base_window)
        top.grab_set()
        top.focus_set()


class CreateCard(tk.Frame):
    def __init__(self, parent, width,
                 height=0, space=2):
        self.__width = width - 20
        self.__height = int(self.__width / 2.7) if not height else height
        self.__space = space
        self.__bg_img = ImageTk.PhotoImage(Image.open("res/card.png").resize((int(self.__width), self.__height)))
        self.__card_list = []  # a list to hold the reference of all card frames

        # store the callback methods
        self.__cancel_callback = None
        self.__payment_callback = None

        super().__init__(parent, background="white", borderwidth=0)  # sc = shadow color

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
            frame = tk.Frame(self.__card_list[-1], width=self.__width - 40, height=self.__height - 35,
                             background="#ebf2f2")
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
            font = ("", 11, "bold", "italic")
            id_date_f = tk.Frame(frame_l, background="#ebf2f2")
            id_date_f.pack(fill=tk.X)
            tk.Label(id_date_f, text=f"TRIP ID: {data.get('trip_id')}", font=font, justify=tk.LEFT,
                     background="#ebf2f2").pack(side="left")
            tk.Label(id_date_f, text=f"PICKUP: {data.get('pickup_datetime')}", font=font, justify=tk.LEFT,
                     background="#ebf2f2").pack(side="left")
            tk.Label(id_date_f, text=f"DROPOFF: {data.get('drop_off_datetime')}", font=font, justify=tk.LEFT,
                     background="#ebf2f2").pack(side="left")
            tk.Label(frame_l, text=f"FROM: {data.get('pickup_address')}", font=font, justify=tk.LEFT,
                     wraplength=self.__width - 45, background="#ebf2f2").pack(anchor=tk.W)
            tk.Label(frame_l, text=f"TO: {data.get('drop_off_address')}", font=font, justify=tk.LEFT,
                     wraplength=self.__width - 45, background="#ebf2f2").pack(anchor=tk.W)
            driver_price_f = tk.Frame(frame_l, background="#ebf2f2")
            driver_price_f.pack(fill=tk.X)
            tk.Label(driver_price_f, text=f"DRIVER: {data.get('driver_name')}", font=font, justify=tk.LEFT,
                     background="#ebf2f2").pack(side="left")
            tk.Label(driver_price_f, text=f"PRICE: Rs.{data.get('price')}", font=font, justify=tk.LEFT,
                     background="#ebf2f2").pack(side="left")
            tk.Label(frame_l, text=f"STATUS: {data.get('status')}", font=font, justify=tk.LEFT,
                     background="#ebf2f2").pack(anchor=tk.W)

            cw.Button(frame_b, text="Payment", font=font,
                      **{k: v for k, v in CustomerDashboard.button_args.items() if k != "font"},
                      command=lambda ind=len(self.__card_list) - 1, tid=data.get("trip_id"): self.__callpay(ind, tid)) \
                .pack(side=tk.RIGHT, anchor=tk.SE, padx=5)
            cw.Button(frame_b, text="Cancel", font=font,
                      **{k: v for k, v in CustomerDashboard.button_args.items() if k != "font"},
                      command=lambda ind=len(self.__card_list) - 1, tid=data.get("trip_id"): self.__callcan(ind, tid)
                      ).pack(side=tk.RIGHT, anchor=tk.SE, padx=5)
            self.__card_list[-1].pack()

    # callback for payment button
    def __callpay(self, ind, tid):
        if not self.__payment_callback:
            return
        self.__payment_callback(ind, tid)

    # callback for cancel button
    def __callcan(self, ind, tid):
        if not self.__cancel_callback:
            return
        self.__cancel_callback(ind, tid)

    # set callback methods
    def set_cancel_cb(self, callback):
        self.__cancel_callback = callback

    def set_payment_cb(self, callback):
        self.__payment_callback = callback

    # add a new card
    def add_card(self, data: dict):
        # add cards individually from here
        # upcoming bookings will have <cancel> and <details> button
        # completed bookings will have <details> and <payment> button
        # event binding will send back the id of the booking to the function
        self.__create_cards([data])

    def add_cards(self, datalist: [{}]):
        self.__create_cards(datalist)

    # remove the card at given index
    def remove(self, index):
        self.__card_list[index].destroy()
        self.__card_list.pop(index)

    # delete all the cards
    def reset(self):
        for card in self.__card_list:
            card.destroy()
