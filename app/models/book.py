import datetime

from app.models.base import BaseModel, db, LAZY
from app.core.user import User

# This is the number of days for date_end = date_start + DATE_DELTA
DATE_DELTA = 140


class Book(BaseModel, db.Model):
    """
        Book model stores the information of books that we have cached. We
        will store here any books that we don't know about, so next time,
        instead of requesting to GoogleAPI, we can check if we have the book
        in this table.
    """
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(255), unique=True)
    title = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    img_url = db.Column(db.String(255), unique=True)
    added_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, title: str, author: str, description: str, isbn: str,
                 img_url: str):
        """
        Book Constructor
        :param title:
        :param author:
        :param description:
        :param isbn:
        :param img_url:
        :return:
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.description = description
        self.img_url = img_url

    def __repr__(self) -> str:
        """
        String representation of Book
        :return: str
        """
        return "<Book #{}: {}>".format(self.id, self.title)

    def get_str_date(self) -> str:
        """
        Returns the added date formatted like 02/22/2016
        :return: str
        """
        return self.added_on.strftime("%m/%d/%Y")

    def get_dict(self) -> dict:
        """
        Return a Book in a dict representation
        :return:
        """
        return {
            'id': self.id,
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'img_url': self.img_url,
            'added_on': self.added_on,
        }


class Condition(BaseModel, db.Model):
    """
        Condition stores the different condition of a book. This is a table
        because we want the infrastructure dynamic. If later we need to add
        more conditions, we can append more rows to this table.
    """
    __tablename__ = "condition"
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(255), unique=True)
    label = db.Column(db.String(255))

    def __init__(self, condition: str, label: str = None):
        """
        Condition Constructor
        :param condition:
        :param label:
        :return:
        """
        self.condition = condition
        self.label = label

    def __repr__(self) -> str:
        """
        String representation of Condition
        :return: str
        """
        return "<Condition: {}>".format(self.condition)

    @staticmethod
    def get_by_id(condition: str) -> db.Model:
        """
        Given a condition, it return a Condition if it exists, otherwise None.
        :param condition: str
        :return: Condition | None
        """
        return Condition.query.get(condition)


class ListingType(BaseModel, db.Model):
    """
        ListingType model will hold the type of listing, e.i, for_sale,
        for_rent, for_trade. This is a table because we want the
        infrastructure dynamic. If later we need to add more conditions,
        we can append more rows to this table.
    """
    ___tablename__ = "listing_type"
    id = db.Column(db.Integer, primary_key=True)
    listing_type = db.Column(db.String(20), unique=True)

    def __init__(self, listing_type: str):
        """
        ListingType Constructor
        :param listing_type:
        :return:
        """
        self.listing_type = listing_type

    def __repr__(self):
        """
        String representation of ListingType
        :return: str
        """
        return "<ListingType: {}>".format(self.listing_type)


class Listing(BaseModel, db.Model):
    """
        Listing model is the object for the public and available books that
        costumers can look, rent, buy, or trade.
    """
    __tablename__ = "listing"
    id = db.Column(db.Integer, primary_key=True)
    book_isbn = db.Column(db.ForeignKey(Book.__tablename__ + ".isbn"),
                          nullable=False)
    book = db.relationship(Book.__name__, backref=db.backref(__tablename__,
                                                             lazy=LAZY))
    username = db.Column(db.ForeignKey(User.__tablename__ + ".username"),
                         nullable=False)
    user = db.relationship(User.__name__, backref=db.backref(__tablename__,
                                                             lazy=LAZY))
    price = db.Column(db.Float, nullable=False)
    listing_type = db.Column(db.ForeignKey(ListingType.__tablename__ +
                                           ".listing_type"), nullable=False)
    condition = db.Column(db.ForeignKey(Condition.__tablename__ +
                                        ".condition"), nullable=False)

    def __init__(self, book: Book, user: User, price: float,
                 listing_type: str, condition: str):
        """
        Listing Constructor
        :param book: Book
        :param user: User
        :param price: float
        :param listing_type: str
        :param condition: str
        :return: None
        """
        self.book = book
        self.book_isbn = book.isbn
        self.user = user
        self.username = user.username
        self.price = price
        self.listing_type = listing_type
        self.condition = condition

    def __repr__(self):
        """
        String representation of Listing
        :return: str
        """
        return "<Listing: {} by: {} Type: {}>".format(self.book, self.user,
                                                      self.listing_type)


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


class Rent(BaseModel, db.Model):
    """
        Rent model is a transaction of type for_rent. Here we store the
        information of that transaction coming from Listing.
    """
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
