from werkzeug.security import generate_password_hash, check_password_hash

class User:

    def __init__(self, conn, username, password):
        self.conn = conn
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def exists(self):
        q = f"SELECT count(username) FROM users WHERE username='{self.username}' LIMIT 1"
        result = self.conn.execute(q).fetchall()

        if result[0][0] == 1:
           return True

        return False

    def register(self):
        try:
            q = f"INSERT INTO users (username, password) VALUES ('{self.username}', '{self.pw_hash}')"
            self.conn.execute(q)
            self.conn.commit()
        except Exception as e:
            raise e
