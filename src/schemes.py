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
