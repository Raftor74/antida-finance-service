from marshmallow import Schema, fields, validate, EXCLUDE, validates, ValidationError
from builders import ServiceBuilder
from services.auth import AuthService
from services.category import CategoryService, CategoryNotFound


class RegisterForm(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Length(5, 100)])


class LoginForm(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class CreateCategoryForm(Schema):
    name = fields.String(required=True)
    parent_id = fields.Integer()

    @validates("parent_id")
    def validate_parent_id(self, value):
        auth_service = ServiceBuilder(AuthService).build()
        category_service = ServiceBuilder(CategoryService).build()
        user_id = auth_service.get_auth_user_id()
        try:
            category_service.get_user_category_by_id(user_id, value)
        except CategoryNotFound:
            raise ValidationError("Родительская категория не найдена")


class UpdateCategoryForm(CreateCategoryForm):
    name = fields.String()


register_form = RegisterForm(unknown=EXCLUDE)
login_form = LoginForm(unknown=EXCLUDE)
create_category_form = CreateCategoryForm(unknown=EXCLUDE)
update_category_form = UpdateCategoryForm(unknown=EXCLUDE)
