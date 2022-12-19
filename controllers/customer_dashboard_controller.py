import tkintermapview
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
        # declare pickup and drop off address
        self.__pickup_marker = None
        self.__drop_off_marker = None
        self.__selection_marker = None  # temporary marker for setting positions
        self.__drive_path = None
        # instantiate Dashboard view
        self.__base_view = CustomerDashboard(self, self.__window, self.__user_info)
        # declare all the views
        self.__booking_view = None
        self.__trips_view = None
        # keep record of currently visible view
        self.__booking_visible = False
        # make booking section page visible for the first run
        self.booking_view()
        # update google map address after the widgets are visible
        load = threading.Timer(1, self.__set_current_location)
        load.start()

    def booking_view(self):
        if self.__trips_view:
            self.__trips_view.pack_forget()
        # set booking view button to be active
        self.__base_view.book_btn["state"] = "disabled"
        self.__base_view.details_btn["state"] = "normal"

        self.__booking_view = BookingSection(self.__base_view.base_frame, self, self.__window)
        self.__booking_view.pack()
        self.__booking_visible = True
        # also update the map to show current location
        self.__set_current_location()

    def trips_view(self):
        if self.__booking_view:
            self.__booking_view.pack_forget()
        # set details view button to be active
        self.__base_view.details_btn["state"] = "disabled"
        self.__base_view.book_btn["state"] = "normal"

        self.__trips_view = TripDetailsSection(self.__base_view.base_frame, self, self.__window)
        self.__trips_view.pack()
        self.__booking_visible = False

    def logout(self):
        self.__home_page(self.__window)

    def __set_current_location(self):
        geo = geocoder.ip("me")
        coord = geo.latlng
        # paths = (27.695525019273244, 85.28963164260394), (27.737999105602512, 85.37726477469697)
        try:
            self.__booking_view.map.set_position(*coord)
        except Exception as e:
            print(e)
        # marker_2 = self.__child_views["booking_section"].map.set_marker(*paths[0], text="Brandenburger Tor")
        # marker_3 = self.__child_views["booking_section"].map.set_marker(*paths[1], text="52.55, 13.4")
        # self.__child_views["booking_section"].map.set_path([marker_2.position, marker_3.position, paths[0], paths[1]])

    def change_map_tiles(self, event):
        # google normal tile server
        tiles = self.__booking_view.map_style.get()
        normal_view = "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga"
        # google satellite tile server
        satellite_view = "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga"
        if tiles == "Satellite View":
            self.__booking_view.map.set_tile_server(satellite_view, max_zoom=22)
            return
        self.__booking_view.map.set_tile_server(normal_view, max_zoom=22)

    # change view inside trips details section i.e. switch between active bookings and history
    def handle_combo(self, _):
        if self.__trips_view.history_filter.get() == "Active Trips":
            self.__trips_view.scroll.reset_view()
            self.__trips_view.history_table.pack_forget()
            self.__trips_view.active_holder.pack(fill="both", expand=True)
            return
        self.__trips_view.scroll.reset_view()
        self.__trips_view.active_holder.pack_forget()
        self.__trips_view.history_table.pack(fill="both", expand=True)

    # method to search the places in map
    def search_map(self):
        place = self.__booking_view.search_box.get().strip()
        if not place:
            return
        self.__booking_view.map.set_address(place)

    def select_pickup_address(self):
        pass

    def select_dropoff_address(self):
        pass

    def set_marker(self, coordinate):
        # add temp marker while the location data is loading
        temp = self.__booking_view.map.set_marker(coordinate[0], coordinate[1], text="<Loading Location>")
        if self.__selection_marker:
            self.__selection_marker.delete()
        # convert current coordinates to the address
        addr = tkintermapview.convert_coordinates_to_address(coordinate[0], coordinate[1])
        add_list = addr.geojson.get('features')[0].get('properties').get('address').split(',')[:4]
        # break long address into two lines
        lines = ','.join(add_list[:2]), ','.join(add_list[2:])
        address = ',\n'.join(lines)
        address = f"{address} ({addr.city})"
        self.__selection_marker = self.__booking_view.map.set_marker(coordinate[0], coordinate[1],
                                                                     text=address)
        temp.delete()
