from views.register import RegistrationPage
from views.base_window import BaseWindow


class RegistrationController:
    def __init__(self, basewindow):
        # get the instance of base window
        self.__window = basewindow
        # instantiate Registration view
        self.registration_view = RegistrationPage(self, self.__window)
        # self.registration_view = LoginPageReg(self, self.__window)
