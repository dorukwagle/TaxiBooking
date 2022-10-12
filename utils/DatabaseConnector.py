import psycopg2 as db
from psycopg2 import OperationalError


class DatabaseConnector:
    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self.__user = "doruk"
        self.__dbname = "taxi_booking"
        self.__password = "dorukdb"
        self.__host = "localhost"
        self.__port = "5432"

    @property
    def __connect(self):
        try:
            if self.__connection is None:
                self.__connection = db.connect(database=self.__dbname, user=self.__user, password=self.__password,
                                               host=self.__host, port=self.__port)
                self.__connection.autocommit = True
            return self.__connection
        except OperationalError as e:
            raise e

    @property
    def cursor(self):
        try:
            if self.__cursor is None:
                conn = self.__connect
                self.__cursor = conn.cursor()
            return self.__cursor
        except OperationalError as e:
            raise e

    def close(self):
        self.cursor.close()
        self.__connect.close()
