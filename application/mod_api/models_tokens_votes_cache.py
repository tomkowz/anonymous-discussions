import flask
from application.mod_api.utils_sql import SQLCursor


class TokensVotesCacheItem:

    def __init__(self,
            user_token,
            object_id,
            object_type,
            value):
        self.user_token = user_token
        self.object_id = object_id
        self.object_type = object_type
        self.value = value


class TokensVotesCacheDAO:

    @staticmethod
    def get_vote(user_token, object_id, object_type):
        query = "select * from tokens_votes_cache \
            where user_token = '%s' and \
                object_id = '%s' and \
                object_type = '%s'"

        params = (user_token, object_id, object_type)
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return TokensVotesCacheDAO._parse_rows(rows)[0]

    @staticmethod
    def set_vote(user_token, object_id, object_type, value):
        query = "insert into tokens_votes_cache \
            (user_token, object_id, object_type, value) \
            values ('%s', '%s', '%s', '%s')"

        params = (user_token, object_id, object_type, value)
        SQLCursor.perform(query, params)

    @staticmethod
    def update_vote(user_token, object_id, object_type, value):
        query = "update tokens_votes_cache \
            set value = '%s' \
            where user_token = '%s' and \
                object_id = '%s' and \
                object_type = '%s'"
        params = (value, user_token, object_id, object_type)
        SQLCursor.perform(query, params)

    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(TokensVotesCacheItem(user_token=row[0],
                object_id=row[1],
                object_type=row[2],
                value=row[3]))
        return items
