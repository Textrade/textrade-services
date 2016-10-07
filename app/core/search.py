from app import db
from app.models.user import User


class SearchEngine:
    def __init__(self):
        pass

    def book_by_isbn(self, isbn):
        raise NotImplementedError

    def book_by_title(self, title):
        raise NotImplementedError

    def book_by_author(self, author):
        raise NotImplementedError

    def user_by_username(self, username):
        raise NotImplementedError
