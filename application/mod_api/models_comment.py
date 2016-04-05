import flask, datetime
from application.mod_api.utils_sql import SQLCursor


class Comment:

    def __init__(self,
        id=None,
        content=None,
        created_at=None,
        entry_id=None,
        op_token=None,
        votes_up=0,
        votes_down=0,
        order=0,
        updated_at=None,
        deleted=0,
        deleted_reason=None,
        entry_author_is_comment_author=False,
        cur_user_is_author=False,
        cur_user_vote=None):

            self.id = id
            self.content = content
            self.created_at = created_at
            self.entry_id = entry_id
            self.votes_up = votes_up
            self.votes_down = votes_down
            self.order = order
            self.op_token = op_token
            self.updated_at = updated_at
            self.deleted = deleted
            self.deleted_reason = deleted_reason

            # Transient
            self.entry_author_is_comment_author = bool(entry_author_is_comment_author)
            self.cur_user_is_author = bool(cur_user_is_author)
            self.cur_user_vote = cur_user_vote


    def to_json(self):
        return CommentDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return CommentDTO.from_json(json)

class CommentDTO:

    @staticmethod
    def to_json(comment):
        return {
            'id': comment.id,
            'content': comment.content,
            'created_at': r"{}".format(comment.created_at),
            'entry_id': comment.entry_id,
            'votes_up': comment.votes_up,
            'votes_down': comment.votes_down,
            'order': comment.order,
            'updated_at': comment.updated_at,
            'deleted': comment.deleted,
            'deleted_reason': comment.deleted_reason,

            'entry_author_is_comment_author': bool(comment.entry_author_is_comment_author),
            'cur_user_is_author': bool(comment.cur_user_is_author),
            'cur_user_vote': comment.cur_user_vote
        }


    @staticmethod
    def from_json(json):
        return Comment(id=json.get('id'),
            content=json.get('content'),
            created_at=json.get('created_at'),
            entry_id=json.get('entry_id'),
            votes_up=json.get('votes_up'),
            votes_down=json.get('votes_down'),
            order=json.get('order'),
            updated_at=json.get('updated_at'),
            deleted=json.get('deleted'),
            deleted_reason=json.get('deleted_reason'),
            entry_author_is_comment_author=json.get('entry_author_is_comment_author'),
            cur_user_is_author=json.get('cur_user_is_author'),
            cur_user_vote=json.get('cur_user_vote'))


class CommentDAO:

    @staticmethod
    def get_all():
        query = 'select c.id, c.content, c.created_at, c.votes_up, c.votes_down from comments c'
        params = tuple()
        rows = SQLCursor.perform_fetch(query, params)

        items = list()
        for row in rows:
            items.append(Comment(id=row[0],
                content=row[1],
                created_at=row[2],
                votes_up=row[3],
                votes_down=row[4]))
        return items


    @staticmethod
    def get_comment(comment_id, cur_user_token):
        query = "{} where id = '%s'".format(CommentDAO._get_comment_query())
        params = (cur_user_token, cur_user_token, cur_user_token, comment_id)
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return CommentDAO._parse_rows(rows)[0]


    @staticmethod
    def save(content, entry_id, cur_user_token):
        query = "insert into comments \
            (content, entry_id, `order`, op_token) \
            values ('%s', '%s', (select count(*) from comments c where c.entry_id = %s) + 1, '%s')"
        params = (content, entry_id, entry_id, cur_user_token)
        cur = SQLCursor.perform(query, params)
        return cur.lastrowid


    @staticmethod
    def vote_up(comment_id):
        query = "update comments \
            set votes_up = (votes_up + 1) \
            where id = '%s'"
        params = (comment_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def vote_down(comment_id):
        query = "update comments \
            set votes_down = (votes_down + 1) \
            where id = '%s'"
        params = (comment_id, )
        SQLCursor.perform(query, params)

    @staticmethod
    def decrease_votes_up(entry_id):
        query = "update comments \
            set votes_up = (votes_up - 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)

    @staticmethod
    def decrease_votes_down(entry_id):
        query = "update comments \
            set votes_down = (votes_down - 1) \
            where id = '%s'"
        params = (entry_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def get_comments_count(entry_id):
        query = "select count(*) from comments where entry_id = '%s'"
        params = (entry_id, )
        rows = SQLCursor.perform_fetch(query, params)
        row = rows[0]
        return row[0]


    @staticmethod
    def get_comments_for_entry(entry_id,
        cur_user_token,
        order,
        per_page=20,
        page=0):
        # order asc or desc
        query = "{} where entry_id = '%s' \
            order by id %s \
            limit {} \
            offset {}".format(CommentDAO._get_comment_query(),
                per_page,
                page * per_page)
        params = (cur_user_token, cur_user_token, cur_user_token, entry_id, order)
        rows = SQLCursor.perform_fetch(query, params)
        return CommentDAO._parse_rows(rows)


    @staticmethod
    def get_comments_for_entry_count(entry_id):
        query = "select count(*) from comments \
            where entry_id = '%s'"
        params = (entry_id, )
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return 0

        row = rows[0]
        return row[0]

    @staticmethod
    def _get_comment_query(): # REMEMBER to pass cur_user_token 3x
        return "select c.id, c.content, c.created_at, c.entry_id, c.votes_up, \
            c.votes_down, c.order, c.updated_at, c.deleted, c.deleted_reason, \
            if(c.op_token = (select e.op_token \
                from entries e where e.id = c.entry_id), true, false) \
                as entry_author_is_comment_author, \
            if(c.op_token = '%s', true, false) \
                as cur_user_is_author, \
            if(tvc.user_token = '%s' and \
                tvc.object_type = 'comment', tvc.value, null) as cur_user_vote \
            from comments c \
            left join tokens_votes_cache as tvc \
            on c.id = tvc.object_id and tvc.user_token = '%s'"


    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(Comment(id=row[0],
                content=row[1],
                created_at=row[2],
                entry_id=row[3],
                votes_up=row[4],
                votes_down=row[5],
                order=row[6],
                updated_at=row[7],
                deleted=row[8],
                deleted_reason=row[9],
                entry_author_is_comment_author=row[10],
                cur_user_is_author=row[11],
                cur_user_vote=row[12]
                ))
        return items
