import psycopg2 as db
from psycopg2 import OperationalError


class Connection:
    __conn = None
    __cur = None

    def __init__(self):
        # load all the database connection details from the environment variable file
        self.__dbuser = "username"
        self.__dbname = "database_name"
        self.__password = "password"
        self.__host = "localhost"
        self.__port = "5432"
        # connect to database
        self.__connect()
        self.__dbcur = Connection.__cur
        self.__dbconn = Connection.__conn

    def __connect(self):
        try:
            if Connection.__conn is None:
                Connection.__conn = db.connect(database=self.__dbname, user=self.__dbuser,
                                                            password=self.__password,
                                                            host=self.__host, port=self.__port)
                Connection.__conn.autocommit = True
                Connection.__cur = Connection.__conn.cursor()
        except OperationalError as e:
            raise e

    @property
    def cursor(self):
        return self.__dbcur

    def close(self):
        self.__dbconn.close()

