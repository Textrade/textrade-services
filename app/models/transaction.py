import datetime

from app.models.base import BaseModel, db, LAZY
from app.models.user import User
from app.models.book import Book
from app.models.listing import ListingType

from app.core.book import BookController
from app.core.user import UserController


class TransactionStatus(BaseModel, db.Model):
    """
        TransactionStatus model store the different status of a transaction.
        This  will be something like pending, completed, or cancelled.
    """
    __tablename__ = "transaction_status"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), unique=True)

    def __init__(self, status: str):
        """
        TransactionStatus Constructor
        :param status: str
        :return:
        """
        self.status = status

    def __repr__(self) -> str:
        """
        String representation of TransactionStatus
        :return: str
        """
        return "<TransactionStatus: {}>".format(self.status)

    @staticmethod
    def get_status(status: str) -> db.Model:
        return TransactionStatus.query.get(status)


class TransactionHistory(BaseModel, db.Model):
    """
        TransactionHistory model is use to store all pending, completed,
        and cancelled transactions from any type. The information here is
        coming from models like Trade, Buy, Renting.
    """
    __tablename__ = "transaction_history"
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.ForeignKey(ListingType.__tablename__ +
                                               ".listing_type"), nullable=False)
    user_a_username = db.Column(db.ForeignKey(User.__tablename__ +
                                              ".username"), nullable=False)
    user_a = db.relationship(User.__name__, foreign_keys=[user_a_username])
    user_b_username = db.Column(db.ForeignKey(User.__tablename__ +
                                              ".username"), nullable=False)
    user_b = db.relationship(User.__name__, foreign_keys=[user_b_username])
    book_isbn = db.Column(db.ForeignKey(Book.__tablename__ + ".isbn"),
                          nullable=False)
    book = db.relationship(Book.__name__, backref=db.backref(__tablename__,
                                                             lazy=LAZY))
    price = db.Column(db.Float, nullable=True)
    transaction_date = db.Column(db.DateTime)
    transaction_status = db.Column(db.ForeignKey(
        TransactionStatus.__tablename__ + ".status"), nullable=False)
    rating_user_a = db.Column(db.Integer, default=None)
    rating_user_b = db.Column(db.Integer, default=None)

    def __init__(self, t_type: str, user_a: User, user_b: User, book: Book,
                 price: float, status: str, t_date: datetime.datetime=None):
        self.transaction_type = t_type
        self.user_a = UserController.get_user_by_username(user_a)
        self.user_a_username = self.user_a.username
        self.user_b = UserController.get_user_by_username(user_b)
        self.user_b_username = self.user_b.username
        self.book = BookController(isbn=book).get_book()
        self.book_isbn = self.book.isbn
        self.price = price
        self.transaction_date = t_date
        self.transaction_status = status

    def __repr__(self):
        return ("<TransactionHistory {}: Type {} User A {} User B {} Book {} "
                "Price {} Date {} Status {}>")

    def get_dict(self):
        return {
            'id': self.id,
            'type': self.transaction_type,
            'user_a': self.user_a_username,
            'user_b': self.user_b_username,
            'book_name': self.book.title,
            'book_isbn': self.book_isbn,
            'price': self.price,
            # TODO: Set this to self.transaction_date when no using SQLite
            'date': "",
            'status': self.transaction_status,
            'rating_user_a': self.rating_user_a,
            'rating_user_b': self.rating_user_b,
        }
