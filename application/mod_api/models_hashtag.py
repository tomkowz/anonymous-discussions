import flask
from application.mod_api.utils_sql import SQLCursor


class Hashtag:

    def __init__(self,
        name=None,
        count=0):

        self.name = name
        self.count = count


    def to_json(self):
        return HashtagDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return HashtagDTO.from_json(json)


class HashtagDTO:

    @staticmethod
    def to_json(hashtag):
        return {
            'name': hashtag.name,
            'count': hashtag.count
        }


    @staticmethod
    def from_json(json):
        return Hashtag(name=json.get('name'),
            count=json.get('count'))


class HashtagDAO:

    @staticmethod
    def save(hashtag_name):
        query = "insert into hashtags \
            (name) values ('%s')"
        params = (hashtag_name, )
        SQLCursor.perform(query, params)


    @staticmethod
    def increment_count(hashtag_name):
        query = "update hashtags \
            set count = (count + 1) \
            where name = '%s'"
        params = (hashtag_name, )
        SQLCursor.perform(query, params)


    @staticmethod
    def get_hashtag(hashtag_name):
        query = "select * from hashtags \
            where name = '%s'"
        params = (hashtag_name, )
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return HashtagDAO._parse_rows(rows)[0]


    @staticmethod
    def get_most_popular_hashtags(limit):
        query = "select * from hashtags \
            order by count desc limit {}".format(limit)
        rows = SQLCursor.perform_fetch(query, tuple())
        return HashtagDAO._parse_rows(rows)


    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(Hashtag(name=row[0],
                count=row[1]))
        return items
