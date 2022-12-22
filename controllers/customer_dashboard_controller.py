from datetime import datetime, timedelta
import tkintermapview
from views.customer_dashboard import CustomerDashboard, BookingSection, TripDetailsSection
from models.customer_dashboard_model import CDashboardModel, InvalidData
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
        # declare a variable to store whether the marker is clicked, and stop further callback on map click
        self.__marker_clicked = False

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
        # call __display_active_trips to load trips data
        self.__display_active_trips()
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

    # method to search the places in map
    def search_map(self):
        place = self.__booking_view.search_box.get().strip()
        if not place:
            return
        self.__booking_view.map.set_address(place)

    def __get_marker_info(self):
        if not self.__selection_marker:
            return None
        text = self.__selection_marker.text
        position = self.__selection_marker.position
        self.__selection_marker.delete()
        self.__selection_marker = None
        return text, position

    def select_pickup_address(self):
        data = self.__get_marker_info()
        if not data:
            return
        self.__pickup_marker = self.__booking_view.map.set_marker(*data[1], icon=self.__booking_view.pickup_mark,
                                                                  text=data[0], command=self.__marker_click,
                                                                  text_color="black")
        self.__booking_view.pickup_btn.config(state="disabled")
        self.__booking_view.pick_label.config(text=self.__pickup_marker.text)
        # check if both the address are selected and draw the path
        self.__draw_path()

    def select_dropoff_address(self):
        data = self.__get_marker_info()
        if not data:
            return
        self.__drop_off_marker = self.__booking_view.map.set_marker(*data[1], icon=self.__booking_view.dropoff_mark,
                                                                    text=data[0], command=self.__marker_click,
                                                                    text_color="black")
        self.__booking_view.dropoff_btn.config(state="disabled")
        self.__booking_view.drop_label.config(text=self.__drop_off_marker.text)
        # draw path if both the addresses are selected
        self.__draw_path()

    # draw the path between pickup and drop off position
    def __draw_path(self):
        # check if both the positions are available
        if self.__pickup_marker and self.__drop_off_marker:
            self.__drive_path = self.__booking_view.map.set_path([self.__pickup_marker.position,
                                                                  self.__drop_off_marker.position])

    # when one of the marker is clicked, delete the marker and the path if exists
    def __marker_click(self, marker):
        self.__marker_clicked = True
        if marker is self.__selection_marker:
            return
        if marker is self.__pickup_marker:
            self.__pickup_marker.delete()
            self.__booking_view.pick_label.config(text="<<Select Pick Up>>")
            self.__booking_view.pickup_btn.config(state="normal")
            self.__pickup_marker = None
        else:
            self.__drop_off_marker.delete()
            self.__booking_view.drop_label.config(text="<<Select Drop Off>>")
            self.__booking_view.dropoff_btn.config(state="normal")
            self.__drop_off_marker = None

        if self.__drive_path:
            self.__drive_path.delete()
            self.__drive_path = None

    def set_marker(self, coordinate):
        # do not execute if the user clicked on marker
        if self.__marker_clicked:
            self.__marker_clicked = False
            return
        # add temp marker while the location data is loading
        temp = self.__booking_view.map.set_marker(coordinate[0], coordinate[1], text="<Loading Location>",
                                                  icon=self.__booking_view.temp_mark)
        if self.__selection_marker:
            self.__selection_marker.delete()
        else:
            # just to delete it later
            temp2 = self.__booking_view.map.set_marker(coordinate[0], coordinate[1], text="<Loading Location>")
            # delete the temp2, so the temp gets enough time to appear in the map
            temp2.delete()
        address = None
        add_list = None
        try:
            # convert current coordinates to the address
            addr = tkintermapview.convert_coordinates_to_address(coordinate[0], coordinate[1])
            add_list = addr.geojson.get('features')[0].get('properties').get('address').split(',')
            # break long address into two lines
            lines = ','.join(add_list[:2]), ','.join(add_list[2:5])
            address = ',\n'.join(lines)
            address = f"{address} ({addr.city})"
        except IndexError as e:
            temp.delete()
            self.__base_view.show_error()
            return

        self.__selection_marker = \
            self.__booking_view.map.set_marker(coordinate[0], coordinate[1], text=address, command=self.__marker_click,
                                               icon=self.__booking_view.temp_mark, text_color="black")
        temp.delete()

    # confirm the booking
    def confirm_booking(self):
        # create customer dashboard model
        model = CDashboardModel()
        # fetch the booking details from the view
        time_input = self.__booking_view.time_input['text'].strip()
        date_input = self.__booking_view.date_input['text'].strip()
        if time_input == "<<Select Time>>" or date_input == "<<Select Date>>" \
                or not self.__pickup_marker or not self.__drop_off_marker:
            self.__booking_view.error_msg.config(text="Please fill all the details")
            return
        date_time = f"{date_input} {time_input}"
        pickup_date_time = datetime.timestamp(datetime.fromisoformat(date_time))
        pickup_address = self.__pickup_marker.text
        drop_off_address = self.__drop_off_marker.text
        # calculate the displacement between pickup and drop off and the driving duration
        info = model.get_driving_info(self.__pickup_marker.position, self.__drop_off_marker.position)
        distance = info.get("distance")
        duration = info.get("duration")
        drop_off_date_time = (datetime.fromtimestamp(pickup_date_time) + timedelta(hours=duration)).timestamp()
        # calculate the price of the ride
        price = model.calculate_price(distance)
        # pack all the details into a dictionary
        details = dict(
            pickup_time=pickup_date_time,
            drop_off_time=drop_off_date_time,
            pickup_address=pickup_address,
            drop_off_address=drop_off_address,
            distance=distance,
            duration=duration,
            price=price,
            cust_id=self.__user_info.get("user_id")
        )
        # pass the dictionary to the model
        model.set_booking_info(details)
        # make a trip request, save the data to the database
        try:
            model.request_trip()
        except InvalidData as e:
            self.__booking_view.error_msg.config(text=str(e))
            return
        # redirect the user to the trip_details section
        self.trips_view()

    # ---------------------Trips Details--------------------------------------------

    # change view inside trips details section i.e. switch between active bookings and history
    def handle_combo(self, _):
        if self.__trips_view.history_filter.get() == "Active Trips":
            self.__trips_view.scroll.reset_view()
            self.__trips_view.history_table.pack_forget()
            self.__trips_view.active_holder.pack(fill="both", expand=True)
            self.__display_active_trips()
            return
        self.__trips_view.scroll.reset_view()
        self.__trips_view.active_holder.pack_forget()
        self.__trips_view.history_table.pack(fill="both", expand=True)
        self.__display_trips_history()

    def __display_active_trips(self):
        model = CDashboardModel()
        data_list = model.get_active_bookings(self.__user_info.get("user_id"))
        if not data_list:
            return
        self.__trips_view.card.add_cards(data_list)

    def __display_trips_history(self):
        self.__trips_view.history_table.set_columns_width({0: 80, 1: 180})
        self.__trips_view.history_table.set_row_height(50)
        self.__trips_view.history_table.set_heading(["id", "Driver", "Drop Off", "Date", "Status"])
