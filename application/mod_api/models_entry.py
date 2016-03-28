import flask
from application.mod_api.utils_sql import SQLCursor


class Entry:

    def __init__(self,
        id=None,
        content=None,
        created_at=None,
        approved=None,
        op_token=None,
        votes_up=0,
        votes_down=0,
        cur_user_is_author=False,
        cur_user_vote=None):

            self.id = id
            self.content = content
            self.created_at = created_at
            self.approved = approved
            self.op_token = op_token
            self.votes_up = votes_up
            self.votes_down = votes_down

            # Transient
            self.cur_user_is_author = cur_user_is_author
            self.cur_user_vote = cur_user_vote


    def to_json(self):
        return EntryDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return EntryDTO.from_json(json)


class EntryDTO:

    @staticmethod
    def to_json(entry):
        return {
            'id': entry.id,
            'content': entry.content,
            'created_at': r"{}".format(entry.created_at),
            'approved': entry.approved,
            'votes_up': entry.votes_up,
            'votes_down': entry.votes_down,
            'cur_user_is_author': entry.cur_user_is_author,
            'cur_user_vote': entry.cur_user_vote
        }


    @staticmethod
    def from_json(json):
        return Entry(id=json.get('id'),
            content=json.get('content'),
            created_at=json.get('created_at'),
            approved=bool(json.get('approved')),
            votes_up=json.get('votes_up'),
            votes_down=json.get('votes_down'),
            cur_user_is_author=json.get('cur_user_is_author'),
            cur_user_vote=json.get('cur_user_vote'))


class EntryDAO:

    @staticmethod
    def get_all():
        query = "select e.id, e.content, e.created_at, \
            e.approved, e.votes_up, e.votes_down \
            from entries e"
        params = tuple()
        rows = SQLCursor.perform_fetch(query, params)

        items = list()
        for row in rows:
            items.append(Entry(id=row[0],
                content=row[1],
                created_at=row[2],
                approved=bool(row[3]),
                votes_up=row[4],
                votes_down=row[5]))
        return items


    @staticmethod
    def get_entries(cur_user_token, order_by, per_page=20, page_number=0):
        if order_by is None:
            order_by = 'id desc'
        query = "{} where e.approved = 1 order by {} limit {} offset {}"\
            .format(EntryDAO._get_entry_query(), order_by, per_page, page_number * per_page)
        params = (cur_user_token, cur_user_token)
        rows = SQLCursor.perform_fetch(query, params)
        return EntryDAO._parse_rows(rows)


    @staticmethod
    def get_entries_with_hashtag(hashtag, cur_user_token, order_by, per_page=20, page_number=0):
        if order_by is None:
            order_by = 'id desc'
        query = "{} where e.approved = 1 and e.content like '%s' order by {} limit {} offset {}"\
            .format(EntryDAO._get_entry_query(), order_by, per_page, page_number * per_page)
        params = (cur_user_token, cur_user_token, '%#{}%'.format(hashtag))
        rows = SQLCursor.perform_fetch(query, params)
        return EntryDAO._parse_rows(rows)


    @staticmethod
    def get_entry(entry_id, cur_user_token):
        query = "{} where e.approved = 1 and e.id = '%s'".format(EntryDAO._get_entry_query())
        params = (cur_user_token, cur_user_token, entry_id)
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return EntryDAO._parse_rows(rows)[0]


    @staticmethod
    def get_entries_count():
        query = "select count(*) from entries e where e.approved = 1"
        params = tuple()
        rows = SQLCursor.perform_fetch(query, params)
        row = rows[0]
        return row[0]


    @staticmethod
    def get_entries_with_hashtag_count(hashtag):
        query = "select count(*) from entries e where e.approved = 1 and e.content like '%s'"
        params = ('%#{}%'.format(hashtag))
        rows = SQLCursor.perform_fetch(query, params)
        row = rows[0]
        return row[0]


    @staticmethod
    def save(content, created_at, approved, op_token):
        query = "insert into entries \
            (content, created_at, approved, op_token) \
            values ('%s', '%s', '%s', '%s')"

        mysql_created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
        params = (content, mysql_created_at, approved, op_token)
        cur = SQLCursor.perform(query, params)
        return cur.lastrowid


    @staticmethod
    def vote_up(entry_id):
        query = "update entries set votes_up = (votes_up + 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def vote_down(entry_id):
        query = "update entries set votes_down = (votes_down + 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def _get_entry_query():
        return "select e.id, e.content, e.created_at, e.approved, e.votes_up, e.votes_down, \
            if(e.op_token = '%s', true, false) as cur_user_is_author, \
            if(tvc.user_token = '%s' and tvc.object_type = 'entry', tvc.value, null) as cur_user_vote \
            from entries e \
            left join tokens_votes_cache tvc \
            on e.id = tvc.object_id"


    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(Entry(id=row[0],
                content=row[1],
                created_at=row[2],
                approved=bool(row[3]),
                votes_up=row[4],
                votes_down=row[5],
                cur_user_is_author=bool(row[6]),
                cur_user_vote=row[7]))
        return items
