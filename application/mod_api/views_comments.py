# -*- coding: utf-8 -*-
import datetime, flask, json, math

from application import app, limiter
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_comment import Comment, CommentDAO
from application.mod_api.models_hashtag import Hashtag, HashtagDAO

from application.utils.notification_services import EmailNotifier
from application.mod_api.utils_hashtags import HashtagsUtils
from application.mod_api.utils_user_notification_broadcaster import UserNotificationBroadcaster
from application.mod_api.views_tokens import _api_check_if_token_exist
from application.mod_api.views_entries import api_get_entry

from application.mod_api.utils_params import \
    _is_user_op_token_param_valid, \
    _is_per_page_param_valid, \
    _is_page_param_valid, \
    _is_comments_order_param_valid, \
    _is_content_param_valid, \
    _create_invalid_param_error_message, \
    _get_value_for_key_if_none, \
    _is_comment_content_valid, \
    _is_int_id_param_valid, \
    _cleanup_content


@app.route('/api/comments', methods=['GET'])
def api_get_comments_for_entry(entry_id=None,
    comments_order=None,
    user_op_token=None,
    per_page=None,
    page=None):
    """Return comments for entry id

    Parameters:
    entry_id -- Id of entry.
    comments_order -- Specifies how comments are ordered. asc/desc.
    user_op_token -- This is op_token that users uses. If it is specified then
      every entry that have the same op_token will have op_user = True,
      otherwise False.
    per_page -- Specifies how many items will be returned by one page.
    page -- Specifies number of a page with results.
    """
    # Get params
    if entry_id is None:
        entry_id = flask.request.args.get('entry_id', None, type=int)

    if user_op_token is None:
        user_op_token = flask.request.args.get('user_op_token', None, type=str)

    if per_page is None:
        per_page = flask.request.args.get('per_page', 20, type=int)

    if page is None:
        page = flask.request.args.get('page', 1, type=int)

    if comments_order is None:
        comments_order = flask.request.args.get('comments_order', 'desc', type=str)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'entry_id': _is_int_id_param_valid(entry_id),
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
        'per_page': _is_per_page_param_valid(per_page),
        'page': _is_page_param_valid(page),
        'comments_order': _is_comments_order_param_valid(comments_order)
    })
    if err_msg is not None:
        return err_msg

    # Prepare results
    response, status = api_get_entry(entry_id=entry_id, user_op_token=user_op_token)
    if status != 200:
        return flask.jsonify({'error': json.loads(response.data)['error']}), 400

    comments = CommentDAO.get_comments_for_entry(entry_id=entry_id,
        cur_user_token=user_op_token,
        order=comments_order,
        per_page=per_page,
        page=page-1)

    total_count = CommentDAO.get_comments_for_entry_count(entry_id)
    metadata = {
        'current_page': page,
        'per_page': per_page,
        'total_count': total_count,
        'last_page': int(math.ceil(total_count / float(per_page)))
    }

    return flask.jsonify({'comments': [c.to_json() for c in comments],
        '_metadata': metadata}), 200


@app.route('/api/comments', methods=['POST'])
@limiter.limit("5/minute")
def api_post_comment(entry_id=None, content=None, user_op_token=None):
    # Get params
    entry_id = _get_value_for_key_if_none(value=entry_id, key='entry_id', type=int)
    content = _get_value_for_key_if_none(value=content, key='content', type=str)
    user_op_token = _get_value_for_key_if_none(value=user_op_token, key='user_op_token', type=str)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'entry_id': _is_int_id_param_valid(entry_id),
        'content': _is_content_param_valid(content),
        'user_op_token': _is_user_op_token_param_valid(user_op_token)
    })
    if err_msg is not None:
        return err_msg

    content_valid, error = _is_comment_content_valid(content)
    if content_valid is False:
        return flask.jsonify({'error': error}), 400

    # Check token existence
    token_check_response, status = _api_check_if_token_exist(user_op_token)
    if status == 200:
        if json.loads(token_check_response.data)['exists'] is False:
            error = "Niepoprawny token. Wygeneruj nowy i spróbuj ponownie"
            return flask.jsonify({'error': error}), 400
    else:
        return flask.jsonify({'error': "Błąd podczas dodawania komentarza"}), 400

    content = _cleanup_content(content).decode('utf-8')
    content = HashtagsUtils.convert_hashtags_to_lowercase(content)
    comment_id = CommentDAO.save(content=content,
        entry_id=entry_id,
        cur_user_token=user_op_token)

    if comment_id is None:
        return flask.jsonify({'error': "Błąd podczas dodawania komentarza"}), 400

    # Create user notification if needed
    UserNotificationBroadcaster.post_notification_to_op_and_followers(entry_id=entry_id,
        user_token=user_op_token)
    UserNotificationBroadcaster.post_notification_to_mentions(entry_id=entry_id,
        comment_content=content)

    EmailNotifier.notify_new_comment(flask.url_for('single_entry', entry_id=entry_id))

    comment = CommentDAO.get_comment(comment_id=comment_id, cur_user_token=user_op_token)
    return flask.jsonify({'comment': comment.to_json()}), 200
