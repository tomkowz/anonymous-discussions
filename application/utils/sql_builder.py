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
        self.query.append("limit {}".format(limit))
        return self

    def get_query(self):
        return ' '.join(self.query)
