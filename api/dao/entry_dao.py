import flask

class EntryDAO:

    TABLE_NAME = 'entries'

    @staticmethod
    def get_all():
        query_f = 'select * from {} order by id desc'
        cur = flask.g.db.execute(query_f.format(EntryDAO.TABLE_NAME))
        rows = cur.fetchall()
        return EntryDAO.parse_rows(rows)

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Entry()
            item.content = row[0]
            items.append(item)
        return items
