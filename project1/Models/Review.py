class Review:
    """An object that provides an instance for interacting with records in the review table
    associated with this application."""

    def __init__(self, rating, review_content, reviewer_id, book_id):
        self.rating = rating
        self.review_content = review_content
        self.reviewer_id = reviewer_id
        self.book_id = book_id

    @staticmethod
    def create(conn, review):
        """Creates an entry in the reviews table with the provided review data."""
        pass

    @staticmethod
    def get_reviews_by_bookId(conn, bookId):
        """Returns a list of Book objects that have the given bookId."""
        pass


    @staticmethod
    def get_unique_review(conn, bookId, userId):
        """Returns the unique review associated with the given bookId, userId pair."""
        pass

    @staticmethod
    def update_review(conn, review):
        """Dpdates the review associated with the given review object with the contents of
        the given review."""
        pass

    @staticmethod
    def delete_review(conn, review):
        """Removes the given review from the database"""
        pass

    @staticmethod
    def get_avg_rating(conn, bookId):
        """Returns the average rating for the given bookId. Returns None if book has no reviews."""
        pass