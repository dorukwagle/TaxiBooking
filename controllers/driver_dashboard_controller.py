from views.driver_dashboard import DriverDashboard
from models.driver_dashboard_model import DriverDashboardModel


class DriverDashboardController:
    def __init__(self, basewindow, home_page, user):
        self.__home_page = home_page
        self.__window = basewindow
        self.__user = user
        self.__model = DriverDashboardModel()
        self.__view = DriverDashboard(self.__window, self, user)

    def sign_out(self):
        self.__home_page(self.__window)

    def tab_changed(self, notebook):
        # function to mark the booking as completed
        def mark_completed(row_index, table_data):
            ask = self.__view.confirm_message()
            if not ask:
                return
            # mark the trip as completed
            self.__model.mark_completed(table_data.get("Trip Id"))
            # remove the row from the table
            self.__view.upcoming_table.remove_row(row_index)

        index = notebook.index(notebook.select())
        if index == 0:
            data = self.__model.get_upcoming_bookings(self.__user.get("user_id"))
            data = [
                list(row) + [('Completed', mark_completed)] for row in data
            ]
            self.__view.upcoming_table.reset()
            self.__view.upcoming_table.add_rows(data)
        else:
            data = self.__model.get_booking_history(self.__user.get("user_id"))
            self.__view.history_table.reset()
            self.__view.history_table.add_rows(data)
