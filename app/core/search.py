from app import db
from app.models.user import User
from app.models.book import Book


class SearchEngine:
    def __init__(self):
        pass

    @staticmethod
    def book_by_isbn(isbn):
        return Book.query.filter(Book.isbn.like('{}%'.format(isbn)))

    @staticmethod
    def book_by_title(title):
        return Book.query.filter(Book.name.contains('%{}%'.format(title)))

    def book_by_author(self, author):
        raise NotImplementedError

    def user_by_username(self, username):
        raise NotImplementedError
