from flask import Blueprint
from flask.views import MethodView

from utils.database import db
from utils.response import json_response
from services.auth import AuthService, UserNotFound, IncorrectPassword
from forms import login_form
from middleware.wraps import validate

bp = Blueprint('auth', __name__)


class BaseView(MethodView):
    def __init__(self):
        self.service = AuthService(db.connection)


class LoginView(BaseView):
    @validate(schema=login_form)
    def post(self, form):
        try:
            self.service.auth(**form)
        except (UserNotFound, IncorrectPassword):
            return json_response.unauthorized()
        else:
            return json_response.success()


class LogoutView(BaseView):
    def post(self):
        self.service.logout()
        return json_response.success()


bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
