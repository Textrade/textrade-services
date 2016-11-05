from app.core.google.google import BookAPI
from app.models.book import Book


class BookController:
    """
        Book Controller
    """
    def __init__(self, isbn: str=None, title: str=None):
        self.isbn = isbn
        self.title = title

    def get_book(self) -> Book:
        """
            This method returns a Book or raise a
            BookController.BookNotFound if after looking at the cached data
            and Google Books API doesn't get any results.
        :exception: BookController.BookNotFound
        :return:    Book
        """
        book = None
        try:
            book = self.__get_book_from_db()
        except self.BookNoCached:
            book = self.__get_book_from_api()
        finally:
            return book

    def __get_book_from_db(self) -> Book:
        """
            Query the data base Book table to returns a book. If it doesn't
            find one, raise a BookController.BookNoCached.
        :exception: BookController.BookNoCached
        :return:    Book
        """
        book = None
        if self.isbn:
            book = Book.query.filter_by(isbn=self.isbn).first()
        elif self.title:
            book = Book.query.filter_by(title=self.isbn).first()
        else:
            return None

        if book:
            return book
        else:
            raise self.BookNoCached

    def __get_book_from_api(self) -> Book:
        """
            This method uses the BookAPI interface to the Google Book API
            to find an book. If the book doesn't exits, it raises a
            BookNotFound.
        :exception: BookController.BookNotFound
        :return:    Book
        """
        try:
            return BookAPI.load_book_info(self.isbn).create()
        except BookAPI.BookDoesNotExist:
            raise self.BookNotFound

    def build_from_args(self, **kwargs) -> Book:
        """
            Takes a dictionary an build a book. This is a helper function
            created with the purpose of passing the return value of the
            BookAPI interface load_book_info function. This function
            instantiate a Book with this data.
        :param kwargs:
        :return: Book
        """
        return Book(
            isbn=self.isbn,
            title=kwargs['title'],
            author=kwargs['authors'],
            description=kwargs['description'],
            img_url=kwargs['img_url'],
        )

    @staticmethod
    def create(isbn: str=None, title: str=None):
        """
            Creates an instance of the BookController.
        :param title: str
        :param isbn: str
        :return: BookController
        """
        return BookController(isbn, title)

    class BookNoCached(Exception):
        pass

    class BookNotFound(Exception):
        pass
