from views.driver_dashboard import DriverDashboard


class DriverDashboardController:
    def __init__(self, basewindow, home_page, user):
        self.__home_page = home_page
        self.__window = basewindow
        DriverDashboard(self.__window, self, user)
