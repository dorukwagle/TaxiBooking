from models.input_model import InputValidation


class DriverRegister(InputValidation):
    def __init__(self, data):
        super().__init__()
        self.__data = data
        self.__license_regex = r"^\d{5,}$"

    def validate(self, data):
        super().validate(data)
