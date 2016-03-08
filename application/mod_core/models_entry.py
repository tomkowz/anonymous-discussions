import flask

class Entry:

    def __init__(self):
        self.id = None
        self.content = None
        self.created_at = None
        self.approved = None

    # DTO
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'approved': self.approved
        }

    @staticmethod
    def from_json(json):
        entry = Entry()
        entry.id = json.get('id')
        entry.content = json.get('content')
        entry.created_at = json.get('created_at')
        entry.approved = json.get('approved')
        return entry

    # DAO
    @staticmethod
    def get_all():
        query = 'select * \
                 from entries \
                 order by id desc'
        cur = flask.g.db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return Entry.parse_rows(rows)

    @staticmethod
    def get_all_approved(approved):
        query = 'select * \
                 from entries \
                 where approved = %s \
                 order by id desc'
        cur = flask.g.db.cursor()
        cur.execute(query % (approved))
        rows = cur.fetchall()
        return Entry.parse_rows(rows)

    @staticmethod
    def get_all_waiting_to_aprove():
        query = 'select * \
                 from entries \
                 where approved is null \
                 order by id desc'
        cur = flask.g.db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return Entry.parse_rows(rows)

    @staticmethod
    def get_with_id(entry_id):
        query = 'select * \
                 from entries \
                 where id = %s'
        cur = flask.g.db.cursor()
        cur.execute(query % (entry_id))
        rows = cur.fetchall()
        result = Entry.parse_rows(rows)
        if len(result) == 1:
            return result[0]
        else:
            return None

    @staticmethod
    def get_with_hashtag(value):
        query = 'select * \
                 from entries \
                 where content like \'%s\' and approved = 1 \
                 order by id desc'
        cur = flask.g.db.cursor()
        cur.execute(query % ('%#{}%'.format(value)))
        rows = cur.fetchall()
        return Entry.parse_rows(rows)

    def save(self):
        mysql_created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')

        cur = flask.g.db.cursor()
        if self.id is None:
            query = 'insert into entries (content, created_at) values (\'%s\', \'%s\')'
            cur.execute(query % (self.content, mysql_created_at))
            self.id = cur.lastrowid
        else:
            query = 'update entries \
                     set content = \'%s\', created_at = \'%s\', approved = %s \
                     where id = %s'
            cur.execute(query % (self.content, mysql_created_at, self.approved, self.id))
        flask.g.db.commit()

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Entry()
            item.id = row[0]
            item.content = row[1]
            item.created_at = row[2]
            item.approved = row[3]
            items.append(item)
        return items
