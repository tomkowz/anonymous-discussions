import flask

from api.model.hashtag import Hashtag

class HashtagDAO:

    @staticmethod
    def insert(item):
        query = 'insert into hashtags (entry_id, value) values (?, ?)'
        cur = flask.g.db.execute(query, [item.entry_id, item.value])
        flask.g.db.commit()
