from flask import Blueprint

from forms import create_category_form, update_category_form
from middleware.wraps import validate, auth_required
from services.category import CategoryNotFound, CategoryAlreadyExist
from utils.response import json_response
from views import CategoryServiceView

bp = Blueprint('category', __name__)


class CategoriesView(CategoryServiceView):
    @auth_required
    @validate(schema=create_category_form)
    def post(self, form, user):
        user_id = user.pop("id", None)
        self.service.create(user_id, **form)
        category = self.service.get_user_category_by_name(user_id, form['name'])
        return json_response.success(category)

    @auth_required
    def get(self, user):
        user_id = user.pop("id", None)
        categories = self.service.get_user_categories(user_id)
        return json_response.success(categories)


class CategoryView(CategoryServiceView):
    @auth_required
    def get(self, category_id, user):
        try:
            user_id = user.pop("id", None)
            category = self.service.get_user_category_by_id(user_id, category_id)
        except CategoryNotFound:
            return json_response.not_found()
        else:
            return json_response.success(category)

    @auth_required
    @validate(schema=update_category_form)
    def patch(self, category_id, user, form):
        user_id = user.pop("id", None)
        try:
            self.service.get_user_category_by_id(user_id, category_id)
        except CategoryNotFound:
            return json_response.not_found()
        try:
            self.service.update_category(category_id, form)
            category = self.service.get_user_category_by_name(user_id, form["name"])
        except CategoryAlreadyExist:
            return json_response.conflict()
        else:
            return json_response.success(category)

    @auth_required
    def delete(self, category_id, user):
        try:
            user_id = user.pop("id", None)
            self.service.get_user_category_by_id(user_id, category_id)
            self.service.delete_category(category_id)
        except CategoryNotFound:
            return json_response.not_found()
        else:
            return json_response.deleted()


bp.add_url_rule('/<int:category_id>/', view_func=CategoryView.as_view('category'))
bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
