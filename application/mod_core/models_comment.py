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
    def vote(comment_id, value):
        query_b = SQLBuilder().insert_into('comment_votes') \
                              .using_mapping('comment_id, value') \
                              .and_values_format("'%s', '%s'")

        params = (comment_id, value)
        SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def votes_with_id(comment_id):
        query_up = SQLBuilder().select("count(value)", 'comment_votes') \
                               .where("value = 'up' and comment_id='{}'".format(comment_id)).get_query()

        query_down = SQLBuilder().select("count(value)", 'comment_votes') \
                                 .where("value = 'down' and comment_id={}".format(comment_id)).get_query()

        select_q = "coalesce(({}), 0) as 'up', coalesce(({}), 0) as 'down'".format(query_up, query_down)
        query_b = SQLBuilder().select(select_q, 'comment_votes') \
                              .where("comment_id = '%s'") \
                              .group_by('comment_id')

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
            item.created_at = row[2]
            item.entry_id = row[3]
            items.append(item)
        return items
