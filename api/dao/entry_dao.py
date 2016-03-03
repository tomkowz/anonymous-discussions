import flask

from api.model.entry import Entry

class EntryDAO:

    TABLE_NAME = 'entries'

    @staticmethod
    def get_all():
        query_f = 'select id, content, timestamp from {} order by id desc'
        cur = flask.g.db.execute(query_f.format(EntryDAO.TABLE_NAME))
        rows = cur.fetchall()
        return EntryDAO.parse_rows(rows)

    @staticmethod
    def insert(item):
        query_f = 'insert into {} (content, timestamp) values (?, ?)'
        cur = flask.g.db.execute(query_f.format(EntryDAO.TABLE_NAME), [item.content, item.timestamp])
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
