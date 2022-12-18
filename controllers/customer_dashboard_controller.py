from views.customer_dashboard import CustomerDashboard, BookingSection, TripDetailsSection
import threading
import geocoder
from views.base_window import BaseWindow


class CDashboardController:

    def __init__(self, base_window, home_page, user):
        # get instance of the base window
        self.__window = base_window
        # login page controller, to get back to login page when logout
        self.__home_page = home_page

        self.__user_info = user
        # instantiate Dashboard view
        self.__base_view = CustomerDashboard(self, self.__window, self.__user_info)
        # declare all the views
        self.__booking_view = None
        self.__trips_view = None
        # make booking section page visible for the first run
        self.booking_view()
        # update google map address after the widgets are visible
        load = threading.Timer(1, self.__set_current_location)
        load.start()

    def booking_view(self):
        if self.__trips_view:
            self.__trips_view.pack_forget()
        self.__booking_view = BookingSection(self.__base_view.base_frame, self, self.__window)
        self.__booking_view.pack()

    def trips_view(self):
        if self.__booking_view:
            self.__booking_view.pack_forget()
        self.__trips_view = TripDetailsSection(self.__base_view.base_frame, self, self.__window)
        self.__trips_view.pack()

    def logout(self):
        self.__home_page(self.__window)

    def __set_current_location(self):
        geo = geocoder.ip("me")
        coord = geo.latlng
        # paths = (27.695525019273244, 85.28963164260394), (27.737999105602512, 85.37726477469697)
        self.__booking_view.map.set_position(*coord)
        # marker_2 = self.__child_views["booking_section"].map.set_marker(*paths[0], text="Brandenburger Tor")
        # marker_3 = self.__child_views["booking_section"].map.set_marker(*paths[1], text="52.55, 13.4")
        # self.__child_views["booking_section"].map.set_path([marker_2.position, marker_3.position, paths[0], paths[1]])

    def change_map_tiles(self, event):
        # google normal tile server
        # self.__child_views["booking_section"].update_idletasks()
        tiles = self.__booking_view.map_style.get()
        normal_view = "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga"
        # google satellite tile server
        satellite_view = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
        if tiles == "Satellite View":
            self.__booking_view.map.set_tile_server(satellite_view, max_zoom=22)
            return
        self.__booking_view.map.set_tile_server(normal_view, max_zoom=22)
