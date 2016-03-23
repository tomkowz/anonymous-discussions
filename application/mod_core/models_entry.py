import flask

from application.utils.sql_services import SQLBuilder, SQLExecute

class Entry:

    def __init__(self, content=None, created_at=None, approved=None):
        self.id = None
        self.content = content
        self.created_at = created_at
        self.approved = approved

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
    def get_count_all_approved():
        query_b = SQLBuilder().select('count(*)', 'entries') \
                              .where('approved = 1')
        _, rows = SQLExecute.perform_fetch(query_b)
        return rows[0][0]

    @staticmethod
    def get_all_approved(approved, limit=None, offset=None):
        query_b = SQLBuilder().select('*', 'entries') \
                              .where('approved = %s') \
                              .order('id desc') \
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
                              .where('id = %s')

        _, rows = SQLExecute().perform_fetch(query_b, (entry_id))

        result = Entry.parse_rows(rows)
        return result[0] if len(result) > 0 else None

    @staticmethod
    def get_with_hashtag(value, limit=None, offset=None):
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
                                  .using_mapping('content, created_at, approved') \
                                  .and_values_format("'%s', '%s', '%s'")

            params = (self.content, mysql_created_at, self.approved)
            cur = SQLExecute().perform(query_b, params, commit=True)
            self.id = cur.lastrowid

        else:
            query_b = SQLBuilder().update('entries') \
                                  .set([('content', "'%s'"),
                                        ('created_at', "'%s'"),
                                        ('approved', "'%s'")]) \
                                  .where('id = %s')

            params = (self.content, mysql_created_at, self.approved, self.id)
            SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def vote(entry_id, value):
        query_b = SQLBuilder().insert_into('entry_votes') \
                              .using_mapping('entry_id, value') \
                              .and_values_format("'%s', '%s'")

        params = (entry_id, value)
        SQLExecute().perform(query_b, params, commit=True)

    @staticmethod
    def votes_with_id(entry_id):
        query_up = SQLBuilder().select("count(value)", 'entry_votes') \
                               .where("value = 'up' and entry_id='{}'".format(entry_id)).get_query()

        query_down = SQLBuilder().select("count(value)", 'entry_votes') \
                                 .where("value = 'down' and entry_id='{}'".format(entry_id)).get_query()

        select_q = "coalesce(({}), 0) as 'up', coalesce(({}), 0) as 'down'".format(query_up, query_down)
        query_b = SQLBuilder().select(select_q, 'entry_votes') \
                              .where("entry_id = '%s'") \
                              .group_by('entry_id')

        params = (entry_id, )
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
            item = Entry()
            item.id = row[0]
            item.content = row[1]
            item.created_at = row[2]
            item.approved = row[3]
            items.append(item)
        return items
