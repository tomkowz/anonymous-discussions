import flask

class Comment:

    def __init__(self):
        self.id = None
        self.content = None
        self.created_at = None
        self.entry_id = None

    # DTO
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'entry_id': self.entry_id
        }

    @staticmethod
    def from_json(json):
        obj = Comment()
        obj.id = json.get('id', None)
        obj.content = json.get('content', None)
        obj.created_at = json.get('created_at', None)
        obj.entry_id = json.get('entry_id', None)

    @staticmethod
    def get_all():
        query = 'select id, content, created_at, entry_id \
                 from comments \
                 order by id desc'
        cur = flask.g.db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return Comment.parse_rows(rows)

    @staticmethod
    def get_comments_count_with_entry_id(entry_id):
        query = 'select count(*) \
                 from comments \
                 where entry_id = %s'
        cur = flask.g.db.cursor()
        cur.execute(query % (entry_id))
        return cur.fetchall()[0][0]

    @staticmethod
    def get_with_entry_id(entry_id, order):
        query = 'select * \
                 from comments \
                 where entry_id = %s \
                 order by id %s'
        cur = flask.g.db.cursor()
        cur.execute(query % (entry_id, order))
        rows = cur.fetchall()
        return Comment.parse_rows(rows)

    def save(self):
        mysql_created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')

        query = 'insert into comments (content, created_at, entry_id) \
                 values (\'%s\', \'%s\', %s)'
        cur = flask.g.db.cursor()
        cur.execute(query % (self.content, self.created_at, self.entry_id))
        self.id = cur.lastrowid
        flask.g.db.commit()

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Comment()
            item.id = row[0]
            item.content = row[1]
            item.created_at = row[2]
            item.entry_id = row[3]
            items.append(item)
        return items
