from views.login import LoginPage
from views.base_window import BaseWindow


class LoginController:
    def __init__(self):
        self.__window = BaseWindow()
        self.__frame = self.__window.frame
        self.login_view = LoginPage(self, self.__frame)
