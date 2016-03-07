import flask

class Admin:

    @staticmethod
    def login(username, password):
        query = 'select count(*) \
                 from admin \
                 where username = \'%s\' and password = \'%s\''
        cur = flask.g.db.cursor()
        cur.execute(query % (username, password))
        rows = cur.fetchall()
        return rows[0][0] == 1
