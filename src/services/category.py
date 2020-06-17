from exceptions import ServiceError
from models import Category, IntegrityError


class CategoryServiceError(ServiceError):
    service = 'category'


class CategoryNotFound(CategoryServiceError):
    pass


class ParentCategoryNotFound(CategoryServiceError):
    pass


class CategoryAlreadyExist(CategoryServiceError):
    pass


class CategoryService:
    def __init__(self, connection):
        self.model = Category(connection)

    def create(self, user_id, name, parent_id=None):
        fields = self._make_category_fields(user_id, name, parent_id)
        try:
            return self._create_category(fields)
        except IntegrityError as e:
            raise ParentCategoryNotFound(str(e)) from e

    def get_user_category_by_name(self, user_id, name):
        name = str(name).lower()
        category = self.model.get_user_category_by_name(user_id, name)
        if category is None:
            raise CategoryNotFound()
        return category

    def get_user_category_by_id(self, user_id, id):
        category = self.model.get_user_category_by_id(user_id, id)
        if category is None:
            raise CategoryNotFound()
        return category

    def get_user_categories(self, user_id):
        return self.model.get_categories_by_user(user_id)

    def _create_category(self, attributes: dict):
        attributes['name'] = str(attributes['name']).lower()
        return self.model.create(attributes)

    def _make_category_fields(self, user_id, name, parent_id=None):
        fields = {"name": name, "account_id": user_id}
        if parent_id is not None:
            fields['parent_id'] = parent_id
        return fields
