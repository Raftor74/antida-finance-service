from functools import wraps
from flask import request
from marshmallow.validate import ValidationError

from builders import ServiceBuilder
from services.auth import AuthService
from services.users import UserService
from utils.response import json_response


def validate(schema):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            json = request.get_json()
            try:
                form = schema.load(json)
            except ValidationError as e:
                return json_response.bad_request(e.messages)
            return view_func(*args, **kwargs, form=form)

        return wrapper

    return decorator


def auth_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        auth_service = ServiceBuilder(AuthService).build()
        user_service = ServiceBuilder(UserService).build()
        user_id = auth_service.get_auth_user_id()
        if user_id is None:
            return json_response.unauthorized()
        user = user_service.get_user_by_id(user_id)
        if user is None:
            return json_response.unauthorized()
        return view_func(*args, **kwargs, user=user)

    return wrapper
