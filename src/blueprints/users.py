from flask import Blueprint

from forms import register_form
from middleware.wraps import validate
from services.users import UserService, EmailAlreadyExist
from utils.response import json_response
from views import ServiceView

bp = Blueprint('users', __name__)


class UserServiceView(ServiceView):
    service_class = UserService


class UsersView(UserServiceView):

    @validate(schema=register_form)
    def post(self, form):
        try:
            user_id = self.service.register(form)
            user = self.service.get_user_by_id(user_id)
            response = self.service.to_response(user)
        except EmailAlreadyExist:
            return json_response.conflict()
        else:
            return json_response.success(response)


bp.add_url_rule('', view_func=UsersView.as_view('users'))
