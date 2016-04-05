import flask, datetime
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
        updated_at=None,
        deleted=0,
        deleted_reason=None,
        cur_user_is_author=False,
        cur_user_vote=None,
        cur_user_follow=False,
        comments_count=0):

            self.id = id
            self.content = content
            self.created_at = created_at
            self.approved = bool(approved)
            self.op_token = op_token
            self.votes_up = int(votes_up)
            self.votes_down = int(votes_down)
            self.updated_at = updated_at
            self.deleted = deleted
            self.deleted_reason = deleted_reason

            # Transient
            self.cur_user_is_author = bool(cur_user_is_author)
            self.cur_user_vote = cur_user_vote
            self.cur_user_follow = bool(cur_user_follow)
            self.comments_count = int(comments_count)


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
            'updated_at': entry.updated_at,
            'deleted': entry.deleted,
            'deleted_reason': entry.deleted_reason,
            'cur_user_is_author': entry.cur_user_is_author,
            'cur_user_vote': entry.cur_user_vote,
            'cur_user_follow': entry.cur_user_follow,
            'comments_count': entry.comments_count
        }


    @staticmethod
    def from_json(json):
        return Entry(id=json.get('id'),
            content=json.get('content'),
            created_at=json.get('created_at'),
            approved=json.get('approved'),
            votes_up=json.get('votes_up'),
            votes_down=json.get('votes_down'),
            updated_at=json.get('updated_at'),
            deleted=json.get('deleted'),
            deleted_reason=json.get('deleted_reason'),
            cur_user_is_author=json.get('cur_user_is_author'),
            cur_user_vote=json.get('cur_user_vote'),
            cur_user_follow=json.get('cur_user_follow'),
            comments_count=json.get('comments_count'))


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
                approved=row[3],
                votes_up=row[4],
                votes_down=row[5]))
        return items


    @staticmethod
    def get_entries(cur_user_token, order_by, per_page=20, page=0):
        if order_by is None:
            order_by = 'id desc'
        query = "{} where e.approved = 1 order by {} limit {} offset {}"\
            .format(EntryDAO._get_entry_query(), order_by, per_page, page * per_page)
        params = EntryDAO._get_entry_query_default_params(cur_user_token)
        rows = SQLCursor.perform_fetch(query, params)
        return EntryDAO._parse_rows(rows)


    @staticmethod
    def get_entries_with_hashtag(hashtag, cur_user_token, order_by, per_page=20, page=0):
        if order_by is None:
            order_by = 'id desc'
        query = "{} where e.approved = 1 and e.content like '%s' order by {} limit {} offset {}"\
            .format(EntryDAO._get_entry_query(), order_by, per_page, page * per_page)
        params = EntryDAO._get_entry_query_default_params(cur_user_token) + ('%#{}%'.format(hashtag), )
        rows = SQLCursor.perform_fetch(query, params)
        return EntryDAO._parse_rows(rows)


    @staticmethod
    def get_entry(entry_id, cur_user_token):
        query = "{} where e.approved = 1 and e.id = '%s'".format(EntryDAO._get_entry_query())
        params = EntryDAO._get_entry_query_default_params(cur_user_token) + (entry_id, )
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return EntryDAO._parse_rows(rows)[0]


    @staticmethod
    def get_op_token_for_entry(entry_id):
        query = "select e.op_token from entries e \
            where e.approved = 1 and e.id = '%s'"
        params = (entry_id, )
        rows = SQLCursor.perform_fetch(query, params)
        row = rows[0]
        return row[0]


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
    def save(content, approved, op_token):
        query = "insert into entries \
            (content, approved, op_token) \
            values ('%s', '%s', '%s')"

        params = (content, approved, op_token)
        cur = SQLCursor.perform(query, params)
        return cur.lastrowid


    @staticmethod
    def vote_up(entry_id):
        query = "update entries \
            set votes_up = (votes_up + 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def vote_down(entry_id):
        query = "update entries \
            set votes_down = (votes_down + 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def decrease_votes_up(entry_id):
        query = "update entries \
            set votes_up = (votes_up - 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def decrease_votes_down(entry_id):
        query = "update entries \
            set votes_down = (votes_down - 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def _get_entry_query(): # REMEMBER to pass user_token 3x
        return """select e.id, e.content, e.created_at, e.approved, e.votes_up, \
            e.votes_down, e.updated_at, e.deleted, e.deleted_reason, \
            if(e.op_token = '%s', true, false) as cur_user_is_author,
            if(tvc.user_token = '%s' and tvc.object_type = 'entry', tvc.value, null) as cur_user_vote,
            if(fe.user_token = '%s', true, false) as cur_user_follow,
            (select count(*) from comments c where e.id = c.entry_id) as comments_count
            from entries e
            left join tokens_votes_cache tvc
            on e.id = tvc.object_id and tvc.user_token ='%s'
            left join followed_entries fe
            on e.id = fe.entry_id and fe.user_token = '%s'"""


    @staticmethod
    def _get_entry_query_default_params(user_token):
        return (user_token, user_token, user_token, user_token, user_token)

    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(Entry(id=row[0],
                content=row[1],
                created_at=row[2],
                approved=row[3],
                votes_up=row[4],
                votes_down=row[5],
                updated_at=row[6],
                deleted=row[7],
                deleted_reason=row[8],
                cur_user_is_author=row[9],
                cur_user_vote=row[10],
                cur_user_follow=row[11],
                comments_count=row[12]))
        return items
