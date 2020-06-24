from flask import Blueprint

from forms import login_form
from middleware.wraps import validate
from services.auth import AuthService, UserNotFound, IncorrectPassword
from utils.response import json_response
from views import ServiceView

bp = Blueprint('auth', __name__)


class AuthServiceView(ServiceView):
    service_class = AuthService


class LoginView(AuthServiceView):

    @validate(schema=login_form)
    def post(self, form):
        try:
            self.service.auth(**form)
        except (UserNotFound, IncorrectPassword):
            return json_response.unauthorized()
        else:
            return json_response.success()


class LogoutView(AuthServiceView):

    def post(self):
        self.service.logout()
        return json_response.success()


bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
