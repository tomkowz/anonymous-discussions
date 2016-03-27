import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

class Entry:

    def __init__(self, id=None, content=None, created_at=None, approved=None, votes_up=0, votes_down=0, op_token=None):
        self.id = id
        self.content = content
        self.created_at = created_at
        self.approved = approved
        self.votes_up = votes_up
        self.votes_down = votes_down
        self.op_token = op_token

        # Transient
        self.op_user = False

    # DTO
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': r"{}".format(self.created_at),
            'approved': self.approved,
            'votes_up': self.votes_up,
            'votes_down': self.votes_down,
            'op_token': self.op_token,

            'op_user': self.op_user
        }

    @staticmethod
    def from_json(json):
        entry = Entry()
        entry.id = json.get('id')
        entry.content = json.get('content')
        entry.created_at = json.get('created_at')
        entry.approved = json.get('approved')
        entry.votes_up = json.get('votes_up')
        entry.votes_down = json.get('votes_down')
        entry.op_token = json.get('op_token')

        entry.op_user = json.get('op_user')
        return entry

    # DAO
    @staticmethod
    def get_all():
        query_b = SQLBuilder().select('*', 'entries')
        _, rows = SQLExecute.perform_fetch(query_b, None)
        return Entry.parse_rows(rows)

    @staticmethod
    def get_count_all_approved():
        query_b = SQLBuilder().select('count(*)', 'entries') \
                              .where('approved = 1')

        _, rows = SQLExecute.perform_fetch(query_b)
        return rows[0][0]

    @staticmethod
    def get_all_approved(approved=True, limit=None, offset=None, order_by=None):
        if order_by is None:
            order_by = "id desc"

        query_b = SQLBuilder().select('*', 'entries') \
                              .where('approved = %s') \
                              .order(order_by) \
                              .limit(limit).offset(offset * limit)

        _, rows = SQLExecute().perform_fetch(query_b, (approved))
        return Entry.parse_rows(rows)

    @staticmethod
    def get_all_waiting_to_aprove():
        query_b = SQLBuilder().select('*', 'entries') \
                              .where('approved is null') \
                              .order('id desc')

        _, rows = SQLExecute().perform_fetch(query_b)
        return Entry.parse_rows(rows)

    @staticmethod
    def get_with_id(entry_id):
        query_b = SQLBuilder().select('*', 'entries') \
                              .where("id = %s")

        _, rows = SQLExecute().perform_fetch(query_b, (entry_id, ))

        result = Entry.parse_rows(rows)
        return result[0] if len(result) > 0 else None

    @staticmethod
    def get_with_hashtag(value, limit=None, offset=None, order_by=None):
        if order_by is None:
            order_by = "id desc"

        query_b = SQLBuilder().select('*', 'entries') \
                              .where("content like '%s' and approved = 1") \
                              .order('id desc') \
                              .limit(limit).offset(offset * limit)

        _, rows = SQLExecute().perform_fetch(query_b, ('%#{}%'.format(value)))
        return Entry.parse_rows(rows)

    @staticmethod
    def get_count_all_with_hashtag(value):
        query_b = SQLBuilder().select('count(*)', 'entries') \
                              .where("content like '%s' and approved = 1")
        _, rows = SQLExecute().perform_fetch(query_b, ('%#{}%'.format(value)))
        return rows[0][0]

    def save(self):
        mysql_created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')

        cur = flask.g.db.cursor()
        if self.id is None:
            query_b = SQLBuilder().insert_into('entries') \
                                  .using_mapping('content, created_at, approved, op_token') \
                                  .and_values_format("'%s', '%s', '%s', '%s'")

            params = (self.content, mysql_created_at, self.approved, self.op_token)
            cur = SQLExecute().perform(query_b, params, commit=True)
            self.id = cur.lastrowid

        else:
            query_b = SQLBuilder().update('entries') \
                                  .set([('content', "'%s'"),
                                        ('created_at', "'%s'"),
                                        ('approved', "'%s'"),
                                        ('op_token', "'%s'")]) \
                                  .where('id = %s')

            params = (self.content, mysql_created_at, self.approved, self.op_token, self.id)
            SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def vote(entry_id, value):
        if value == 'up':
            Entry._vote_up(entry_id)
        elif value == 'down':
            Entry._vote_down(entry_id)

    @staticmethod
    def _vote_up(entry_id):
        query_b = SQLBuilder().update('entries') \
                              .set([('votes_up', "votes_up + 1")]) \
                              .where("id = '%s'")
        params = (entry_id, )
        SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def _vote_down(entry_id):
        query_b = SQLBuilder().update('entries') \
                              .set([('votes_down', "votes_down + 1")]) \
                              .where("id = '%s'")
        params = (entry_id, )
        SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Entry(id=row[0],
                         content=row[1],
                         created_at=r"{}".format(row[2]),
                         approved=row[3],
                         votes_up=row[4],
                         votes_down=row[5],
                         op_token=row[6])
            items.append(item)
        return items
