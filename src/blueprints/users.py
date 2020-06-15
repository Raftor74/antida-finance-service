from flask import Blueprint

from forms import register_form
from middleware.wraps import validate
from services.users import EmailAlreadyExist
from utils.response import json_response
from views import UserServiceView

bp = Blueprint('users', __name__)


class UsersView(UserServiceView):

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
