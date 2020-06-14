from functools import wraps
from flask import request
from marshmallow.validate import ValidationError

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
