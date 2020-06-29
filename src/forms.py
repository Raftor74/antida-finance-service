from marshmallow import Schema, fields, validate, EXCLUDE


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
    parent_id = fields.Integer(allow_none=True)


class UpdateCategoryForm(CreateCategoryForm):
    name = fields.String()


class CreateTransactionForm(Schema):
    type = fields.Integer(required=True)
    sum = fields.Float(required=True)
    description = fields.String()
    category_id = fields.Integer(allow_none=True)
    date_time = fields.DateTime()


class UpdateTransactionForm(CreateTransactionForm):
    type = fields.Integer()
    sum = fields.Float()


class FilterTransactionForm(Schema):
    limit = fields.Integer()
    offset = fields.Integer()
    category = fields.Integer()
    datetime = fields.String()
    datetime_from = fields.DateTime()
    datetime_to = fields.DateTime()


register_form = RegisterForm(unknown=EXCLUDE)
login_form = LoginForm(unknown=EXCLUDE)
create_category_form = CreateCategoryForm(unknown=EXCLUDE)
update_category_form = UpdateCategoryForm(unknown=EXCLUDE)
create_transaction_form = CreateTransactionForm(unknown=EXCLUDE)
update_transaction_form = UpdateTransactionForm(unknown=EXCLUDE)
filter_transaction_form = FilterTransactionForm(unknown=EXCLUDE)
