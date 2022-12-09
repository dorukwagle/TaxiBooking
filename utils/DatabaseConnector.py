import psycopg2 as db
from psycopg2 import OperationalError


class DatabaseConnector:
    __connection = None
    __cursor = None

    def __init__(self):
        self.__user = "doruk"
        self.__dbname = "taxi_booking"
        self.__password = "dorukdb"
        self.__host = "localhost"
        self.__port = "5432"
        # connect to database
        self.__connect()
        self.__dbconnection = DatabaseConnector.__connection
        self.__dbcursor = DatabaseConnector.__cursor

    def __connect(self):
        try:
            if DatabaseConnector.__connection is None:
                DatabaseConnector.__connection = db.connect(database=self.__dbname, user=self.__user,
                                                            password=self.__password,
                                                            host=self.__host, port=self.__port)
                DatabaseConnector.__connection.autocommit = True
                DatabaseConnector.__cursor = DatabaseConnector.__connection.cursor()
        except OperationalError as e:
            raise e

    @property
    def cursor(self):
        return self.__dbcursor

    def close(self):
        self.__dbconnection.close()

