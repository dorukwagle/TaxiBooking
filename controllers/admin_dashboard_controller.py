from views.admin_dashboard import AdminDashboard


class AdminDashboardController:
    def __init__(self, basewindow):
        self.__window = basewindow
        AdminDashboard(self, self.__window)
