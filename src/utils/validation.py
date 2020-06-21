from builders import ServiceBuilder
from services.category import CategoryService, CategoryNotFound
from services.transaction import TransactionService


class ValidationError(Exception):
    pass


def is_category_owner(user_id, category_id):
    category_service = ServiceBuilder(CategoryService).build()
    try:
        return category_service.get_user_category_by_id(user_id, category_id)
    except CategoryNotFound:
        raise ValidationError()


def is_valid_transaction_type(type_id):
    transaction_service = ServiceBuilder(TransactionService).build()
    if transaction_service.get_transaction_type(type_id) is None:
        raise ValidationError
