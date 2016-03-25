import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

class Token:

    def __init__(self, value=None):
        self.value = value

    def save(self):
        query_b = SQLBuilder().insert_into('tokens') \
                              .using_mapping('value') \
                              .and_values_format("'%s'")
        params = (self.value, )
        SQLExecute().perform(query_b, params, commit=True)

    def to_json(self):
        return {'value': self.value}

    @staticmethod
    def get_with_value(value):
        query_b = SQLBuilder().select('*', 'tokens') \
                              .where("value = '%s'")
        params = (value, )
        _, rows = SQLExecute.perform_fetch(query_b, params)

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            items.append(Token(value=row[0]))
        return items
