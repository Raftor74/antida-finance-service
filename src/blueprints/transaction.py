from flask import Blueprint, request

from forms import create_transaction_form, update_transaction_form
from middleware.wraps import validate, auth_required
from services.category import CategoryNotFound
from services.transaction import (
    TransactionService,
    TransactionNotFound,
    InvalidTransactionType
)
from schemes import TransactionSchema
from utils.response import json_response
from views import ServiceView, SchemaView

bp = Blueprint('transaction', __name__)


class TransactionServiceView(ServiceView, SchemaView):
    service_class = TransactionService
    schema_class = TransactionSchema


class TransactionsView(TransactionServiceView):
    @auth_required
    @validate(schema=create_transaction_form)
    def post(self, form, user):
        user_id = user.get('id')
        try:
            transaction_id = self.service.create(user_id, form)
            transaction = self.service.get_user_transaction_by_id(user_id, transaction_id)
            response = self.schema_response(transaction)
        except InvalidTransactionType:
            return json_response.bad_request({'type': 'Передан неверный тип транзакции'})
        except CategoryNotFound:
            return json_response.bad_request({'category_id': 'Категория транзакции не существует'})
        else:
            return json_response.success(response)

    @auth_required
    def get(self, user):
        user_id = user.get('id')
        query_args = dict(request.args)
        limit = query_args.get('limit', 20)
        offset = query_args.get('offset', 0)
        transactions = self.service.get_user_transactions(user_id, query_args, limit, offset)
        total = self.service.get_user_transactions_count(user_id, query_args)
        schema_transactions = [
            self.schema_response(transaction)
            for transaction in transactions
        ]
        response = {
            'data': schema_transactions,
            'limit': limit,
            'offset': offset,
            'total': total,
        }
        return json_response.success(response)


class TransactionView(TransactionServiceView):
    @auth_required
    def get(self, transaction_id, user):
        try:
            user_id = user.get('id')
            transaction = self.service.get_user_transaction_by_id(user_id, transaction_id)
            response = self.schema_response(transaction)
        except TransactionNotFound:
            return json_response.not_found()
        else:
            return json_response.success(response)

    @auth_required
    @validate(schema=update_transaction_form)
    def patch(self, transaction_id, user, form):
        user_id = user.get('id')
        try:
            self.service.update_transaction(user_id, transaction_id, form)
            transaction = self.service.get_user_transaction_by_id(user_id, transaction_id)
            response = self.schema_response(transaction)
        except TransactionNotFound:
            return json_response.not_found()
        except InvalidTransactionType:
            return json_response.bad_request({'type': 'Передан неверный тип транзакции'})
        except CategoryNotFound:
            return json_response.bad_request({'category_id': 'Категория транзакции не существует'})
        else:
            return json_response.success(response)

    @auth_required
    def delete(self, transaction_id, user):
        try:
            user_id = user.get('id')
            self.service.delete_transaction(user_id, transaction_id)
        except TransactionNotFound:
            return json_response.not_found()
        else:
            return json_response.deleted()


bp.add_url_rule('/<int:transaction_id>/', view_func=TransactionView.as_view('transaction'))
bp.add_url_rule('', view_func=TransactionsView.as_view('transactions'))
