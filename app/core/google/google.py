import requests

from app.models.book import Book


class BookAPI:
    @staticmethod
    def load_book_info(val) -> Book:
        """
            This function uses the Google Book API to search for a given isbn
            or a title and create a Book model and return it.
        :param val: str
        :return: Book
        """
        val = val.replace(" ", "%20")  # Replace spaces with '%20'
        data = requests.get(
            "https://www.googleapis.com/books/v1/volumes?q={}".format(
                val)
        ).json()

        if data['totalItems']:
            try:
                description = data['items'][0]['volumeInfo']['description']
            except KeyError:
                description = "No description available."
            book = {
                'isbn': val,
                'title': data['items'][0]['volumeInfo']['title'],
                'author': ', '.join(data['items'][0]['volumeInfo']['authors']),
                'description': description,
                'img_url':
                    data['items'][0]['volumeInfo']['imageLinks']['thumbnail'],
            }
            return Book(
                isbn=book['isbn'],
                title=book['title'],
                author=book['author'],
                description=book['description'],
                img_url=book['img_url'],
            )
        else:
            raise BookAPI.BookDoesNotExist("The book doesn't exists")

    class BookDoesNotExist(Exception):
        pass
