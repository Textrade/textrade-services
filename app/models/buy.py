import datetime

from app.models.base import BaseModel, db, LAZY
from app.models.user import User
from app.models.book import Book
from app.models.transaction import TransactionStatus


class Buy(BaseModel, db.Model):
    """
        Buy model is a transaction of type for_buy. Here we store the
        information of that transaction.
    """
    __tablename__ = "buy"
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.ForeignKey(Book.__tablename__ + ".isbn"),
                          nullable=False)
    book = db.relationship(Book.__name__, backref=db.backref(__tablename__,
                                                             lazy=LAZY))

    buyer_username = db.Column(db.ForeignKey(User.__tablename__ +
                                             ".username"), nullable=False)
    buyer = db.relationship(User.__name__, backref=db.backref(__tablename__,
                                                              lazy=LAZY))
    seller_username = db.Column(db.ForeignKey(User.__tablename__ +
                                              ".username"), nullable=False)
    seller = db.relationship(User.__name__, backref=db.backref(__tablename__,
                                                               lazy=LAZY))
    price = db.Column(db.Float, nullable=False)
    purchased_date = db.Column(db.DateTime, default=datetime.datetime.now())
    transaction_status = db.Column(db.ForeignKey(
        TransactionStatus.__tablename__ + ".status"), nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    buyer_rating = db.Column(db.Float, nullable=True, default=None)
    seller_rating = db.Column(db.Float, nullable=True, default=None)

    def __init__(self, book: Book, buyer: User, seller: User, price: float,
                 comment: str):
        """
        Buy Constructor
        :param book:
        :param buyer:
        :param seller:
        :param price:
        :param comment:
        :return:
        """
        if buyer.username == seller.username:
            raise self.ModelError("In Buy: buyer.username and seller.username "
                                  "cannot by the same.")
        else:
            self.book = book
            self.book_isbn = book.isbn
            self.buyer = buyer
            self.buyer_username = buyer.username
            self.seller = seller
            self.seller_username = seller.username
            self.price = price
            self.comment = comment

    def __repr__(self) -> str:
        """
        String representation of Buy
        :return: str
        """
        return "<Buy {}: Buyer {} Seller {} Book {}>".format(self)
