from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)


class CategorySchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    parent_id = fields.Integer()


class TransactionSchema(Schema):
    id = fields.Integer(required=True)
    type = fields.Integer(required=True)
    sum = fields.Decimal(as_string=True)
    description = fields.String()
    date_time = fields.DateTime()
    category_id = fields.Integer()
