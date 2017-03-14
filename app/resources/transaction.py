from flask import Blueprint
from flask_restful import Resource, Api, fields, marshal, reqparse

from app.auth.auth import client_auth
from app.core.tools import ResponseTemplate
from app.core.transaction import TransactionHistory, TransactionController

transaction_fields = {
    'id': fields.Integer,
    'type': fields.String,
    'user_a': fields.String,
    'user_b': fields.String,
    'book_name': fields.String,
    'book_isbn': fields.String,
    'price': fields.String,
    # 'date': fields.DateTime,
    'status': fields.String,
    'rating_user_a': fields.Integer,
    'rating_user_b': fields.Integer
}


class TransactionRes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument(
            'type',
            type=str,
            required=True,
            help="Transaction type is required"
        )
        self.parser.add_argument(
            'user_a',
            type=str,
            required=True,
            help="Username A is required"
        )
        self.parser.add_argument(
            'user_b',
            type=str,
            required=True,
            help="Username B is required"
        )
        self.parser.add_argument(
            'book',
            type=str,
            required=True,
            help="Book's ISBN required"
        )
        self.parser.add_argument(
            'price',
            type=float,
            required=True,
            help="Price is required"
        )
        self.parser.add_argument(
            'status',
            type=str,
            required=False,
        )
        super().__init__()

    @client_auth.login_required
    def get(self, transaction_id):
        try:
            transaction = TransactionController.get_transaction_by_id(
                transaction_id)
        except TransactionHistory.NotFound as e:
            return ResponseTemplate(status=404, msg=str(e)).response()
        else:
            transaction_content = marshal(transaction.get_dict(),
                                          transaction_fields)
            return ResponseTemplate(status=200,
                                    content=transaction_content).response()

    @client_auth.login_required
    def post(self):
        args = self.parser.parse_args()
        transaction = TransactionController.create_transaction(**args)
        content = marshal(transaction.get_dict(), transaction_fields)
        return ResponseTemplate(status=200, content=content).response()

transaction_api = Blueprint('app.res.transaction', __name__)
api = Api(transaction_api)

api.add_resource(
    TransactionRes,
    '/transactions',
    '/transactions/<int:transaction_id>',
    endpoint='transactions'
)
