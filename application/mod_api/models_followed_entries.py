import flask
from application.mod_api.utils_sql import SQLCursor

class FollowedEntriesItem:

    def __init__(self, user_token=None, entry_id=None):
        self.user_token = user_token
        self.entry_id = entry_id


    def to_json(self):
        return FollowEntriesDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return FollowEntriesDTO.from_json(json)


class FollowedEntriesDTO:

    @staticmethod
    def to_json(item):
        return {
            'user_token': item.user_token,
            'entry_id': item.entry_id
        }


    @staticmethod
    def from_json(json):
        return FollowEntriesItem(user_token=json.get('user_token'),
            entry_id=json.get('entry_id'))


class FollowedEntriesDAO:

    @staticmethod
    def follow_entry(entry_id, user_token):
        query = "insert into followed_entries \
            (entry_id, user_token) values ('%s', '%s')"
        params = (entry_id, user_token)
        SQLCursor.perform(query, params)


    @staticmethod
    def unfollow_entry(entry_id, user_token):
        query = "delete from followed_entries \
            where entry_id = '%s' and user_token = '%s'"
        params = (entry_id, user_token)
        SQLCursor.perform(query, params)


    @staticmethod
    def get_followed_entries(user_token):
        query = "select * from followed_entries \
            where user_token = '%s'"
        params = (user_token, )
        rows = SQLCursor.perform_fetch(query, params)
        return FollowEntriesDAO._parse_rows(rows)


    @staticmethod
    def get_user_tokens_for_entry(entry_id):
        query = "select * from followed_entries \
            where entry_id = '%s'"
        params = (entry_id, )
        rows = SQLCursor.perform_fetch(query, params)
        return FollowedEntriesDAO._parse_rows(rows)


    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(FollowedEntriesItem(user_token=row[0],
                entry_id=row[1]))
        return items
