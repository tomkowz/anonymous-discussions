
from application.mod_api.utils_sql import SQLCursor


class UserSettings:

    def __init__(self,
        mark_my_posts=0):
        self.mark_my_posts = mark_my_posts


    def to_json(self):
        return UserSettingsDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return UserSettingsDTO.from_json(json)



class UserSettingsDTO:

    @staticmethod
    def to_json(us):
        return {
            'mark_my_posts': us.mark_my_posts
        }


    @staticmethod
    def from_json(json):
        return UserSettings(mark_my_posts=json.get('mark_my_posts'))


class UserSettingsDAO:

    @staticmethod
    def get_settings(token):
        query = """SELECT mark_my_posts FROM user_settings
            WHERE token = '%s'
            LIMIT 1"""

        params = (token, )
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return UserSettingsDAO.parse_rows(rows)[0]


    @staticmethod
    def create_settings(token):
        query = """INSERT INTO user_settings (token) VALUES ('%s')"""
        params = (token, )
        SQLCursor.perform(query, params)


    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            items.append(UserSettings(mark_my_posts=row[0]))
        return items
