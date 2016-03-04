import flask

from api.model.hashtag import Hashtag

class HashtagDAO:

    TABLE_NAME = 'hashtags'

    @staticmethod
    def insert(item):
        query_f = 'insert into {} (entry_id, value) values (?, ?)'
        cur = flask.g.db.execute(query_f.format(HashtagDAO.TABLE_NAME),
                                 [item.entry_id, item.value])
        flask.g.db.commit()
