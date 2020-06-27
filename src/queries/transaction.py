from .base import Query
from builders import ServiceBuilder
from models import Transaction
from services.category import Category


class TransactionQuery(Query):
    table_name = Transaction.table

    def set_filter(self, user_id, query_filter: dict):
        self.filter_by_user(user_id) \
            .filter_by_category(query_filter)
        return self

    def filter_by_user(self, user_id):
        return self.where('account_id', user_id)

    def filter_by_category(self, query_filter: dict):
        category_id = query_filter.get('category')
        if category_id is None:
            return self
        category_service = ServiceBuilder(Category).build()
        sub_categories = category_service.get_subcategories(category_id, ['id'])
        categories_pk = [sub_category['id'] for sub_category in sub_categories]
        categories_pk.append(category_id)
        categories_pk = list(map(str, categories_pk))
        placeholder = ','.join(categories_pk)
        value_placeholder = f'({placeholder})'
        return self.where_raw('category_id', value_placeholder, 'IN')
