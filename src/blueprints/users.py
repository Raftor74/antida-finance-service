from flask import Blueprint
from flask.views import MethodView

from utils.database import db
from utils.response import json_response
from services.users import UserService, EmailAlreadyExist
from middleware.wraps import validate
from forms import register_form

bp = Blueprint('users', __name__)


class BaseView(MethodView):
    def __init__(self):
        self.service = UserService(db.connection)


class UsersView(BaseView):
    @validate(schema=register_form)
    def post(self, form):
        try:
            user_id = self.service.register(form)
            user = self.service.get_user(user_id)
            user.pop('password')
        except EmailAlreadyExist:
            return json_response.conflict()
        else:
            return json_response.success(user)


bp.add_url_rule('', view_func=UsersView.as_view('users'))
