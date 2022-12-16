

class InputValidation:
    def __init__(self):
        self.__name_regex = r"^[a-zA-Z]+([ ][a-zA-Z]+){1,2}$"
        self.__address_regex = r"^[\w\s,\d]+$"
        self.__email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        self.__username_regex = r"\w"
        self.__password_regex = r"^.{6,}$"

    def validate(self, data):
        pass