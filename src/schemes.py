from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    email = fields.String()
    first_name = fields.String()
    last_name = fields.String()


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    parent_id = fields.Integer()


class TransactionCategorySchema(Schema):
    id = fields.Integer()
    name = fields.String()


class TransactionSchema(Schema):
    id = fields.Integer()
    type = fields.Integer()
    sum = fields.Decimal(as_string=True)
    description = fields.String()
    date_time = fields.DateTime()
    category_id = fields.Integer()
    categories = fields.List(fields.Nested(TransactionCategorySchema))
