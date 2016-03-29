# -*- coding: utf-8 -*-
import flask, json

from application import app
from application.mod_api.models_user_notification import UserNotification
from application.mod_api.views_user_notifications import \
    api_get_active_user_notifications, \
    api_dismiss_all_user_notifications

from application.mod_web.presentable_object import PresentableUserNotification
from application.mod_web.utils_user_notifications import utils_get_user_notifications_count
@app.route('/powiadomienia', methods=['GET'])
def show_notifications():
    user_token = flask.request.cookies.get('op_token', None)
    response, status = api_get_active_user_notifications(user_token=user_token)

    user_notifications = list()
    if status == 200:
        response_json = json.loads(response.data)['notifications']
        for un_json in response_json:
            un = UserNotification.from_json(un_json)
            user_notifications.append(un)

    p_user_notifications = [PresentableUserNotification(un) for un in user_notifications]

    user_notifications_count = len(p_user_notifications)

    return flask.render_template('web/user_notifications.html',
        title='Powiadomienia',
        p_user_notifications=p_user_notifications,
        user_notifications_count=user_notifications_count)

@app.route('/powiadomienia/oznacz_wszystkie_jako_przeczytane', methods=['GET'])
def mark_all_notifications_as_read():
    user_token = flask.request.cookies.get('op_token', None)
    response, status = api_dismiss_all_user_notifications(user_token=user_token)
    return show_notifications()
