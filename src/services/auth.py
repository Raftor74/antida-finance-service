from flask import session

from .base import ModelService
from exceptions import ServiceError
from models import User


class AuthServiceError(ServiceError):
    service = 'auth'


class UserNotFound(AuthServiceError):
    pass


class IncorrectPassword(AuthServiceError):
    pass


class AuthService(ModelService):
    model_class = User

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

    @classmethod
    def get_auth_user_id(cls):
        return session.get('user_id')

    def _check_user_password(self, user, password):
        return self.model.check_password_hash(user['password'], password)

    @classmethod
    def _auth_user(cls, user):
        session['user_id'] = user['id']
