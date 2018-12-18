class Book:
    """An object that provides access to the books table in this application's database."""

    def __init__(self, bookId, isbn, title, author, year):
        """Returns an instance of the Book Model for a particular book."""
        self.bookId = bookId
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    @staticmethod
    def find(conn, query):
        """Returns a list of Book objects whose isbn, title, or author match the query string
        provided."""

        # search db for book with a matching ISBN, title, or author
        q = f"""SELECT * FROM books
                WHERE
                    isbn LIKE'%{query}%' OR
                    title LIKE '%{query}%' OR
                    author LIKE '%{query}%'"""
        results = conn.execute(q).fetchall()

        # convert results into Books
        books = []
        for result in results:
            books.append(Book(result[0], result[1], result[2], result[3], result[4]))

        return books
