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
        # booking_section = BookingSection(self.base_frame, controller, self.__base_window)
        # booking_section.pack()
        # controller.add_view("booking_section", booking_section)

        TripDetailsSection(self.base_frame, controller, self.__base_window).pack()
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
        # add scroller
        scroll = ScrollFrame(self.__trips_frame)
        scroll.pack(fill=tk.BOTH, expand=True)

        # create frame to hold all the active bookings
        self.active_holder = ttk.Frame(scroll, style="trips.TFrame")
        # create frame to store all the history in a table
        self.table_frame = ttk.Frame(scroll, style="trips.TFrame")
        self.table_frame.pack()
        for i in range(100):
            ttk.Label(self.table_frame, text=f"test{i}").pack()
        # self.history_table.set_heading([ "name", "address", "phone"])
        # rows = []
        # for i in range(100):
        #     rows.append([f"data {i+1},{j+1}" for j in range(3)])
        # self.history_table.add_rows(rows)
        # self.table_frame.pack()
        # print(rows)
class Table(ttk.Frame):
    def __init__(self, parent, bgcolor="white",
                 headingcolor="silver",
                 fontcolor="black",
                 hovercolor="silver",
                 heading_fontsize=12,
                 fontsize=10,):
        # check if the heading is set or not
        self.__heading_set = False
        self.__cols_length = 0
        style = ttk.Style()
        style.configure("tableCell.TLabel", fontcolor=fontcolor, background=bgcolor, font=("", fontsize))
        style.configure("tableCellHover.TLabel", fontcolor=fontcolor, background=hovercolor, font=("", fontsize))
        style.configure("tableHeading.TLabel", fontcolor=fontcolor, background=headingcolor,
                        font=("", heading_fontsize, "bold"))
        style.configure("tableRow.TFrame")
        super().__init__(parent)
        self.__heading = ttk.Frame(self)
        self.__heading.pack(fill=tk.X)

    # set heading of the table
    def set_heading(self, heading: list):
        self.__heading_set = True
        self.__cols_length = len(heading)

        for i in range(self.__cols_length):
            ttk.Label(self.__heading, text=heading[i], style="tableHeading.TLabel").pack(side="left", fill=tk.X)

    # add rows data to the table
    def add_rows(self, data: list[list]):
        if not self.__heading_set:
            raise Exception("Table Heading Not Defined, set table heading first...")

        for i in range(len(data)):
            # create a frame
            frame = ttk.Frame(self)
            frame.pack(fill=tk.X)
            frame.rowconfigure(0)
            frame.columnconfigure(self.__cols_length)
            for j in range(self.__cols_length):
                # create label and add to frame
                ttk.Label(frame, text=data[i][j], style="tableCell.TLabel", relief="sunken").pack(side="left")



class Card(tk.Frame):
    def __init__(self, parent, **options):
        super().__init__(parent, bg=options["sc"])  # sc = shadow color
        self.label = tk.Label(self, padx=15, pady=10, background="silver")
        self.label.pack(expand=1, fill="both", padx=(0, options["si"]), pady=(0, options["si"]))  # shadow intensity


class ScrollFrame(ttk.Frame):
    def __init__(self, parent, bg="white"):
        style = ttk.Style()
        style.configure("scrf.TFrame", background=bg)
        style.element_options("Vertical.TScrollbar.thumb")
        style.configure("scr.Vertical.TScrollbar", troughcolor="gray", arrowcolor="black", background="white",
                        bordercolor="white")
        super().__init__(parent, style="scrf.TFrame")
        # create a canvas and scrollbar
        scroller = ttk.Scrollbar(self, orient="vertical", style="scr.Vertical.TScrollbar")
        scroller.pack(fill=tk.Y, side="right")
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=scroller.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroller.config(command=canvas.yview)
        # self.pack_propagate(False)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.frame = frame = ttk.Frame(canvas, style="scrf.TFrame")
        frame_id = canvas.create_window(0, 0, window=frame,
                                        anchor=tk.NW)

        # update and change the size of the canvas and frame when the objects are added
        def __config_frame(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas width of the canvas to fit the frame
                canvas.config(width=frame.winfo_reqwidth())

        frame.bind('<Configure>', __config_frame)

        def __config_canvas(event):
            if frame.winfo_reqwidth() != canvas.winfo_width():
                # update the frame size to the size of frame
                canvas.itemconfigure(frame_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', __config_canvas)

        # define what to do when the mouse wheel is rotated
        def __on_wheel(event):
            scroll = 0
            if event.num == 5 or event.delta == -120:
                scroll += 1
            else:
                scroll -= 1
            canvas.yview_scroll(scroll, "units")

        # now check and start listening to mouse wheel event when the cursor is inside the scroll frame
        def __start_scroll_event(event):
            # start the mouse wheel listener
            canvas.bind_all("<MouseWheel>", __on_wheel)
            canvas.bind_all("<Button-4>", __on_wheel)
            canvas.bind_all("<Button-5>", __on_wheel)

        def __stop_scroll_event(event):
            # stop the mouse wheel listener
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        frame.bind("<Enter>", __start_scroll_event)
        frame.bind("<Leave>", __stop_scroll_event)
