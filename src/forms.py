from marshmallow import Schema, fields, validate, EXCLUDE


class RegisterForm(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True, validate=[validate.Email()])
    password = fields.String(required=True, validate=[validate.Length(5, 100)])


class LoginForm(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


register_form = RegisterForm(unknown=EXCLUDE)
login_form = LoginForm(unknown=EXCLUDE)
