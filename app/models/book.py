import datetime

from app.models.base import BaseModel, db


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
        :param title: str
        :param author: str
        :param description: str
        :param isbn: str
        :param img_url: str
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
        Return a dict representation of Book
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
