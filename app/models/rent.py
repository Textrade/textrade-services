import datetime

from app.models.base import BaseModel, db, LAZY
from app.models.user import User
from app.models.book import Book
from app.models.transaction import TransactionStatus


class Rent(BaseModel, db.Model):
    """
        Rent model is a transaction of type for_rent. Here we store the
        information of that transaction coming from Listing.
    """
    # This is the number of days for date_end = date_start + DATE_DELTA
    DATE_DELTA = 140
    __tablename__ = "rent"
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.ForeignKey(Book.__tablename__ + ".isbn"),
                          nullable=False)
    book = db.relationship(Book.__name__, backref=db.backref(__tablename__,
                                                             lazy=LAZY))
    by_username = db.Column(db.ForeignKey(User.__tablename__ + ".username"),
                            nullable=False)
    by = db.relationship(User.__name__, backref=db.backref(__tablename__,
                                                           lazy=LAZY))
    to_username = db.Column(db.ForeignKey(User.__tablename__ + ".username"),
                            nullable=False)
    to = db.relationship(User.__name__, backref=db.backref(__tablename__,
                                                           lazy=LAZY))
    price = db.Column(db.Float, nullable=False)
    date_start = db.Column(db.Date, default=datetime.date.today())
    date_end = db.Column(db.Date, default=datetime.date.today() +
                                          datetime.timedelta(days=DATE_DELTA))
    transaction_status = db.Column(db.ForeignKey(
        TransactionStatus.__tablename__ + ".status"), nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    by_rating = db.Column(db.Float, nullable=True, default=None)
    to_rating = db.Column(db.Float, nullable=True, default=None)

    def __init__(self, book: Book, by: User, to: User, price: float,
                 status: str, comment: str):
        """
        Rent Constructor
        :param book: Book
        :param by: User
        :param to: User
        :param price: float
        :param status: str
        :param comment: str
        :return:
        """
        if by.username == to.username:
            raise self.ModelError("In Rent: by.username and to.username "
                                  "cannot be the same user")
        else:
            self.book = book
            self.book_isbn = book.isbn
            self.by = by
            self.by_username = by.username
            self.to = to
            self.to_username = to.username
            self.transaction_status = status
            self.price = price
            self.comment = comment

    def __repr__(self) -> str:
        """
        String representation of Rent
        :return: str
        """
        return "<Rent {}: To {} By {} Book {}>".format(self.id, self.to,
                                                       self.book)
