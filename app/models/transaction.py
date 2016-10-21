import datetime

from app.models.base import BaseModel, db, LAZY
from app.models.user import User
from app.models.book import Book
from app.models.listing import ListingType


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
    user_a = db.relationship(User.__name__, backref=db.backref(__tablename__,
                                                               lazy=LAZY))
    user_b_username = db.Column(db.ForeignKey(User.__tablename__ +
                                              ".username"), nullable=False)
    user_b = db.relationship(User.__name__, backref=db.backref(__tablename__,
                                                               lazy=LAZY))
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
                 price: float, t_date: datetime.datetime, status: str):
        self.transaction_type = t_type
        self.user_a = user_a
        self.user_a_username = user_a.username
        self.user_b = user_b
        self.user_b_username = user_b.username
        self.book = book
        self.book_isbn = book.isbn
        self.price = price
        self.transaction_date = t_date
        self.transaction_status = status

    def __repr__(self):
        return ("<TransactionHistory {}: Type {} User A {} User B {} Book {} "
                "Price {} Date {} Status {}>")
