import flask
from application.mod_api.utils_sql import SQLCursor


class Token:

    def __init__(self,
            value=None):
        self.value = value


    def to_json(self):
        return TokenDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return TokenDTO.from_json(json)


class TokenDTO:

    @staticmethod
    def to_json(token):
        return {'value': token.value}


    @staticmethod
    def from_json(json):
        return Token(value=json.get('value'))


class TokenDAO:

    @staticmethod
    def save(value):
        query = "insert into tokens \
            (value) values ('%s')"
        params = (value, )
        SQLCursor.perform(query, params)


    @staticmethod
    def get_token(value):
        query = "select * from tokens where value = '%s'"
        params = (value, )
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return TokenDAO._parse_rows(rows)[0]


    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(Token(value=row[0]))
        return items
