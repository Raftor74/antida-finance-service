from datetime import datetime

from .base import ModelService
from .category import CategoryService
from builders import ServiceBuilder
from exceptions import ServiceError
from models import Transaction, TransactionTypes
from queries.transaction import TransactionQueryBuilder


class TransactionServiceError(ServiceError):
    service = 'transaction'


class TransactionNotFound(TransactionServiceError):
    pass


class InvalidTransactionType(TransactionServiceError):
    pass


class TransactionService(ModelService):
    model_class = Transaction

    def create(self, user_id, attributes):
        if 'category_id' in attributes:
            self.validate_transaction_category(user_id, attributes['category_id'])
        self.validate_transaction_type(attributes['type'])
        fields = self._make_transaction_fields(user_id, attributes)
        return self._create_transaction(fields)

    def get_user_transaction_by_id(self, user_id, transaction_id):
        transaction = self.model.get_user_transaction_by_id(user_id, transaction_id)
        if transaction is None:
            raise TransactionNotFound()
        return self.prepare_transaction_fields(transaction)

    def prepare_transaction_fields(self, transaction):
        transaction['sum'] = self._pennies_to_rubles(transaction['sum'])
        transaction['date_time'] = self.formatting_date_time(transaction['date_time'])
        transaction['categories'] = self.get_transaction_categories(transaction['category_id'])
        return transaction

    def update_transaction(self, user_id, transaction_id, attributes: dict):
        if 'category_id' in attributes:
            self.validate_transaction_category(user_id, attributes['category_id'])
        if 'type' in attributes:
            self.validate_transaction_type(attributes['type'])
        self.validate_transaction_on_exist(user_id, transaction_id)
        return self._update_transaction(transaction_id, attributes)

    def validate_transaction_on_exist(self, user_id, transaction_id):
        self.get_user_transaction_by_id(user_id, transaction_id)

    @classmethod
    def validate_transaction_category(cls, user_id, category_id):
        if category_id is None:
            return

        service = ServiceBuilder(CategoryService).build()
        service.validate_category_on_exist(user_id, category_id)

    @classmethod
    def validate_transaction_type(cls, type_id):
        if type_id not in TransactionTypes.list():
            raise InvalidTransactionType()

    def delete_transaction(self, user_id, transaction_id):
        self.validate_transaction_on_exist(user_id, transaction_id)
        return self.model.delete(transaction_id)

    def get_user_transactions(self, user_id, filter: dict, limit: int = None, offset: int = None):
        query = TransactionQueryBuilder().set_filter(user_id, filter) \
            .limit(limit) \
            .offset(offset).order('date_time', 'DESC')
        return (
            self.prepare_transaction_fields(transaction)
            for transaction in self.model.find_by_query_many(query)
        )

    def get_user_transactions_count_rows(self, user_id, filter):
        query = TransactionQueryBuilder().set_filter(user_id, filter) \
            .select(['COUNT(id) AS CNT'])
        result = self.model.find_by_query_one(query)
        count = result.get('CNT') if result is not None else 0
        return int(count) if count is not None else 0

    def get_user_transactions_total(self, user_id, filter):
        income_type_id = int(TransactionTypes.INCOME)
        expense_type_id = int(TransactionTypes.EXPENSE)
        income = self._get_user_transactions_subtotal(user_id, filter, income_type_id)
        expense = self._get_user_transactions_subtotal(user_id, filter, expense_type_id)
        total = income - expense
        return self._pennies_to_rubles(total)

    @classmethod
    def get_transaction_categories(cls, category_id):
        category_service = ServiceBuilder(CategoryService).build()
        return category_service.get_parent_categories(category_id)

    def _get_user_transactions_subtotal(self, user_id, filter, type_id):
        query = TransactionQueryBuilder().set_filter(user_id, filter)\
            .where('type', type_id) \
            .select(['SUM(sum) AS SUM'])
        result = self.model.find_by_query_one(query)
        total = result.get('SUM') if result is not None else 0
        return int(total) if total is not None else 0

    def _make_transaction_fields(self, user_id, fields):
        fields['account_id'] = user_id
        if 'date_time' not in fields:
            fields['date_time'] = datetime.now().isoformat()
        fields['sum'] = abs(self._sum_to_pennies(fields['sum']))
        return fields

    def _create_transaction(self, attributes: dict):
        return self.model.create(attributes)

    def _update_transaction(self, transaction_id, attributes: dict):
        if 'sum' in attributes:
            attributes['sum'] = abs(self._sum_to_pennies(attributes['sum']))
        return self.model.update(transaction_id, attributes)

    @classmethod
    def _sum_to_pennies(cls, sum):
        return sum * 100

    @classmethod
    def _pennies_to_rubles(cls, pennies):
        return pennies / 100

    @classmethod
    def formatting_date_time(cls, date_time):
        return datetime.fromisoformat(date_time)
