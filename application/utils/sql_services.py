import flask
class SQLExecute:
    #query_b = SQLBuilder
    @staticmethod
    def perform_fetch(query_b, params_tuple=None):
        cur = SQLExecute.perform(query_b, params_tuple)
        rows = cur.fetchall()
        return cur, rows

    @staticmethod
    def perform(query_b, params_tuple=None, commit=False):
        cur = flask.g.db.cursor()

        if params_tuple is not None:
            cur.execute(query_b.get_query() % params_tuple)
        else:
            cur.execute(query_b.get_query())

        if commit == True:
            flask.g.db.commit()

        return cur

class SQLBuilder:

    def __init__(self):
        self.query = list()

    def select(self, what, where):
        self.query.append("select {} from {}".format(what, where))
        return self

    def where(self, rules):
        self.query.append("where {}".format(rules))
        return self

    def order(self, how):
        self.query.append("order by {}".format(how))
        return self

    def insert_into(self, where):
        self.query.append("insert into {}".format(where))
        return self

    def using_mapping(self, mapping):
        self.query.append("({})".format(mapping))
        return self

    def and_values_format(self, format_str):
        self.query.append("values ({})".format(format_str))
        return self

    def update(self, what):
        self.query.append("update {}".format(what))
        return self

    def set(self, key_format_tuple):
        set_arr = ["{} = {}".format(k, f) for k, f in key_format_tuple]
        set_str = ', '.join(set_arr)
        self.query.append("set " + set_str)
        return self

    def limit(self, limit):
        if limit is not None:
            self.query.append("limit {}".format(limit))
        return self

    def offset(self, offset):
        if offset is not None:
            self.query.append("offset {}".format(offset))
        return self

    def get_query(self):
        return ' '.join(self.query)
