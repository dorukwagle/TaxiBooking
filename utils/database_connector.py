import psycopg2 as db
from psycopg2 import OperationalError
from utils.env_loader import EnvLoader


class DatabaseConnector:
    __connection = None
    __cursor = None

    def __init__(self):
        # load all the database connection details from the environment variable file
        env = EnvLoader("db_config.env", True)  # load from db_config.env file at root directory, 'True' stripes spaces
        self.__user = env.get("username")
        self.__dbname = env.get("database_name")
        self.__password = env.get("password")
        self.__host = env.get("host")
        self.__port = env.get("port")
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

