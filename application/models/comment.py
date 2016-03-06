import flask

class Comment:

    def __init__(self):
        self.id = None
        self.content = None
        self.timestamp = None
        self.entry_id = None

    # DTO
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp,
            'entry_id': self.entry_id
        }

    @staticmethod
    def from_json(json):
        obj = Comment()
        obj.id = json.get('id', None)
        obj.content = json.get('content', None)
        obj.timestamp = json.get('timestamp', None)
        obj.entry_id = json.get('entry_id', None)

    @staticmethod
    def get_all():
        query = 'select id, content, timestamp, entry_id from comments order by id desc'
        cur = flask.g.db.execute(query)
        return Comment.parse_rows(cur.fetchall())

    @staticmethod
    def get_comments_count_with_entry_id(entry_id):
        query = 'select count(*) from comments \
                 where entry_id = ?'
        cur = flask.g.db.execute(query, [entry_id])
        return cur.fetchall()[0][0]

    @staticmethod
    def get_with_entry_id(entry_id):
        query = 'select id, content, timestamp, entry_id from comments \
                 where entry_id = ? \
                 order by id desc'
        cur = flask.g.db.execute(query, [entry_id])
        return Comment.parse_rows(cur.fetchall())

    def save(self):
        query = 'insert into comments (content, timestamp, entry_id) values (?, ?, ?)'
        cur = flask.g.db.execute(query, [self.content, self.timestamp, self.entry_id])
        self.id = cur.lastrowid
        flask.g.db.commit()

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Comment()
            item.id = row[0]
            item.content = row[1]
            item.timestamp = row[2]
            item.entry_id = row[3]
            items.append(item)
        return items
