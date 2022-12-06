import psycopg2 as db
from psycopg2 import OperationalError


class DatabaseConnector:
    __connection = None

    def __init__(self):
        self.__user = "doruk"
        self.__dbname = "taxi_booking"
        self.__password = "dorukdb"
        self.__host = "localhost"
        self.__port = "5432"

    @property
    def __connect(self):
        try:
            if DatabaseConnector.__connection is None:
                DatabaseConnector.__connection = db.connect(database=self.__dbname, user=self.__user,
                                                            password=self.__password,
                                                            host=self.__host, port=self.__port)
                DatabaseConnector.__connection.autocommit = True
            return DatabaseConnector.__connection
        except OperationalError as e:
            raise e

    @property
    def cursor(self):
        return DatabaseConnector.__connection.cursor()

    def close(self):
        self.__connect.close()
