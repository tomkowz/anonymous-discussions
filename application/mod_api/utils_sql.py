import flask


class SQLCursor:

    @staticmethod
    def perform_fetch(query_str, params_tup):
        cur = flask.g.db.cursor()
        cur.execute(query_str % params_tup)
        rows = cur.fetchall()
        return rows


    @staticmethod
    def perform(query_str, params_tup):
        cur = flask.g.db.cursor()
        cur.execute(query_str % params_tup)
        flask.g.db.commit()
        return cur
