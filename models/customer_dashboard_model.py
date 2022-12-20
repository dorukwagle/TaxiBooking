# from geopy.geocoders import Nominatim
# geo_loc = Nominatim(user_agent="GetLoc")
# address = geo_loc.reverse("27.727494800526653, 85.30451081887394").address

import geocoder
from utils.database_connector import DatabaseConnector


class CDashboardModel:
    def __init__(self):
        self.__driving_speed = 22  # KM/h

    # calculate driving time and distance
    def get_driving_info(self, position1: list, position2: list):
        # calculate the displacement between two coordinates in KM
        distance = geocoder.distance(position1, position2)
        # calculate the driving time
        time = distance / self.__driving_speed
        return dict(
            distance=distance,
            duration=time
        )

    @staticmethod
    def calculate_price(distance):
        base_distance = 2
        base_price = 200
        price = 0
        if distance <= base_distance:
            price = base_price
        elif base_distance < distance < 8:
            price = base_price + (distance - base_distance) * 50
        elif distance <= 20:
            price = base_price + (distance - base_distance) * 80
        elif distance >= 21:
            price = base_price + (distance - base_distance) * 90
        return price
