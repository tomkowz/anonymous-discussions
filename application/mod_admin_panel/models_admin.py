from application.utils.sql_services import SQLBuilder, SQLExecute

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
        query_b = SQLBuilder().select('*', 'admin') \
                              .where("username = '%s' and password = '%s'") \
                              .limit('1')

        _, rows = SQLExecute().perform_fetch(query_b, (username, password))
        return rows[0] if len(rows) > 0 else None
