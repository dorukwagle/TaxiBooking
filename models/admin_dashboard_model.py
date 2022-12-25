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
            [
                row[0],  # customer full name
                row[1],  # customer telephone
                row[2],  # pickup_address
                row[3],  # pickup date and time
                row[4],  # driver full name
                f"{row[5], row[6]}"  # trip and payment status
            ] for row in self.__cursor.fetchall()
        ]

    # fetch all the registered drivers
    def get_all_drivers(self):
        query = "select driver_id, full_name, license_id from driver"
        self.__cursor.execute(query)
        return [
            [
                row[0],  # driver id
                row[1],  # driver full name
                row[2]   # driver license id
            ] for row in self.__cursor.fetchall()
        ]

    # fetch the trips history
    def get_trips_history(self):
        query = "select c.full_name, t.pickup_address, t.pickup_datetime, d.full_name, t.trip_status, t.payment_status" \
                " from customer c inner join trip t on c.cust_id = t.cust_id inner join driver d on " \
                "d.driver_id = t.driver_id where (t.trip_status = 'completed' and t.payment_status = 'paid') or " \
                "t.trip_status = 'cancelled'"
        self.__cursor.execute(query)
        return [
            [
                row[0],  # customer full name
                row[1],  # pickup address
                row[2],  # pickup date and time
                row[3],  # driver full name
                f"{row[4]}, {row[5]}"  # trip and payment status
            ] for row in self.__cursor.fetchall()
        ]
