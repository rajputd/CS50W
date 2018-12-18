class Review:
    """An object that provides an instance for interacting with records in the review table
    associated with this application."""

    def __init__(self, rating, content, reviewer, book_title):
        self.rating = rating
        self.content = content
        self.reviewer = reviewer
        self.book_title = book_title

    @staticmethod
    def create(conn, rating, content, reviewer_id, book_id):
        """Creates an entry in the reviews table with the provided review data."""
        q = f"""INSERT INTO reviews
                (rating, review_content, reviewer_id, book_id)
            VALUES
                ('{rating}', '{content}', '{reviewer_id}', '{book_id}')"""
        try:
            conn.execute(q)
            conn.commit()
        except Exception as e:
            raise e


    @staticmethod
    def get_reviews_by_bookId(conn, bookId):
        """Returns a list of Book objects that have the given bookId."""

        q = f"""SELECT rating, review_content, username, title
            FROM reviews
            JOIN books ON reviews.book_id=books.book_id
            JOIN users ON reviews.reviewer_id=users.user_id
            WHERE reviews.book_id='{bookId}'"""
        results = conn.execute(q).fetchall()

        reviews = []
        for result in results:
            reviews.append(Review(result[0], result[1], result[2], result[3]))

        return reviews


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
        # get review info
        q = f"SELECT AVG(rating) FROM reviews WHERE book_id='{bookId}'"
        result = conn.execute(q).fetchall()

        #get review_count from query result
        average_score = result[0][0]

        #return None when there are no reviews
        if average_score == None:
            return None

        #convert result into float for easier processing
        return float(average_score)

    @staticmethod
    def get_review_count(conn, bookId):
        """Returns the number of reviews for the given bookId."""
        q = f"SELECT COUNT(rating) FROM reviews WHERE book_id='{bookId}'"
        result = conn.execute(q).fetchall()

        #get review_count from query result
        count = result[0][0]

        return count

