import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

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
            'created_at': r"{}".format(self.created_at),
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
                              .limit(limit).offset(offset)

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
    def votes_with_id(comment_id):
        query_b = SQLBuilder().select('votes_up, votes_down', 'comments') \
                              .where("id = '%s'")

        params = (comment_id, )
        _, rows = SQLExecute().perform_fetch(query_b, params)
        if len(rows) == 1:
            row = rows[0]
            return row[0], row[1] # up, down
        else:
            return 0, 0

    @staticmethod
    def parse_rows(rows):
        items = list()
        for row in rows:
            item = Comment()
            item.id = row[0]
            item.content = row[1]
            item.created_at = r"{}".format(row[2])
            item.entry_id = row[3]
            items.append(item)
        return items
