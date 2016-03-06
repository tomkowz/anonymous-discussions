import flask

class Entry:

    def __init__(self):
        self.id = None
        self.content = None
        self.timestamp = None
        self.approved = None

    # DTO
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp,
            'approved': self.approved
        }

    @staticmethod
    def from_json(json):
        entry = Entry()
        entry.id = json.get('id')
        entry.content = json.get('content')
        entry.timestamp = json.get('timestamp')
        entry.approved = json.get('approved')
        return entry

    # DAO
    @staticmethod
    def get_all():
        query = 'select * \
                 from entries \
                 order by id desc'
        cur = flask.g.db.execute(query)
        return Entry.parse_rows(cur.fetchall())

    @staticmethod
    def get_all_approved(approved):
        query = 'select * \
                 from entries \
                 where approved = ? \
                 order by id desc'
        cur = flask.g.db.execute(query, [approved])
        return Entry.parse_rows(cur.fetchall())

    @staticmethod
    def get_all_waiting_to_aprove():
        query = 'select * \
                 from entries \
                 where approved is null \
                 order by id desc'
        cur = flask.g.db.execute(query)
        return Entry.parse_rows(cur.fetchall())

    @staticmethod
    def get_with_id(entry_id):
        query = 'select * \
                 from entries where id = ?'
        cur = flask.g.db.execute(query, [entry_id])
        result = Entry.parse_rows(cur.fetchall())
        if len(result) == 1:
            return result[0]
        else:
            return None

    @staticmethod
    def get_with_hashtag(value):
        print value
        query = 'select * \
                 where content like ? and approved = 1 \
                 order by id desc'
        cur = flask.g.db.execute(query, ['%' + '#' + value + '%'])
        return Entry.parse_rows(cur.fetchall())

    def save(self):
        if self.id is None:
            query = 'insert into entries (content, timestamp) values (?, ?)'
            cur = flask.g.db.execute(query, [self.content, self.timestamp])
            self.id = cur.lastrowid
        else:
            query = 'update entries \
                     set content = ?, timestamp = ?, approved = ? \
                     where id = ?'
            flask.g.db.execute(query, [self.content, self.timestamp, self.approved, self.id])
        flask.g.db.commit()

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Entry()
            item.id = row[0]
            item.content = row[1]
            item.timestamp = row[2]
            item.approved = row[3]
            items.append(item)
        return items
