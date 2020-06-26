from .base import ModelService
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


class CategoryService(ModelService):
    model_class = Category

    def create(self, user_id, attributes: dict):
        if 'parent_id' in attributes:
            self.validate_parent_category_on_exist(user_id, attributes['parent_id'])

        try:
            attributes.update({'account_id': user_id})
            return self._create_category(attributes)
        except IntegrityError as e:
            raise CategoryAlreadyExist(str(e)) from e

    def get_user_category_by_id(self, user_id, category_id):
        category = self.model.get_user_category_by_id(user_id, category_id)
        if category is None:
            raise CategoryNotFound()
        return category

    def get_user_categories(self, user_id):
        return self.model.get_categories_by_user(user_id)

    def update_category(self, category_id, user_id, attributes: dict):
        self.validate_category_on_exist(user_id, category_id)

        if 'parent_id' in attributes:
            self.validate_parent_category_on_exist(user_id, attributes['parent_id'])

        try:
            return self._update_category(category_id, attributes)
        except IntegrityError as e:
            raise CategoryAlreadyExist(str(e)) from e

    def validate_category_on_exist(self, user_id, category_id):
        self.get_user_category_by_id(user_id, category_id)

    def validate_parent_category_on_exist(self, user_id, category_id):
        try:
            self.get_user_category_by_id(user_id, category_id)
        except CategoryNotFound as e:
            raise ParentCategoryNotFound(str(e)) from e

    def delete_category(self, user_id, category_id):
        self.validate_category_on_exist(user_id, category_id)
        return self.model.delete(category_id)

    def _update_category(self, category_id, attributes: dict):
        if 'name' in attributes:
            attributes['name'] = str(attributes['name']).lower()
        return self.model.update(category_id, attributes)

    def _create_category(self, attributes: dict):
        attributes['name'] = str(attributes['name']).lower()
        return self.model.create(attributes)
