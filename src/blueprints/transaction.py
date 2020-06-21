from flask import Blueprint

from forms import create_transaction_form, update_transaction_form
from middleware.wraps import validate, auth_required
from services.transaction import TransactionNotFound
from utils.response import json_response
from views import TransactionServiceView

bp = Blueprint('transaction', __name__)


class TransactionsView(TransactionServiceView):
    @auth_required
    @validate(schema=create_transaction_form)
    def post(self, form, user):
        user_id = user.pop("id", None)
        transaction_id = self.service.create(user_id, form)
        transaction = self.service.get_user_transaction_by_id(user_id, transaction_id)
        response = self.service.to_response(transaction)
        return json_response.success(response)

    @auth_required
    def get(self, user):
        user_id = user.pop("id", None)
        transactions = self.service.get_user_transactions(user_id)
        response = [
            self.service.to_response(transaction)
            for transaction in transactions
        ]
        return json_response.success(response)


class TransactionView(TransactionServiceView):
    @auth_required
    def get(self, transaction_id, user):
        try:
            user_id = user.pop("id", None)
            transaction = self.service.get_user_transaction_by_id(user_id, transaction_id)
            response = self.service.to_response(transaction)
        except TransactionNotFound:
            return json_response.not_found()
        else:
            return json_response.success(response)

    @auth_required
    @validate(schema=update_transaction_form)
    def patch(self, transaction_id, user, form):
        user_id = user.pop("id", None)
        try:
            self.service.get_user_transaction_by_id(user_id, transaction_id)
        except TransactionNotFound:
            return json_response.not_found()
        self.service.update_transaction(transaction_id, form)
        transaction = self.service.get_user_transaction_by_id(user_id, transaction_id)
        response = self.service.to_response(transaction)

        return json_response.success(response)

    @auth_required
    def delete(self, transaction_id, user):
        try:
            user_id = user.pop("id", None)
            self.service.get_user_transaction_by_id(user_id, transaction_id)
            self.service.delete_transaction(transaction_id)
        except TransactionNotFound:
            return json_response.not_found()
        else:
            return json_response.deleted()


bp.add_url_rule('/<int:transaction_id>/', view_func=TransactionView.as_view('transaction'))
bp.add_url_rule('', view_func=TransactionsView.as_view('transactions'))
