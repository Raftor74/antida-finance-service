from .base import ModelService, SchemaService
from exceptions import ServiceError
from models import User, IntegrityError
from schemes import UserSchema


class UserServiceError(ServiceError):
    service = 'user'


class EmailAlreadyExist(UserServiceError):
    pass


class UserService(ModelService, SchemaService):
    model_class = User
    schema_class = UserSchema

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
