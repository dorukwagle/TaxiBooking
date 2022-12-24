from views.admin_dashboard import AdminDashboard
from models.registration_model import RegistrationModel, InputException


class AdminDashboardController:
    def __init__(self, basewindow, home_page, user):
        self.__home_page = home_page
        self.__window = basewindow
        self.__view = AdminDashboard(self.__window, self, user)

    def logout(self):
        self.__home_page(self.__window)

    # disable search bar and button when registration tab is open
    def tab_changed(self, notebook):
        tab_index = notebook.index(notebook.select())
        if tab_index == 3:
            self.__view.search_bar.config(state='disabled')
            self.__view.search_btn.config(state='disabled')
            return
        if str(self.__view.search_bar['state']) == 'disabled':
            self.__view.search_bar.config(state='normal')
            self.__view.search_btn.config(state='normal')

    def register_driver(self):
        DriverRegistration(self.__view.register_v).sign_up()


# -----------------------Driver Registration---------------------
class DriverRegistration:
    def __init__(self, view):
        self.__view = view

    # get all the user input from the views
    def __fetch_info(self):
        full_name = self.__view.full_name.get().strip()
        address = self.__view.address.get().strip()
        license_id = self.__view.license_id.get().strip()
        username = self.__view.username.get().strip()
        password = self.__view.password.get().strip()
        confirm_pass = self.__view.confirm_password.get().strip()
        gender = self.__view.gender.get().strip().lower() if self.__view.gender.current() > -1 else ""

        # check if any field is empty
        if not all([full_name, address, license_id, username, password, gender]):
            self.__view.error_msg.config(text="Please fill all the fields")
            return None
        if password != confirm_pass:
            self.__view.error_msg.config(text="Passwords do not match")
            return None

        # pack all the data into a dictionary
        info = dict(
            full_name=full_name,
            address=address,
            license_id=license_id,
            username=username,
            user_password=password,
            gender=gender
        )
        return info

    def __validate_info(self, info):
        self.__reg_model = RegistrationModel(info)
        # first validate the given data
        try:
            self.__reg_model.validate_driver()
        except InputException as e:
            self.__view.error_msg.config(text=str(e))
            return False

        # check if username already exists in the database
        if self.__reg_model.user_exists():
            self.__view.error_msg.config(text="Username already exists")
            return False
        return True

    def sign_up(self):
        # get the data
        info = self.__fetch_info()
        if not info:
            return
        # check if the data is valid and ready for registration
        if not self.__validate_info(info):
            return
        self.__reg_model.register_driver()
        # show successful message
        self.__view.successful()
        # clear all the input fields
        self.__view.full_name.set_text("")
        self.__view.address.set_text("")
        self.__view.license_id.set_text("")
        self.__view.username.set_text("")
        self.__view.password.set_text("")
        self.__view.confirm_password.set_text("")
