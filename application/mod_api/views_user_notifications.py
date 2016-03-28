import flask

from application import app
from application.mod_api.models_user_notification import UserNotification, UserNotificationDAO
from application.mod_api.utils_params import \
    _create_invalid_param_error_message, \
    _is_user_op_token_param_valid, \
    _is_int_id_param_valid


@app.route('/api/user_notifications', methods=['GET'])
def api_get_user_notifications(user_token=None):
    # Get params
    if user_token is None:
        user_token = flask.request.args.get('user_token')

    # Check params
    err_msg = _create_invalid_param_error_message({
        'user_token': _is_user_op_token_param_valid(user_token)
    })
    if err_msg is not None:
        return err_msg

    # Get notifications
    notifications = UserNotificationDAO.get_notifications(user_token)
    return flask.jsonify({'notifications': [n.to_json() for n in notifications]}), 200


@app.route('/api/user_notifications/<int:id>/dismiss', methods=['GET'])
def api_dismiss_user_notification(id):
    # Get params
    err_msg = _create_invalid_param_error_message({
        'id': _is_int_id_param_valid(id)
    })
    if err_msg is not None:
        return err_msg

    UserNotificationDAO.dismiss_notification(notification_id=id)
    notification = UserNotificationDAO.get_notification(id)
    return flask.jsonify({'notification': notification.to_json()}), 200
