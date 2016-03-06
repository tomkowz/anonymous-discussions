import flask

class Comment:

    @property
    def id(self):
        return self._id

    def id(self, v):
        self._id = v

    @property
    def content(self):
        return self._content

    def content(self, v):
        self._content = v

    @property
    def timestamp(self):
        return self._timestamp

    def timestamp(self, v):
        self._timestamp = v

    @property
    def entry_id(self):
        return self._entry_id

    def entry_id(self, v):
        self._entry_id = v

    # DTO
    @staticmethod
    def from_json(json):
        obj = Comment()
        obj.id = json.get('id', None)
        obj.content = json.get('content', None)
        obj.timestamp = json.get('timestamp', None)
        obj.entry_id = json.get('entry_id', None)

    def to_json(self):
        json = dict()
        json['id'] = self.id
        json['content'] = self.content
        json['timestamp'] = self.timestamp
        json['entry_id'] = self.entry_id

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