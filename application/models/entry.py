import flask

class Entry:

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
    def approved(self):
        return self._approved

    def approved(self, v):
        self._approved = v

    # DTO
    def to_json(self):
        json = dict()
        json['id'] = self.id
        json['content'] = self.content
        json['timestamp'] = self.timestamp
        return json

    @staticmethod
    def from_json(json):
        entry = Entry()
        entry.id = json.get('id')
        entry.content = json.get('content')
        entry.timestamp = json.get('timestamp')
        return entry

    # DAO
    @staticmethod
    def get_all():
        query = 'select id, content, timestamp, approved \
                 from entries \
                 order by id desc'
        cur = flask.g.db.execute(query)
        return Entry.parse_rows(cur.fetchall())

    @staticmethod
    def get_all_approved(approved):
        query = 'select id, content, timestamp, approved \
                 from entries \
                 where approved = ? \
                 order by id desc'
        cur = flask.g.db.execute(query, [approved])
        return Entry.parse_rows(cur.fetchall())

    @staticmethod
    def get_with_id(entry_id):
        query = 'select id, content, timestamp, approved \
                 from entries where id = ? and approved = 1'
        cur = flask.g.db.execute(query, [entry_id])
        result = Entry.parse_rows(cur.fetchall())
        if len(result) == 1:
            return result[0]
        else:
            return None

    @staticmethod
    def get_with_hashtag(value):
        print value
        query = 'select id, content, timestamp, approved from entries \
                 where content like ? and approved = 1 \
                 order by id desc'
        cur = flask.g.db.execute(query, ['%' + '#' + value + '%'])
        return Entry.parse_rows(cur.fetchall())

    def save(self):
        query = 'insert into entries (content, timestamp) values (?, ?)'
        cur = flask.g.db.execute(query, [self.content, self.timestamp])
        self.id = cur.lastrowid
        flask.g.db.commit()

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Entry()
            item.id = row[0]
            item.content = row[1]
            item.timestamp = row[2]
            item.timestamp = row[3]
            items.append(item)
        return items
