import geocoder
from utils.database_connector import DatabaseConnector
from datetime import datetime


class InvalidData(BaseException):
    pass


class CDashboardModel:
    def __init__(self):
        self.__info = None
        self.__driving_speed = 20  # KM/h
        self.__cursor = DatabaseConnector().cursor

    def set_booking_info(self, booking_info: dict):
        self.__info = booking_info

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

    def request_trip(self):
        if not self.__info:
            return
        # validate time before saving the request
        if datetime.now().timestamp() > datetime.fromtimestamp(float(self.__info.get("pickup_time"))).timestamp():
            raise InvalidData("choose upcoming time, can't pick you from past!!")
        query = """insert into trip(pickup_address, drop_off_address, pickup_datetime, distance, duration, price, 
                drop_off_datetime, trip_status, payment_status, cust_id) values(%s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s)"""
        self.__cursor.execute(query, [
            self.__info.get("pickup_address"),
            self.__info.get("drop_off_address"),
            self.__info.get("pickup_datetime"),
            self.__info.get("distance"),
            self.__info.get("duration"),
            self.__info.get("price"),
            self.__info.get("drop_off_datetime"),
            "pending",
            "unpaid",
            self.__info.get("cust_id")
        ])

    def get_active_bookings(self):
        # query all the bookings with status: confirmed and pending or payment status unpaid
        # fetch the pickup and drop off time and convert to datetime
        # return status and payment status as status, payment status e.g. confirmed, unpaid
        pass
