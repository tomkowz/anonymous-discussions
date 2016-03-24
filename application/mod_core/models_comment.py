import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

class Comment:

    def __init__(self, id=None, content=None, created_at=None, entry_id=None, votes_up=0, votes_down=0):
        self.id = id
        self.content = content
        self.created_at = created_at
        self.entry_id = entry_id
        self.votes_up = votes_up
        self.votes_down = votes_down

    # DTO
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': r"{}".format(self.created_at),
            'entry_id': self.entry_id,
            'votes_up': self.votes_up,
            'votes_down': self.votes_down
        }

    @staticmethod
    def from_json(json):
        obj = Comment()
        obj.id = json.get('id', None)
        obj.content = json.get('content', None)
        obj.created_at = json.get('created_at', None)
        obj.entry_id = json.get('entry_id', None)
        obj.votes_up = json.get('votes_up', 0)
        obj.votes_down = json.get('votes_down', 0)

    @staticmethod
    def get_all():
        query_b = SQLBuilder().select('*', 'comments')
        _, rows = SQLExecute.perform_fetch(query_b, None)
        return Comment.parse_rows(rows)

    @staticmethod
    def get_comments_count_with_entry_id(entry_id):
        query_b = SQLBuilder().select('count(*)', 'comments') \
                              .where("entry_id = '%s'")
        _, rows = SQLExecute().perform_fetch(query_b, (entry_id))
        return rows[0][0]

    @staticmethod
    def get_comments_with_entry_id(entry_id, order, limit=None, offset=None):
        query_b = SQLBuilder().select('*', 'comments') \
                              .where("entry_id = '%s'") \
                              .order("id %s") \
                              .limit(limit).offset(offset * limit)

        _, rows = SQLExecute().perform_fetch(query_b, (entry_id, order))
        return Comment.parse_rows(rows)

    def save(self):
        query_b = SQLBuilder().insert_into('comments') \
                              .using_mapping('content, created_at, entry_id') \
                              .and_values_format("'%s', '%s', '%s'")

        cur = SQLExecute().perform(query_b, (self.content, self.created_at, self.entry_id),
                                   commit=True)
        self.id = cur.lastrowid

    @staticmethod
    def vote(entry_id, value):
        if value == 'up':
            Comment._vote_up(entry_id)
        elif value == 'down':
            Comment._vote_down(entry_id)

    @staticmethod
    def _vote_up(comment_id):
        query_b = SQLBuilder().update('comments') \
                              .set([('votes_up', "votes_up + 1")]) \
                              .where("id = '%s'")
        params = (comment_id, )
        SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def _vote_down(comment_id):
        query_b = SQLBuilder().update('comments') \
                              .set([('votes_down', "votes_down + 1")]) \
                              .where("id = '%s'")
        params = (comment_id, )
        SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Comment(id=row[0], content=row[1], created_at=r"{}".format(row[2]),
                           entry_id=row[3], votes_up=row[4], votes_down=row[5])
            items.append(item)
        return items
