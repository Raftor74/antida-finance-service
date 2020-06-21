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


class TransactionSchema(Schema):
    id = fields.Integer()
    type = fields.Integer()
    sum = fields.Float()
    description = fields.String()
    date_time = fields.String()
    category_id = fields.Integer()
