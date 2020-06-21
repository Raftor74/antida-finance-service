from builders import ServiceBuilder
from services.auth import AuthService


def get_auth_user_id():
    auth_service = ServiceBuilder(AuthService).build()
    return auth_service.get_auth_user_id()
