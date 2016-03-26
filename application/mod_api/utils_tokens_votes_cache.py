import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

class TokenVoteCacheItem:

    def __init__(self, user_token, object_id, object_type, value):
        self.user_token = user_token
        self.object_id = object_id
        self.object_type = object_type
        self.value = value

class TokensVotesCache:

    @staticmethod
    def get_vote(user_token, object_id, object_type):
        query_b = SQLBuilder().select('*', 'tokens_votes_cache') \
                              .where("user_token = '%s' and \
                                      object_id = '%s' and \
                                      object_type = '%s'")
        params = (user_token, object_id, object_type)
        _, rows = SQLExecute.perform_fetch(query_b, params)
        items = TokensVotesCache._parse_rows(rows)
        return items[0] if len(items) > 0 else None

    @staticmethod
    def set_vote(user_token, object_id, object_type, value):
        query_b = SQLBuilder().insert_into('tokens_votes_cache') \
                              .using_mapping('user_token, object_id, \
                                              object_type, value') \
                              .and_values_format("'%s', '%s', '%s', '%s'")
        params = (user_token, object_id, object_type, value)
        SQLExecute.perform(query_b, params, commit=True)

    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            item = TokenVoteCacheItem(user_token=row[0],
                                      object_id=row[1],
                                      object_type=row[2],
                                      value=row[3])
            items.append(item)
        return items
