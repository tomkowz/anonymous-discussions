
class Admin:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        if not self.username or not self.password:
            return False

        return SQLAdmin.select(self.username, self.password) is not None


import flask
class SQLAdmin:

    @staticmethod
    def select(username, password):
        query = "select * from admin \
                 where username = '%s' and password = '%s' \
                 limit 1"

        cur = flask.g.db.cursor()
        cur.execute(query % (username, password))
        rows = cur.fetchall()
        return rows[0] if len(rows) > 0 else None
