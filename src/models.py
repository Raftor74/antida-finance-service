import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash


class IntegrityError(Exception):
    pass


class BaseModel:
    pk_name = "id"
    table = None

    def __init__(self, connection):
        self.connection = connection

    def get_by_field(self, field_name, value):
        query = f"""
            SELECT *
            FROM {self.table} 
            WHERE {field_name} = ?
        """
        result = self.connection.execute(query, (value,)).fetchone()
        return dict(result) if result is not None else None

    def find_one(self, fields: dict):
        result = self._find(fields).fetchone()
        return dict(result) if result is not None else None

    def find_many(self, fields: dict):
        result = self._find(fields).fetchall()
        return [dict(row) for row in result]

    def get_by_id(self, id):
        return self.get_by_field(self.pk_name, id)

    def create(self, attributes: dict, on_conflict: str = ''):
        keys = attributes.keys()
        values = attributes.values()
        placeholder = ', '.join('?' for _ in values)
        fields_str = ', '.join(keys)
        query = f"""
            INSERT {on_conflict} INTO {self.table} ({fields_str})
            VALUES ({placeholder})
        """
        try:
            cursor = self.connection.execute(query, tuple(values))
            self.connection.commit()
            return cursor.lastrowid

        except sqlite3.IntegrityError as e:
            raise IntegrityError(str(e)) from e

    def _find(self, fields: dict):
        keys = fields.keys()
        placeholders = [f"{key} = ?" for key in keys]
        placeholder = " AND ".join(placeholders)

        query = f"""
             SELECT *
             FROM {self.table}
             WHERE {placeholder}
         """
        return self.connection.execute(query, tuple(fields.values()))


class User(BaseModel):
    table = 'account'

    def get_by_email(self, email):
        return self.get_by_field('email', email)

    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password_hash(password_hash, password):
        return check_password_hash(password_hash, password)


class Category(BaseModel):
    table = 'category'

    def create(self, attributes: dict, on_conflict: str = 'OR IGNORE'):
        return super().create(attributes, on_conflict)

    def get_user_category_by_name(self, user_id, name):
        fields = {'name': name, 'account_id': user_id}
        return self.find_one(fields)

    def get_user_category_by_id(self, user_id, id):
        fields = {'id': id, 'account_id': user_id}
        return self.find_one(fields)

    def get_categories_by_user(self, user_id):
        return self.find_many({'account_id': user_id})
