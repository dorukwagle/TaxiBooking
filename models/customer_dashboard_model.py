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
        return int(price)

    def request_trip(self):
        if not self.__info:
            return
        # validate time before saving the request
        if datetime.now().timestamp() > datetime.fromtimestamp(float(self.__info.get("pickup_time"))).timestamp():
            raise InvalidData("choose upcoming time, can't pick you from past!!")
        query = """insert into trip(pickup_address, drop_off_address, pickup_datetime, distance, duration, price, 
                drop_off_datetime, trip_status, payment_status, cust_id) values(%s, %s, to_timestamp(%s), %s, %s, %s, 
                to_timestamp(%s), %s, %s, %s)"""
        self.__cursor.execute(query, [
            self.__info.get("pickup_address"),
            self.__info.get("drop_off_address"),
            self.__info.get("pickup_time"),
            self.__info.get("distance"),
            self.__info.get("duration"),
            self.__info.get("price"),
            self.__info.get("drop_off_time"),
            "pending",
            "unpaid",
            self.__info.get("cust_id")
        ])

    def get_active_bookings(self, cust_id):
        # local function for converting hours to hours and minutes
        def hours_minutes(hours):
            hours = float(hours)
            hour = int(hours)
            minute = hours * 60 - hour * 60
            return f"{hour} Hr, {'%.3f' % float(minute)} Min"

        # query all the bookings with status: not cancelled and payment status unpaid
        query = """select * from (select * from trip where cust_id=%s and trip_status!='cancelled') as t 
        where trip_status != 'completed' or payment_status != 'paid'"""
        self.__cursor.execute(query, [cust_id])
        return [
            # fetch the pickup and drop off time and convert to datetime
            dict(
                trip_id=row[0],
                pickup_address=row[1].replace("\n", " "),
                drop_off_address=row[2].replace("\n", " "),
                pickup_datetime=row[3],  # convert timestamp to date and time
                distance=f'{row[4]} KM',
                duration=hours_minutes(row[5]),
                price=row[6],
                drop_off_datetime=row[7],  # convert timestamp to date and time
                status=f'{row[8]}, {row[9]}',
                driver_name=self.__get_driver_name(row[10])
            ) for row in self.__cursor.fetchall()
        ]

    # method to get driver name
    def __get_driver_name(self, driver_id):
        if not driver_id:
            return "<<Not Assigned>>"
        sql = "select full_name from driver where driver_id=%s"
        self.__cursor.execute(sql, [int(driver_id)])
        return self.__cursor.fetchone()[0]

    def get_trips_history(self, cust_id):
        # id, driver, drop off, date, status
        query = "select trip_id, driver_id, drop_off_address, pickup_datetime, trip_status" \
                " from trip where cust_id=%s and trip_id not in " \
                "(select trip_id from (select trip_id from trip where cust_id=%s and trip_status!='cancelled') as t "\
                "where trip_status != 'completed' or payment_status != 'paid');"
        self.__cursor.execute(query, [cust_id, cust_id])
        details = list(self.__cursor.fetchall())
        for ind, row in enumerate(details):
            # convert whole row from tuple to list
            details[ind] = list(row)
            details[ind][1] = self.__get_driver_name(row[1])
        return details

    def cancel_booking(self, trip_id):
        query = "update trip set trip_status='cancelled' where trip_id=%s"
        self.__cursor.execute(query, [trip_id])

    def complete_payment(self, trip_id):
        query = "update trip set payment_status='paid' where trip_id=%s"
        self.__cursor.execute(query, [trip_id])

    def complete_trip(self, trip_id):
        query = "update trip set trip_status='completed' where trip_id=%s"
        self.__cursor.execute(query, [trip_id])

    # returns a single trip information
    def get_trip(self, trip_id):
        # local function for converting hours to hours and minutes
        def hours_minutes(hours):
            hours = float(hours)
            hour = int(hours)
            minute = hours * 60 - hour * 60
            return f"{hour} Hr, {'%.3f' % float(minute)} Min"
        # pickup_time, From, To, Driver_name, price, duration, distance
        query = "select pickup_datetime, pickup_address, drop_off_address, driver_id, price, duration, distance," \
                " trip_id, trip_status, payment_status  from trip where trip_id=%s"
        self.__cursor.execute(query, [trip_id])
        result = self.__cursor.fetchone()
        return dict(
            pickup_time=result[0],
            pickup_address=result[1],
            drop_off_address=result[2],
            driver_name=self.__get_driver_name(result[3]),
            price='%.3f' % float(result[4]),
            duration=hours_minutes(result[5]),
            distance=f"{'%.3f' % float(result[6])} KM",
            trip_id=result[7],
            trip_status=result[8],
            payment_status=result[9]
        )
