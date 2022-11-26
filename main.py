from controllers.login_controller import LoginController
from controllers.register_controller import RegistrationController
from controllers.CustomerDashboardController import CDashboardController
from views.base_window import BaseWindow


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # instantiate BaseWindow and pass it to the controller object
    base_window = BaseWindow()
    # LoginController(base_window)
    # RegistrationController(base_window)
    CDashboardController(base_window)
    base_window.mainloop()
