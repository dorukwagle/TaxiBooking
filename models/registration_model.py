import re
from utils.database_connector import DatabaseConnector
import utils.hash as hs


class InputException(BaseException):
    pass


class RegistrationModel:
    def __init__(self, data):
        self.__data = data
        self.__name_regex = r"^[a-zA-Z]+([ ][a-zA-Z]+){1,2}$"
        self.__address_regex = r"^[\w\s,\d]+$"
        self.__email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.__username_regex = r"([a-zA-Z]{4,}(\d+)?)$"
        self.__password_regex = r"^.{6,}"
        self.__telephone_regex = r"^((\d{10})|(\+\d{13}))$"
        self.__license_regex = r"^\d{5,}$"
        # initialize database connection
        db = DatabaseConnector()
        self.__cursor = db.cursor

    def __validate(self):
        # extract the data from dictionary object
        name = self.__data.get("full_name")
        user = self.__data.get("username")
        pw = self.__data.get("user_password")
        # now match each datum to the
        if not re.fullmatch(self.__name_regex, name):
            raise InputException("Invalid Full Name")
        if not re.fullmatch(self.__username_regex, user):
            raise InputException("Invalid username")
        if not re.fullmatch(self.__password_regex, pw):
            raise InputException("Invalid password length")

    def validate_customer(self):
        self.__validate()
        email = self.__data.get("email")
        telephone = self.__data.get("telephone")
        address = self.__data.get("address")
        if not re.fullmatch(self.__telephone_regex, telephone):
            raise InputException("Invalid telephone number")
        if not re.fullmatch(self.__email_regex, email):
            raise InputException("Invalid email address")
        if not re.fullmatch(self.__address_regex, address):
            raise InputException("Invalid Address")

    def validate_driver(self):
        self.__validate()
        if not re.fullmatch(self.__license_regex, self.__data.get("license_id")):
            raise InputException("Invalid license id")

    def email_exists(self):
        query = "select * from customer where email=%s;"
        self.__cursor.execute(query, [self.__data.get("email")])
        if not self.__cursor.fetchone():
            return False
        return True

    def user_exists(self):
        query = "select * from credentials where username=%s;"
        self.__cursor.execute(query, [self.__data.get("username")])
        if not self.__cursor.fetchone():
            return False
        return True

    def register_customer(self):
        # hash the password before storing to the database
        hashed_pass = hs.hashed(self.__data.get("user_password"))
        query1 = "insert into customer(full_name, gender, email, address, telephone, payment_method, username) "\
                 "values(%s, %s, %s, %s, %s, %s, %s)"
        query2 = "insert into credentials(username, user_password, user_role) values(%s, %s, 'customer')"
        self.__cursor.execute(query1, (
            self.__data.get("full_name"),
            self.__data.get("gender"),
            self.__data.get("email"),
            self.__data.get("address"),
            self.__data.get("telephone"),
            self.__data.get("payment_method"),
            self.__data.get("username")
        ))
        self.__cursor.execute(query2, (
            self.__data.get("username"),
            hashed_pass
        ))

    def register_driver(self):
        hashed_pass = hs.hashed(self.__data.get("user_password"))
        query1 = "insert into driver(full_name, gender, lincese_id, username) values(%s, %s, %s, %s)"
        query2 = "insert into credentials(username, user_password, user_role) values(%s, %s, 'driver')"
        self.__cursor.execute(query1, (
            self.__data.get("full_name"),
            self.__data.get("gender"),
            self.__data.get("license_id"),
            self.__data.get("username")
        ))
        self.__cursor.execute(query2, (
            self.__data.get("username"),
            hashed_pass
        ))


