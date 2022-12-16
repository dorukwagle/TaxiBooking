from views.driver_dashboard import DriverDashboard


class DriverDashboardController:
    def __init__(self, basewindow):
        self.__window = basewindow
        DriverDashboard(self.__window, self)
