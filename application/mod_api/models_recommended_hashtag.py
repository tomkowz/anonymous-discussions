import flask
from application.mod_api.utils_sql import SQLCursor


class RecommendedHashtag:

    def __init__(self,
            name=None,
            position=0):

        self.name = name
        self.position = position


    def to_json(self):
        return RecommendedHashtagDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return RecommendedHashtagDTO.from_json(json)


class RecommendedHashtagDTO:

    @staticmethod
    def to_json(hashtag):
        return {
            'name': hashtag.name,
            'position': hashtag.position
        }


    @staticmethod
    def from_json(json):
        return RecommendedHashtag(name=json.get('name'),
            position=json.get('position'))


class RecommendedHashtagDAO:

    @staticmethod
    def get_all():
        query = "select * from recommended_hashtags \
            order by position asc"
        rows = SQLCursor.perform_fetch(query, tuple())
        return RecommendedHashtagDAO._parse_rows(rows)


    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(RecommendedHashtag(name=row[0],
                position=row[1]))
        return items
