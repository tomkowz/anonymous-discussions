import flask

from application import app
from application.mod_api.models_user_settings import \
    UserSettings, UserSettingsDAO

from application.mod_api.utils_params import \
    _create_invalid_param_error_message, \
    _is_user_op_token_param_valid, \
    _get_value_for_key_if_none


@app.route('/api/user_settings', methods=['GET'])
def api_get_user_settings(user_token=None):
    user_token = _get_value_for_key_if_none(value=user_token, key='user_token', type=str)

    err_msg = _create_invalid_param_error_message({
        'user_token': _is_user_op_token_param_valid(user_token)
    })
    if err_msg is not None:
        return err_msg

    user_settings = UserSettingsDAO.get_settings(token=user_token)
    if user_settings is None:
        UserSettingsDAO.create_settings(token=user_token)
        user_settings = UserSettingsDAO.get_settings(token=user_token)

    return flask.jsonify({'user_settings': user_settings.to_json()}), 200


@app.route('/api/user_settings', methods=['PUT'])
def update_settings(user_token=None, mark_my_posts=None):
    user_token = _get_value_for_key_if_none(value=user_token, key='user_token', type=str)
    mark_my_posts = _get_value_for_key_if_none(value=mark_my_posts, key='mark_my_posts', type=bool)

    err_msg = _create_invalid_param_error_message({
        'user_token': _is_user_op_token_param_valid(user_token)
    })
    if err_msg is not None:
        return err_msg

    UserSettingsDAO.update_settings(token=user_token, mark_my_posts=mark_my_posts)
    user_settings = UserSettingsDAO.get_settings(token=user_token).to_json()
    return flask.jsonify({'user_settings': user_settings}), 200
