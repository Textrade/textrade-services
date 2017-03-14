from app.models.transaction import TransactionHistory, TransactionStatus, db
from app.core.book import BookController
from app.core.user import UserController


class TransactionController:

    @staticmethod
    def create_transaction(**kwargs):
        transaction = TransactionHistory(
            t_type=kwargs['type'],
            user_a=kwargs['user_a'],
            user_b=kwargs['user_b'],
            book=kwargs['book'],
            price=kwargs['price'],
            # t_date=kwargs['date'],
            status=kwargs['status']
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def get_transaction_by_id(transaction_id):
        transaction = TransactionHistory.query.filter_by(
            id=transaction_id).first()
        if transaction is None:
            raise TransactionHistory.NotFound("%d is not a transaction."
                                              % transaction_id)
        else:
            return transaction
