import flask, json
from application import app
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_followed_entries import FollowedEntriesItem, FollowedEntriesDAO
from application.mod_api.views_entries import api_get_entry

from application.mod_api.utils_params import \
    _is_user_op_token_param_valid, \
    _is_int_id_param_valid, \
    _create_invalid_param_error_message

@app.route('/api/entries/<int:entry_id>/follow', methods=['GET'])
def api_follow_entry(entry_id=None, user_token=None):

    result = _get_params_or_error(entry_id=entry_id, user_token=user_token)
    if result["success"] is False:
        return result["value"]

    entry_id, user_token, entry = result["value"]
    print result["value"]
    # Do not follow already followed entry
    if entry.cur_user_follow is False:
        FollowedEntriesDAO.follow_entry(entry_id=entry_id, user_token=user_token)

    entry = EntryDAO.get_entry(entry_id=entry_id, cur_user_token=user_token)
    return flask.jsonify({'entry': entry.to_json()}), 200

@app.route('/api/entries/<int:entry_id>/unfollow', methods=['GET'])
def api_unfollow_entry(entry_id=None, user_token=None):
    result = _get_params_or_error(entry_id=entry_id, user_token=user_token)
    if result["success"] is False:
        return result["value"]

    entry_id, user_token, entry = result["value"]
    # Do not follow already followed entry
    if entry.cur_user_follow is True:
        FollowedEntriesDAO.unfollow_entry(entry_id=entry_id, user_token=user_token)

    entry = EntryDAO.get_entry(entry_id=entry_id, cur_user_token=user_token)
    return flask.jsonify({'entry': entry.to_json()}), 200


@app.route('/api/entries/<int:entry_id>/toggle_follow', methods=['GET'])
def api_toggle_follow_entry(entry_id=None, user_token=None):
    result = _get_params_or_error(entry_id=entry_id, user_token=user_token)
    if result["success"] is False:
        return result["value"]

    entry_id, user_token, entry = result["value"]
    # Do not follow already followed entry
    if entry.cur_user_follow is True:
        FollowedEntriesDAO.unfollow_entry(entry_id=entry_id, user_token=user_token)
    else:
        FollowedEntriesDAO.follow_entry(entry_id=entry_id, user_token=user_token)

    entry = EntryDAO.get_entry(entry_id=entry_id, cur_user_token=user_token)
    return flask.jsonify({'entry': entry.to_json()}), 200

def _get_params_or_error(entry_id=None, user_token=None):
    result = {"success": False, "value": None}
    # Get params
    if entry_id is None:
        entry_id = flask.request.args.get('entry_id', None, type=int)

    if user_token is None:
        user_token = flask.request.args.get('user_token', None, type=str)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'entry_id': _is_int_id_param_valid(entry_id),
        'user_token': _is_user_op_token_param_valid(user_token)
    })
    if err_msg is not None:
        result["value"] = err_msg
        return result

    # Check whether entry exist
    response, status = api_get_entry(entry_id=entry_id, user_op_token=user_token)
    if status != 200:
        result["value"] = flask.jsonify({'error': 'Wpis nie istnieje'}), 400
        return result

    response_json = json.loads(response.data)
    entry = Entry.from_json(response_json['entry'])

    result["success"] = True
    result["value"] = entry_id, user_token, entry
    return result
