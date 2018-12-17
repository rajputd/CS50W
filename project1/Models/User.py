class User:

    def __init__(self, conn):
        self.conn = conn

    def exists(self, username):
        q = f"SELECT count(username) FROM users WHERE username='{username}' LIMIT 1"
        result = self.conn.execute(q).fetchall()

        if result[0][0] == 1:
           return True

        return False

    def register(self, username, password):
        try:
            q = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
            self.conn.execute(q)
            self.conn.commit()
        except Exception as e:
            raise e
