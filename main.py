from controllers.reg_log_controller import LoginController
from controllers.customer_dashboard_controller import CDashboardController
from controllers.admin_dashboard_controller import AdminDashboardController
from controllers.driver_dashboard_controller import DriverDashboardController
from views.base_window import BaseWindow


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # instantiate BaseWindow and pass it to the controller object
    basewindow = BaseWindow()
    LoginController(basewindow)
    # CDashboardController(basewindow)
    # AdminDashboardController(basewindow)
    # DriverDashboardController(basewindow)
    basewindow.mainloop()
