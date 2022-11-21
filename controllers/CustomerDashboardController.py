from views.customer_dashboard import CustomerDashboard
from views.base_window import BaseWindow


class CDashboardController:

    def __init__(self, base_window, username=""):
        # get instance of the base window
        self.__window = base_window
        # self.frame = self.__window.frame

        # retrieve the user information from database
        user_info = dict()  # query database and store the result
        # instantiate Dashboard view
        self.customer_dashboard = CustomerDashboard(self, self.__window, user_info)
