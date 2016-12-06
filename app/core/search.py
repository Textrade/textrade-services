from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import db
from app.models.user import User
from app.models.book import Book
from app.core.book import BookController


class SearchEngine:
    """
        This is the search engine of the services. The goal of the engine is
        to get data from the data base. If the data is not found, it find it
        elsewhere, if the context is valid, and cached so that next time
        there is no need to look somewhere else.
    """
    def __init__(self, query: str):
        """
            This is the constructor of the SearchEngine class. Here we try to
            interpret the format of the query which decides where we are
            searching.
        :param query: str
        :return:
        """
        self.isbn = None
        self.title = None

        if query.isdigit():
            self.isbn = query
        elif not query.isnumeric():
            self.title = query

    def search(self) -> ([db.Model], bool):
        """
            This function returns a tuple with the list of objects and a flag
            where False is that the results are not exact and True is that
            the result contains both, exact and result like the query.
            This function might return None if the query is couldn't produce
            any search.
        :return: db.Model
        """
        results = []

        if self.isbn:
            rv = self.__book_by_isbn()
            if rv:
                results.append(rv)
            results = list(set(results + self.__book_like_isbn()))
        elif self.title:
            rv = self.__book_by_title()
            if rv:
                results.append(rv)
            results = list(set(results + self.__book_like_title()))
        else:
            return None

        for book in results:
            if Book.query.filter_by(isbn=book.isbn).first():
                pass
            else:
                Book(title=book.title, author=book.author,
                     description=book.description, isbn=book.isbn,
                     img_url=book.img_url).create()
        return results, (len(results) > 0)  # TODO: Test this results

    def __book_by_isbn(self) -> Book:
        """
            This function calls the BookController to get a book by the isbn.
        :return: Book
        """
        return BookController.create(self.isbn).get_book()

    def __book_by_title(self) -> Book:
        """
            This function calls the BookController to get a Book by title.
        :return: Book
        """
        return BookController.create(self.title).get_book()

    def __book_like_isbn(self) -> [Book]:
        """
            This method returns a list of Book that are like the isbn in the
            query.
        :return: [Book]
        """
        return [obj for obj in Book.query.filter(Book.isbn.like('{}%'.format(
            self.isbn)))]

    def __book_like_title(self) -> [Book]:
        """
            This method returns a list of Book that are like the title in the
            query.
        :return:
        """
        return [obj for obj in Book.query.filter(
            Book.title.contains('%{}%'.format(self.title)))]

    def __book_by_author(self) -> Book:
        raise NotImplementedError

    def user_by_username(self, username) -> User:
        raise NotImplementedError
