import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

class RecommendedHashtag:

    def __init__(self, name=None, position=0):
        self.name = name
        self.position = position

    def to_json(self):
        return {
            'name': self.name,
            'position': self.position
        }

    @staticmethod
    def get_all():
        query_b = SQLBuilder().select('*', 'recommended_hashtags') \
                              .order('position asc')
        _, rows = SQLExecute().perform_fetch(query_b)
        return RecommendedHashtag.parse_rows(rows)

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = RecommendedHashtag(name=row[0],
                                      position=row[1])
            items.append(item)
        return items
