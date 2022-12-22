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
        # local function to obtain the driver name
        def get_driver_name(cursor, driver_id):
            sql = "select full_name from driver where driver_id=%s"
            cursor.execute(sql, [int(driver_id)])
            return cursor.fetchone()[0]

        # local function for converting hours to hours and minutes
        def hours_minutes(hours):
            hours = float(hours)
            hour = int(hours)
            minute = hours * 60 - hour * 60
            return f'{hour} Hr, {minute} Min'

        # query all the bookings with status: not cancelled and payment status unpaid
        query = """select * from (select * from trip where cust_id=%s and trip_status!='cancelled') as t 
        where payment_status='unpaid'"""
        self.__cursor.execute(query, [cust_id])
        details = self.__cursor.fetchall()
        trip_infos = []
        for row in details:
            # fetch the pickup and drop off time and convert to datetime
            row_dict = dict(
                trip_id=row[0],
                pickup_address=row[1].replace("\n", " "),
                drop_off_address=row[2].replace("\n", " "),
                pickup_datetime=row[3],  # convert timestamp to date and time
                distance=f'{row[4]} KM',
                duration=hours_minutes(row[5]),
                price=row[6],
                drop_off_datetime=row[7],  # convert timestamp to date and time
                status=f'{row[8]}, {row[9]}',
                driver_name=get_driver_name(self.__cursor, row[10]) if row[10] else '<<Not Assigned>>'
            )
            trip_infos.append(row_dict)
        return trip_infos

    def get_trips_history(self, cust_id):
        # local function to obtain the driver name
        def get_driver_name(cursor, driver_id):
            sql = "select full_name from driver where driver_id=%s"
            cursor.execute(sql, [int(driver_id)])
            return cursor.fetchone()[0]

        # id, driver, drop off, date, status
        query = "select trip_id, driver_id, drop_off_address, pickup_datetime, trip_status" \
                " from trip where cust_id=%s and trip_id not in " \
                "(select trip_id from (select trip_id from trip where cust_id=%s and trip_status!='cancelled') as t "\
                "where payment_status='unpaid'"
        self.__cursor.execute(query, [cust_id, cust_id])
        details = []
        for row in self.__cursor.fetchall():
            row_dict = dict(
                trip_id=row[0],
                driver_id=get_driver_name(self.__cursor, row[1]) if row[1] else '<<Not Assigned>>',
                drop_off_address=row[2],
                pickup_datetime=row[3],
                trip_status=row[4]
            )
            details.append(row_dict)
        return details
