from views.login import LoginPage
from views.register import RegistrationPage, CustomerRegistration
from models.registration_model import RegistrationModel, InputException
from models.login_model import LoginModel
from controllers.customer_dashboard_controller import CDashboardController
from controllers.admin_dashboard_controller import AdminDashboardController
from controllers.driver_dashboard_controller import DriverDashboardController


class LoginController:
    def __init__(self, basewindow):
        # get the instance of base window as well as its frame
        self.__window = basewindow
        # instantiate the login view and add it to the base window
        self.__view = LoginPage(self.__window, self)

    def open_register(self):
        RegistrationController(self.__window)

    def login(self):
        # fetch user credentials from the input fields
        username = self.__view.username.get().strip()
        password = self.__view.password.get()
        log_model = LoginModel(dict(
            username=username,
            user_password=password
        ))
        user = log_model.get_user()
        # check if credentials are verified
        if not user:
            self.__view.error_msg.config(text="Invalid username or password")
            return
        # check the user role and redirect to the corresponding dashboard
        role = user.get("user_role")
        if role == "customer":
            CDashboardController(self.__window, home_page=LoginController, user=user)
        elif role == "admin":
            AdminDashboardController(self.__window, home_page=LoginController, user=user)
        else:
            DriverDashboardController(self.__window, home_page=LoginController, user=user)


class RegistrationController:
    def __init__(self, basewindow):
        # instantiate base class
        # get the instance of base window
        self.__window = basewindow
        # instantiate Registration view
        self.__frame = RegistrationPage(self.__window, self).base_frame
        self.__view = CustomerRegistration(self.__frame, self)
        self.__view.pack()
        self.__reg_model = None
        # self.registration_view = LoginPageReg(self, self.__window)

    def open_login(self):
        LoginController(self.__window)

        # fetch all the inputs from the input fields

    def __fetch_all(self):
        full_name = self.__view.full_name.get().strip()
        email = self.__view.email_address.get().strip()
        address = self.__view.address.get().strip()
        telephone = self.__view.telephone.get().strip()
        username = self.__view.username.get().strip()
        password = self.__view.password.get()
        confirm_pass = self.__view.confirm_password.get().strip()
        gender = self.__view.gender.get().strip().lower() if self.__view.gender.current() > -1 else ""
        payment_method = self.__view.payment_method.get().strip() if self.__view.payment_method.current() > -1 else ""

        # check if any field is empty
        if not all([full_name, email, address, telephone, username, password, gender, payment_method]):
            self.__view.error_msg.config(text="Please fill all the fields")
            return None
        if password != confirm_pass:
            self.__view.error_msg.config(text="Passwords do not match")
            return None

        # pack all the data into a dictionary
        data = dict(
            full_name=full_name,
            email=email,
            address=address,
            telephone=telephone,
            username=username,
            user_password=password,
            gender=gender,
            payment_method=payment_method
        )
        return data

    # validate the user input and also check if the username or email already exists
    def __validate(self, data):
        self.__reg_model = RegistrationModel(data)
        # first validate the given data
        try:
            self.__reg_model.validate_customer()
        except InputException as e:
            self.__view.error_msg.config(text=str(e))
            return False

        # check if email or username already exists in the database
        if self.__reg_model.email_exists():
            self.__view.error_msg.config(text="Email already exists")
            return False
        if self.__reg_model.user_exists():
            self.__view.error_msg.config(text="Username already exists")
            return False
        return True

    def sign_up(self):
        # get the data
        data = self.__fetch_all()
        if not data:
            return
        # check if the data is valid and ready for registration
        if not self.__validate(data):
            return
        self.__reg_model.register_customer()
        # call the login model and get the user information
        log_model = LoginModel(dict(
            username=data.get("username"),
            user_password=data.get("user_password")
        ))
        user = log_model.get_user()
        # since, it is customer who is registered, open the customer dashboard
        CDashboardController(self.__window, home_page=LoginController, user=user)
