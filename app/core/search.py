from app import db
from app.models.user import User
from app.models.book import BookToRent


class SearchEngine:
    def __init__(self):
        pass

    @staticmethod
    def book_by_isbn(isbn):
        return BookToRent.query.filter(BookToRent.isbn.contains('%{}%'.format(isbn)))

    def book_by_title(self, title):
        raise NotImplementedError

    def book_by_author(self, author):
        raise NotImplementedError

    def user_by_username(self, username):
        raise NotImplementedError
