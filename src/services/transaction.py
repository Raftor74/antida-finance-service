from datetime import datetime

from .base import ModelService
from .category import CategoryService
from builders import ServiceBuilder
from exceptions import ServiceError
from models import Transaction
from queries.transaction import TransactionQuery


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

    def validate_transaction_type(self, type_id):
        transaction_type = self.get_transaction_type(type_id)
        if transaction_type is None:
            raise InvalidTransactionType()

    def delete_transaction(self, user_id, transaction_id):
        self.validate_transaction_on_exist(user_id, transaction_id)
        return self.model.delete(transaction_id)

    def get_user_transactions(self, user_id, filter: dict, limit: int = None, offset: int = None):
        query = TransactionQuery().set_filter(user_id, filter) \
            .limit(limit) \
            .offset(offset).order('date_time', 'DESC')
        return (
            self.prepare_transaction_fields(transaction)
            for transaction in self.model.find_by_query_many(query)
        )

    def get_user_transactions_count(self, user_id, filter):
        query = TransactionQuery().set_filter(user_id, filter) \
            .select(['COUNT(id) AS CNT'])
        count = self.model.find_by_query_one(query)
        return count.get('CNT') if count is not None else 0

    def get_transaction_type(self, type_id):
        return self.model.TRANSACTION_TYPES.get(type_id)

    @classmethod
    def get_transaction_categories(cls, category_id):
        category_service = ServiceBuilder(CategoryService).build()
        return category_service.get_parent_categories(category_id)

    def _make_transaction_fields(self, user_id, fields):
        fields['account_id'] = user_id
        if 'date_time' not in fields:
            fields['date_time'] = datetime.now().isoformat()
        fields['sum'] = self._sum_to_pennies(fields['sum'])
        return fields

    def _create_transaction(self, attributes: dict):
        return self.model.create(attributes)

    def _update_transaction(self, transaction_id, attributes: dict):
        if 'sum' in attributes:
            attributes['sum'] = self._sum_to_pennies(attributes['sum'])
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
