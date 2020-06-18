from marshmallow import Schema, fields, validate, EXCLUDE

# dump_only, load_only (required только для load_only )

class RegisterForm(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Length(5, 100)])


class LoginForm(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class CategoryForm(Schema):
    name = fields.String(required=True)
    parent_id = fields.Integer()


register_form = RegisterForm(unknown=EXCLUDE)
login_form = LoginForm(unknown=EXCLUDE)
# ????? , many=True
category_form = CategoryForm(unknown=EXCLUDE)
