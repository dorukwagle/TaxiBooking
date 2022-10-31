from views.login import LoginPage
from views.base_window import BaseWindow


class LoginController:
    def __init__(self):
        # get the instance of base window as well as its frame
        self.__window = BaseWindow()
        # self.__frame = self.__window.frame

        # instantiate the login view and add it to the base window
        self.login_view = LoginPage(self, self.__window)

