import tkinter as tk
from tkinter import ttk
import views.custom_widget as cw
from PIL import ImageTk, Image
from tktimepicker import AnalogPicker, AnalogThemes, constants
from tkcalendar import Calendar


class CustomerDashboard(ttk.Frame):
    def __init__(self, controller, parent, user_info):
        self.__controller = controller
        self.__parent = parent
        super().__init__(self.__parent.frame)

        # configure styles for frames and labels
        style = ttk.Style()
        style.configure("b.TFrame", background="#aaff00")
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
                  takefocus=0, font=("", 23, "bold", "italic"),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522", bg_pressed="#043927"
                  ).pack(fill=tk.X, side=tk.BOTTOM)

        # update the idle tasks so the BookingSection can use actual width and height of the widgets in self
        self.update_idletasks()
        # BOOKING SECTION OR TRIPS DETAIL SECTION WILL BE MANUALLY ADDED BY THE CONTROLLER CLASS IN THE self.base_frame
        BookingSection(self.base_frame).pack()

        self.pack()
        parent.mainloop()


class BookingSection(ttk.Frame):
    def __init__(self, container):
        style = ttk.Style()
        style.configure("map.TFrame", background="#22ff00")
        style.configure("panel.TFrame", background="#aaff00")
        style.configure("label.TLabel", background="#aaff00", font=("", 13, "italic"))
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
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 20)).pack()

        self.pick_label = ttk.Label(self.__panel_frame, text="<<Select Pick Up >>",
                                    justify=tk.LEFT, relief="raised",
                                    wraplength=self.__panel_width * 0.9,
                                    width=self.__panel_width * 0.9, style="label.TLabel")
        self.pick_label.pack()

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 10)).pack()
        cw.Button(self.__panel_frame, text="Set Pickup",
                  takefocus=0, font=("", 20, "bold", "italic"),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                  bg_pressed="#043927")\
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
        cw.Button(self.__panel_frame, text="Set DropOff",
                  takefocus=0, font=("", 20, "bold", "italic"),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                  bg_pressed="#043927") \
            .pack(padx=self.__panel_width * 0.1, fill=tk.X)

        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 40)).pack()

        img_calendar = ImageTk.PhotoImage(Image.open("res/calendar_icon.png"))
        self.date_input = ttk.Label(self.__panel_frame, background="silver", text="<<Select Date>>",
                                       font=("", 15), image=img_calendar, compound="right")
        self.date_input.bind("<ButtonRelease>", self.__date_pick)
        self.date_input.pack(padx=self.__panel_width * 0.1, fill=tk.X)
        img_test = ImageTk.PhotoImage(Image.open("res/female_avatar.png"))
        test = ttk.Label(self.__map_frame, image=img_test, text="test image with text", compound="top")
        test.pack()
        # add space
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 5)).pack()
        img_clock = ImageTk.PhotoImage(Image.open("res/clock_icon.png"))
        self.time_input = ttk.Label(self.__panel_frame, background="silver", text="<<Select Time>>",
                                       font=("", 15), image=img_clock, compound="none")
        self.time_input.bind("<ButtonRelease>", self.__pick_time)
        self.time_input.pack(padx=self.__panel_width * 0.1, fill=tk.X)

        # add space
        # ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 40)).pack()
        # ttk.Label(self.__map_frame, image=tk.PhotoImage(file="res/clock_icon.png")).pack()
        ttk.Label(self.__panel_frame, text="", style="label.TLabel", font=("", 40)).pack()
        cw.Button(self.__panel_frame, text="Confirm Trip",
                  takefocus=0, font=("", 20, "bold", "italic"),
                  fg="white", fg_pressed="grey", bg="#299617", bg_hover="#0a6522",
                  bg_pressed="#043927") \
            .pack(fill=tk.X)

        self.pack()

        # create time input
    def __pick_time(self, _):
        top = tk.Toplevel(self.__panel_frame)
        time_input = AnalogPicker(top, type=constants.HOURS12)
        time_input.pack()
        AnalogThemes(time_input).setNavyBlue()

        # create date input calendar
    def __date_pick(self, _):
        top = tk.Toplevel(self.__panel_frame)
        calendar = Calendar(top, selectmode="day")
        calendar.pack()


class TripDetailsSection(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
