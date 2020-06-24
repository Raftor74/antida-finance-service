from .base import ModelService
from exceptions import ServiceError
from models import User, IntegrityError


class UserServiceError(ServiceError):
    service = 'user'


class EmailAlreadyExist(UserServiceError):
    pass


class UserService(ModelService):
    model_class = User

    def register(self, attributes: dict):
        try:
            return self._create_user(attributes)
        except IntegrityError as e:
            raise EmailAlreadyExist(str(e)) from e

    def get_user_by_id(self, user_id):
        return self.model.get_by_id(user_id)

    def _generate_user_password(self, password):
        return self.model.generate_password_hash(password)

    def _create_user(self, attributes: dict):
        attributes['password'] = self._generate_user_password(attributes['password'])
        return self.model.create(attributes)
