from utils.hash import hash_match
from utils.database_connector import DatabaseConnector


class LoginModel:
    def __init__(self, creds):
        self.__creds = creds
        self.__cursor = DatabaseConnector().cursor

    # verify the user using the given username and password,
    def __verify(self):
        # first fetch the data from credentials with given username
        query = "select username, user_password, user_role from credentials where username=%s"
        self.__cursor.execute(query, [self.__creds.get("username")])
        creds = self.__cursor.fetchone()
        if not creds:
            return None
        # now match the password with the hashed password in the database
        if not hash_match(self.__creds.get("user_password"), creds[1]):
            return None
        return True

    # returns the details of user if verified else returns None
    def get_user(self):
        if not self.__verify():
            return None
        # fetch all the other information about the user
        query = "select username, user_role from credentials where username=%s"
        self.__cursor.execute(query, [self.__creds.get("username")])
        username, user_role = self.__cursor.fetchone()
        sql = f"select {'cust_id' if user_role=='customer' else 'driver_id' if user_role=='driver' else 'admin_id'}, " \
              f"full_name, gender from {user_role} where username=%s"
        self.__cursor.execute(sql, [username])
        user_id, full_name, gender = self.__cursor.fetchone()
        # return a dictionary with all the user information
        user = dict(
            full_name=full_name,
            gender=gender,
            username=username,
            user_role=user_role,
            user_id=user_id
        )
        return user
