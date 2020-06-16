from flask import session

from exceptions import ServiceError
from models import User


class AuthServiceError(ServiceError):
    service = 'auth'


class UserNotFound(AuthServiceError):
    pass


class IncorrectPassword(AuthServiceError):
    pass


class AuthService:
    def __init__(self, connection):
        self.model = User(connection)

    def get_user_by_id(self, user_id):
        return self.model.get_by_id(user_id)

    def get_auth_user_id(self):
        return session.get('user_id')

    def auth(self, email, password):
        user = self.model.get_by_email(email)
        if user is None:
            raise UserNotFound()

        if not self._check_user_password(user, password):
            raise IncorrectPassword()

        self._auth_user(user)

    @classmethod
    def logout(cls):
        session.pop('user_id', None)

    def _check_user_password(self, user, password):
        return self.model.check_password_hash(user['password'], password)

    @classmethod
    def _auth_user(cls, user):
        session['user_id'] = user['id']
