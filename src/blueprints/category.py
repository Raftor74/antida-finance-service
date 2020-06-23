from flask import Blueprint

from forms import create_category_form, update_category_form
from middleware.wraps import validate, auth_required
from services.category import CategoryService, CategoryNotFound, CategoryAlreadyExist
from utils.response import json_response
from views import ServiceView

bp = Blueprint('category', __name__)


class CategoryServiceView(ServiceView):
    service_class = CategoryService


class CategoriesView(CategoryServiceView):
    @auth_required
    @validate(schema=create_category_form)
    def post(self, form, user):
        user_id = user.get('id')
        try:
            category_id = self.service.create(user_id, **form)
            category = self.service.get_user_category_by_id(user_id, category_id)
            response = self.service.to_response(category)
        except CategoryAlreadyExist:
            return json_response.conflict()
        else:
            return json_response.success(response)

    @auth_required
    def get(self, user):
        user_id = user.get('id')
        categories = self.service.get_user_categories(user_id)
        response = [
            self.service.to_response(category)
            for category in categories
        ]
        return json_response.success(response)


class CategoryView(CategoryServiceView):
    @auth_required
    def get(self, category_id, user):
        try:
            user_id = user.get('id')
            category = self.service.get_user_category_by_id(user_id, category_id)
            response = self.service.to_response(category)
        except CategoryNotFound:
            return json_response.not_found()
        else:
            return json_response.success(response)

    @auth_required
    @validate(schema=update_category_form)
    def patch(self, category_id, user, form):
        user_id = user.get('id')
        try:
            self.service.update_category(category_id, user_id, form)
            category = self.service.get_user_category_by_id(user_id, category_id)
            response = self.service.to_response(category)
        except CategoryAlreadyExist:
            return json_response.conflict()
        except CategoryNotFound:
            return json_response.not_found()
        else:
            return json_response.success(response)

    @auth_required
    def delete(self, category_id, user):
        try:
            user_id = user.get('id')
            self.service.delete_category(user_id, category_id)
        except CategoryNotFound:
            return json_response.not_found()
        else:
            return json_response.deleted()


bp.add_url_rule('/<int:category_id>/', view_func=CategoryView.as_view('category'))
bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
