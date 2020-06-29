from flask import Blueprint, request

from forms import (
    create_transaction_form,
    update_transaction_form,
    filter_transaction_form
)
from middleware.wraps import auth_required, validate, validate_query_args
from services.transaction import (
    TransactionService,
    TransactionNotFound,
    TransactionCategoryNotFound,
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
        except InvalidTransactionType as e:
            return json_response.bad_request(e.get_error_message())
        except TransactionCategoryNotFound as e:
            return json_response.bad_request(e.get_error_message())
        else:
            return json_response.success(response)

    @auth_required
    @validate_query_args(schema=filter_transaction_form)
    def get(self, user, form):
        user_id = user.get('id')
        limit = form.get('limit', 20)
        offset = form.get('offset', 0)
        transactions = self.service.get_user_transactions(user_id, form, limit, offset)
        count = self.service.get_user_transactions_count_rows(user_id, form)
        total = self.service.get_user_transactions_total(user_id, form)
        schema_transactions = [
            self.schema_response(transaction)
            for transaction in transactions
        ]
        response = {
            'data': schema_transactions,
            'limit': limit,
            'offset': offset,
            'count': count,
            'total': total
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
        except InvalidTransactionType as e:
            return json_response.bad_request(e.get_error_message())
        except TransactionCategoryNotFound as e:
            return json_response.bad_request(e.get_error_message())
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
