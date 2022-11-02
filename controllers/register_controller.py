from views.register import RegistrationPage
from views.base_window import BaseWindow


class RegistrationController:
    def __init__(self):
        # get the instance of base window
        self.__window = BaseWindow()
        # instantiate Registration view
        self.registration_view = RegistrationPage(self, self.__window)