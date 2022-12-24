from utils.database_connector import DatabaseConnector


class AdminDashboardModel:
    def __init__(self):
        self.__cursor = DatabaseConnector().cursor

    # method to fetch customer name
    def __get_customer_name(self, cust_id):
        self.__cursor.execute("select full_name from customer where cust_id=%s", [cust_id])
        return self.__cursor.fetchone()[0]

    # fetch all pending trips requests
    def get_pending_bookings(self):
        query = "select t.trip_id, c.full_name, t.pickup_address, t.pickup_datetime from trip t inner join " \
                "customer c on t.cust_id = c.cust_id where t.trip_status='pending' "
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    # fetch all the confirmed or unpaid bookings
    def get_confirmed_bookings(self):
        query = "select c.full_name, c.telephone, t.pickup_address, t.pickup_datetime, d.full_name, t.trip_status, " \
                "t.payment_status from customer c inner join trip t on c.cust_id=t.cust_id " \
                "inner join driver d on t.driver_id=d.driver_id where" \
                " t.trip_status='confirmed' or t.payment_status='unpaid'"
        self.__cursor.execute(query)
        return [
            dict(
                customer_name=row[0],
                telephone=row[1],
                pickup_address=row[2],
                pickup_datetime=row[3],
                driver_name=row[4],
                status=f"{row[5], row[6]}"
            ) for row in self.__cursor.fetchall()
        ]

    # fetch all the registered drivers
    def get_all_drivers(self):
        query = "select driver_id, full_name, license_id from driver"
        self.__cursor.execute(query)
        return [
            dict(
                driver_id=row[0],
                driver_name=row[1],
                license_id=row[2]
            ) for row in self.__cursor.fetchall()
        ]

    # fetch the trips history
    def get_trips_history(self):
        query = "select c.full_name, c.pickup_address, c.pickup_datetime, d.full_name, t.trip_status, t.payment_status" \
                " from customer c inner join trip t on c.cust_id = t.cust_id inner join driver d on " \
                "d.driver_id = t.driver_id where (t.trip_status = 'completed' and t.payment_status = 'paid') or " \
                "t.trip_status = 'cancelled'"
        self.__cursor.execute(query)
        return [
            dict(
                customer_name=row[0],
                pickup_address=row[1],
                pickup_datetime=row[2],
                driver_name=row[3],
                status=f"{row[4]}, {row[5]}"
            ) for row in self.__cursor.fetchall()
        ]
