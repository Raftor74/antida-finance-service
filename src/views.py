from flask.views import MethodView
from builders import ServiceBuilder
from services.auth import AuthService
from services.users import UserService
from services.category import CategoryService


class ServiceView(MethodView):
    service_class = None

    def __init__(self):
        self.service = ServiceBuilder(self.service_class).build()


class AuthServiceView(ServiceView):
    service_class = AuthService


class UserServiceView(ServiceView):
    service_class = UserService


class CategoryServiceView(ServiceView):
    service_class = CategoryService
