from models.input_model import InputValidation


class CustomerModel(InputValidation):
    def __init__(self, data):
        super().__init__()
        self.__data = data
        self.__telephone_regex = r"^((\d{10})|(\+\d{13}))$"

    def validate(self, data):
        super().validate(data)
