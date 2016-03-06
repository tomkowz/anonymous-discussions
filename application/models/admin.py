import flask

class Admin:

    @staticmethod
    def login(username, password):
        query = 'select count(*) \
                 from admin \
                 where username = ? and password = ?'
        cur = flask.g.db.execute(query, [username, password])
        rows = cur.fetchall()
        return rows[0][0] == 1
