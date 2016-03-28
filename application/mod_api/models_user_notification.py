import flask

from application.mod_api.utils_sql import SQLCursor


class UserNotification:

    def __init__(self,
        id=None,
        user_token=None,
        content=None,
        created_at=None,
        object_id=None,
        object_type=None,
        active=None):

            self.id = id
            self.user_token = user_token
            self.content = content
            self.created_at = created_at
            self.object_id = object_id
            self.object_type = object_type
            self.active = active


    def to_json(self):
        return UserNotificationDTO.to_json(self)


    @staticmethod
    def from_json(json):
        return UserNotificationDTO.from_json(json)


class UserNotificationDTO:

    @staticmethod
    def to_json(un):
        return {
            'id': un.id,
            'user_token': un.user_token,
            'content': un.content,
            'created_at': r"{}".format(un.created_at),
            'object_id': un.object_id,
            'object_type': un.object_type,
            'active': un.active
        }


    @staticmethod
    def from_json(json):
        return UserNotification(id=json.get('id'),
            user_token=json.get('user_token'),
            content=json.get('content'),
            created_at=json.get('created_at'),
            object_id=json.get('object_id'),
            object_type=json.get('object_type'),
            active=bool(json.get('active')))


class UserNotificationDAO:

    @staticmethod
    def get_notifications(user_token):
        query = "select * from user_notifications \
            where user_token = '%s' order by id desc"
        params = (user_token, )
        rows = SQLCursor.perform_fetch(query, params)
        return UserNotificationDAO._parse_rows(rows)


    @staticmethod
    def get_notification(notification_id):
        query = "select * from user_notifications \
            where id = '%s'"
        params = (notification_id, )
        rows = SQLCursor.perform_fetch(query, params)
        if len(rows) == 0:
            return None

        return UserNotificationDAO._parse_rows(rows)[0]


    @staticmethod
    def dismiss_notification(notification_id):
        query = "update user_notifications \
            set active = 0 \
            where id = '%s'"
        params = (notification_id, )
        SQLCursor.perform(query, params)


    @staticmethod
    def save(user_token, content, created_at, object_id, object_type):
        query = "insert into user_notifications \
            (user_token, content, created_at, object_id, object_type) \
            values ('%s', '%s', '%s', '%s', '%s')"

        mysql_created_at = created_at.strftime('%Y-%m-%d %H:%M:%S')
        params = (user_token, content, mysql_created_at, object_id, object_type)
        SQLCursor.perform(query, params)


    @staticmethod
    def get_active_notifications_count(user_token):
        query = "select count(*) from user_notifications \
            where user_token = '%s' and active = 1"
        params = (user_token, )
        rows = SQLCursor.perform_fetch(query, params)
        row = rows[0]
        return row[0]


    @staticmethod
    def _parse_rows(rows):
        items = list()
        for row in rows:
            items.append(UserNotification(id=row[0],
                user_token=row[1],
                content=row[2],
                created_at=row[3],
                object_id=row[4],
                object_type=row[5],
                active=bool(row[6])))
        return items
