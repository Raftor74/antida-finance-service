from flask import Blueprint, request
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from utils.database import db

bp = Blueprint('users', __name__)


class UsersView(MethodView):
    def post(self):
        pass


bp.add_url_rule('', view_func=UsersView.as_view('users'))
