from views.login import LoginPage
from views.register import RegistrationPage, CustomerRegistration


class LoginController:
    def __init__(self, basewindow):
        # get the instance of base window as well as its frame
        self.__window = basewindow
        # self.__frame = self.__window.frame
        # instantiate the login view and add it to the base window
        self.login_view = LoginPage(self, self.__window)

    def open_register(self):
        RegistrationController(self.__window)


class RegistrationController:
    def __init__(self, basewindow):
        # instantiate base class
        # get the instance of base window
        self.__window = basewindow
        # instantiate Registration view
        self.registration_view = RegistrationPage(self, self.__window)
        # self.registration_view = LoginPageReg(self, self.__window)

    def open_login(self):
        LoginController(self.__window)
