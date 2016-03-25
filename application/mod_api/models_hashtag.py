import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

class Hashtag:

    def __init__(self, name=None, count=0):
        self.name = name
        self.count = count

    def to_json(self):
        return {
            'name': self.name,
            'count': self.count
        }

    def save(self):
        query_b = SQLBuilder().insert_into('hashtags') \
                              .using_mapping('name') \
                              .and_values_format("'%s'")

        params = (self.name, )
        SQLExecute().perform(query_b, params, commit=True)

    def increment_count(self):
        query_b = SQLBuilder().update('hashtags') \
                              .set([('count', 'count + 1')]) \
                              .where("name = '%s'")

        params = (self.name, )
        SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def get_with_name(name):
        query_b = SQLBuilder().select('*', 'hashtags') \
                              .where("name = '%s'") \
                              .limit('1')

        params = (name, )
        _, rows = SQLExecute().perform_fetch(query_b, params)
        hashtags = Hashtag.parse_rows(rows)
        return hashtags[0] if len(hashtags) == 1 else None

    @staticmethod
    def get_most_popular(limit):
        query_b = SQLBuilder().select('*', 'hashtags') \
                              .order('count desc') \
                              .limit(limit)

        _, rows = SQLExecute.perform_fetch(query_b, None)
        return Hashtag.parse_rows(rows)

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Hashtag(name=row[0], count=row[1])
            items.append(item)
        return items
