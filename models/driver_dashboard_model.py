from utils.database_connector import DatabaseConnector


class DriverDashboardModel:
    def __init__(self):
        self.__cursor = DatabaseConnector().cursor

    def get_upcoming_bookings(self, driver_id):
        query = "select trip_id, pickup_address, drop_off_address, pickup_datetime from trip where driver_id=%s"
        self.__cursor.execute(query, [driver_id])
        return self.__cursor.fetchall()

    def get_booking_history(self, driver_id):
        # function to fetch customer name
        def get_customer_name(customer_id):
            sql = "select full_name from customer where cust_id=%s"
            self.__cursor.execute(sql, [customer_id])
            return self.__cursor.fetchone()[0]

        query = "select cust_id, pickup_address, pickup_datetime, trip_status, payment_status from trip " \
                "where driver_id=%s and (trip_status='completed' or trip_status='cancelled' )"
        self.__cursor.execute(query, [driver_id])
        return [
            [get_customer_name(row[0])] + list(row)[1:-2] + [f"{row[-2]}, {row[-1]}"]
            for row in self.__cursor.fetchall()
        ]

    def mark_completed(self, trip_id):
        query = "update trip set trip_status='completed' where trip_id=%s"
        self.__cursor.execute(query, [trip_id])
