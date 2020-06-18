from flask import Blueprint

from forms import category_form
from middleware.wraps import validate, auth_required
from services.category import ParentCategoryNotFound, CategoryNotFound
from utils.response import json_response
from views import CategoryServiceView

bp = Blueprint('category', __name__)


class CategoriesView(CategoryServiceView):
    @auth_required
    @validate(schema=category_form)
    def post(self, form, user):
        try:
            user_id = user.pop("id", None)
            self.service.create(user_id, **form)
            category = self.service.get_user_category_by_name(user_id, form['name'])
        except ParentCategoryNotFound:
            return json_response.conflict()
        else:
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


bp.add_url_rule('/<int:category_id>/', view_func=CategoryView.as_view('category'))
bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
