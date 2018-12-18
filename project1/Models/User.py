from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """An object that provides access to the users table in this applications database."""

    def __init__(self, conn, username="", password=""):
        """Returns an instance of the User Model.
        conn is a SQL alchemy connection to the database and is required.
        username and password are the users credentials and are optional.
        """
        self.conn = conn
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """Generates a hash of the given password and sets the password hash member field of
        this object."""
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the given (unhashed) password matches with the hash associated with the
         current user."""
        return check_password_hash(self.pw_hash, password)

    def exists(self):
        """Returns True if the user with the set username exists, false otherwise."""
        q = f"SELECT count(username) FROM users WHERE username='{self.username}' LIMIT 1"
        result = self.conn.execute(q).fetchall()

        if result[0][0] == 1:
           return True

        return False

    def register(self):
        """Inserts the given user into the table of know users. Throws an error if a database
         issue occurs."""
        try:
            q = f"INSERT INTO users (username, password) VALUES ('{self.username}', '{self.pw_hash}')"
            self.conn.execute(q)
            self.conn.commit()
        except Exception as e:
            raise e

    def get_user_id(self):
        """Returns the user_id of the associated user. Returns None if there is no user_id"""
        q = f"SELECT user_id FROM users WHERE username='{self.username}'"
        result = self.conn.execute(q).fetchall()

        if len(result) == 0:
            return None

        return result[0][0]

    @staticmethod
    def get_user_by_username(conn, username):
        """Returns a User object if an account with the given username exists, returns None
         otherwise."""

        #see if password for given username exists
        q = f"SELECT password FROM users WHERE username='{username}'"
        result = conn.execute(q).fetchall()

        #if password does not exist then return nothing
        if len(result) == 0:
            return None

        #construct user object
        user = User(conn, username)
        user.pw_hash = result[0][0]

        return user


