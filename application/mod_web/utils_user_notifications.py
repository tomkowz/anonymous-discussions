import flask, json
from application.mod_api.views_user_notifications import \
    api_get_active_user_notifications_count


def utils_get_user_notifications_count(user_token):
    response, status = api_get_active_user_notifications_count(user_token=user_token)
    user_notifications_count = 0
    if status == 200:
        response_json = json.loads(response.data)
        user_notifications_count = int(response_json['active_count'])
    return user_notifications_count
