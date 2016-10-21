from app.models.base import BaseModel, db, LAZY
from app.models.user import User
from app.models.book import Book


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