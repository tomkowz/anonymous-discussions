import flask

from api.model.entry import Entry

class EntryDAO:

    @staticmethod
    def get_all():
        query = 'select id, content, timestamp from entries order by id desc'
        cur = flask.g.db.execute(query)
        rows = cur.fetchall()
        return EntryDAO.parse_rows(rows)

    @staticmethod
    def get_with_hashtag(value):
        query_f = 'select id, content, timestamp from entries \
                   inner join hashtags \
                   on hashtags.entry_id = entries.id \
                   where hashtags.value = \'{}\''
        cur = flask.g.db.execute(query_f.format(value))
        rows = cur.fetchall()
        return EntryDAO.parse_rows(rows)

    @staticmethod
    def insert(item):
        query = 'insert into entries (content, timestamp) values (?, ?)'
        cur = flask.g.db.execute(query, [item.content, item.timestamp])
        item.id = cur.lastrowid
        flask.g.db.commit()

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Entry()
            item.id = row[0]
            item.content = row[1]
            item.timestamp = row[2]
            items.append(item)
        return items
