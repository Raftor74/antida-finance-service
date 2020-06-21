from marshmallow import Schema, fields, validate, EXCLUDE, validates, ValidationError
from utils.auth import get_auth_user_id
from utils.validation import (
    ValidationError as CustomValidationError,
    is_category_owner,
    is_valid_transaction_type
)


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
        try:
            user_id = get_auth_user_id()
            is_category_owner(user_id, value)
        except CustomValidationError:
            raise ValidationError("Родительская категория не найдена")


class UpdateCategoryForm(CreateCategoryForm):
    name = fields.String()


class CreateTransactionForm(Schema):
    type = fields.Integer(required=True)
    sum = fields.Float(required=True)
    description = fields.String()
    category_id = fields.Integer()
    date_time = fields.DateTime()

    @validates("category_id")
    def validate_category_id(self, value):
        try:
            user_id = get_auth_user_id()
            is_category_owner(user_id, value)
        except CustomValidationError:
            raise ValidationError("Категория не найдена")

    @validates("type")
    def validate_type(self, value):
        try:
            is_valid_transaction_type(value)
        except CustomValidationError:
            raise ValidationError("Передан не верный тип транзакции")


class UpdateTransactionForm(CreateTransactionForm):
    type = fields.Integer()
    sum = fields.Float()


register_form = RegisterForm(unknown=EXCLUDE)
login_form = LoginForm(unknown=EXCLUDE)
create_category_form = CreateCategoryForm(unknown=EXCLUDE)
update_category_form = UpdateCategoryForm(unknown=EXCLUDE)
create_transaction_form = CreateTransactionForm(unknown=EXCLUDE)
update_transaction_form = UpdateTransactionForm(unknown=EXCLUDE)
