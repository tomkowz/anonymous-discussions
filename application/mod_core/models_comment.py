import flask

from application.utils.sql_helper import SQLBuilder, SQLExecute

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
        query = SQLBuilder().select('*', 'comments') \
                            .order('id desc').get_query()

        _, rows = SQLExecute().perform_fetch(query)
        return Comment.parse_rows(rows)

    @staticmethod
    def get_comments_count_with_entry_id(entry_id):
        query = SQLBuilder().select('count(*)', 'comments') \
                            .where("entry_id = '%s'").get_query()
        _, rows = SQLExecute().perform_fetch(query, (entry_id))
        return rows[0][0]

    @staticmethod
    def get_with_entry_id(entry_id, order):
        query = SQLBuilder().select('*', 'comments') \
                            .where("entry_id = '%s'") \
                            .order("id %s").get_query()

        _, rows = SQLExecute().perform_fetch(query, (entry_id, order))
        return Comment.parse_rows(rows)

    def save(self):
        query = SQLBuilder().insert_into('comments') \
                            .using_mapping('content, created_at, entry_id') \
                            .and_values_format("'%s', '%s', '%s'").get_query()

        cur = SQLExecute().perform(query, (self.content, self.created_at, self.entry_id),
                                      commit=True)
        self.id = cur.lastrowid

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
