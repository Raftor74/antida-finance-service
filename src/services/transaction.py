from datetime import datetime

from .base import ModelService
from exceptions import ServiceError
from models import Transaction


class TransactionServiceError(ServiceError):
    service = 'transaction'


class TransactionNotFound(TransactionServiceError):
    pass


class TransactionService(ModelService):
    model_class = Transaction

    def create(self, user_id, fields):
        fields = self._make_transaction_fields(user_id, fields)
        return self._create_transaction(fields)

    def get_user_transaction_by_id(self, user_id, transaction_id):
        transaction = self.model.get_user_transaction_by_id(user_id, transaction_id)
        if transaction is None:
            raise TransactionNotFound()
        return self.prepare_transaction_fields(transaction)

    def prepare_transaction_fields(self, transaction):
        transaction['sum'] = self._pennies_to_rubles(transaction['sum'])
        transaction['date_time'] = self.formatting_date_time(transaction['date_time'])
        return transaction

    def update_transaction(self, user_id, transaction_id, attributes: dict):
        self.validate_transaction_on_exist(user_id, transaction_id)
        return self._update_transaction(transaction_id, attributes)

    def validate_transaction_on_exist(self, user_id, transaction_id):
        self.get_user_transaction_by_id(user_id, transaction_id)

    def delete_transaction(self, user_id, transaction_id):
        self.validate_transaction_on_exist(user_id, transaction_id)
        return self.model.delete(transaction_id)

    def _update_transaction(self, transaction_id, attributes: dict):
        if 'sum' in attributes:
            attributes['sum'] = self._sum_to_pennies(attributes['sum'])
        return self.model.update(transaction_id, attributes)

    def get_user_transactions(self, user_id):
        return (
            self.prepare_transaction_fields(transaction)
            for transaction in self.model.get_transactions_by_user(user_id)
        )

    def get_transaction_type(self, type_id):
        return self.model.TRANSACTION_TYPES.get(type_id)

    def _make_transaction_fields(self, user_id, fields):
        fields['account_id'] = user_id
        if 'date_time' not in fields:
            fields['date_time'] = datetime.now().isoformat()
        fields['sum'] = self._sum_to_pennies(fields['sum'])
        return fields

    def _create_transaction(self, attributes: dict):
        return self.model.create(attributes)

    @classmethod
    def _sum_to_pennies(cls, sum):
        return sum * 100

    @classmethod
    def _pennies_to_rubles(cls, pennies):
        return pennies / 100

    @classmethod
    def formatting_date_time(cls, date_time):
        return datetime.fromisoformat(date_time)
