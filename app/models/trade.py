import datetime

from app.models.base import BaseModel, db, LAZY
from app.models.user import User
from app.models.book import Book
from app.models.transaction import TransactionStatus


class Trade(BaseModel, db.Model):
    """
        Trade model is a transaction of type for_trade. Here we store the
        information of that transaction coming from Listing.
    """
    __tablename__ = "trade"
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.ForeignKey(Book.__tablename__ + ".isbn"),
                          nullable=False)
    book = db.relationship(Book.__name__, backref=db.backref(__tablename__,
                                                             lazy=LAZY))

    user_a_username = db.Column(db.ForeignKey(User.__tablename__ +
                                              ".username"), nullable=False)
    user_a = db.relationship(User.__name__, backref=db.backref(
        __tablename__, lazy=LAZY))
    user_b_username = db.Column(db.ForeignKey(User.__tablename__ +
                                                ".username"), nullable=False)
    user_b = db.relationship(User.__name__, backref=db.backref(
        __tablename__, lazy=LAZY))
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    transaction_status = db.Column(db.ForeignKey(
        TransactionStatus.__tablename__ + ".status"), nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    user_a_rating = db.Column(db.Float, nullable=True, default=None)
    user_b_rating = db.Column(db.Float, nullable=True, default=None)

    def __init__(self, book: Book, user_a: User, user_b: User, status: str,
                 comment: str):
        self.book = book
        self.book_isbn = book.isbn
        self.user_a = user_a
        self.user_a_username = user_a.username
        self.user_b = user_b
        self.user_b_username = user_b.username
        self.transaction_status = status
        self.comment = comment

    def __repr__(self):
        """
        String representation of Trade
        :return: str
        """
        return "<Rent {}: User A {} User B {} Book {}>".format(
            self.id, self.user_a, self.user_b, self.book)
