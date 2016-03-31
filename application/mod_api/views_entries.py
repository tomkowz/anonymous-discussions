# -*- coding: utf-8 -*-
import datetime, flask, json, re

from application import app, limiter
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_comment import Comment, CommentDAO
from application.mod_api.models_hashtag import Hashtag, HashtagDAO
from application.mod_api.models_user_notification import UserNotification, UserNotificationDAO

from application.utils.notification_services import EmailNotifier
from application.mod_api.utils_hashtags import HashtagsUtils
from application.mod_api.views_tokens import _api_check_if_token_exist

from application.mod_api.utils_params import \
    _is_hashtag_param_valid, \
    _is_order_by_param_valid, \
    _is_user_op_token_param_valid, \
    _is_per_page_param_valid, \
    _is_page_param_valid, \
    _is_entry_id_param_valid, \
    _is_comments_order_param_valid, \
    _is_content_param_valid, \
    _create_invalid_param_error_message, \
    _get_value_for_key_if_none, \
    _is_entry_content_valid, \
    _is_comment_content_valid, \
    _cleanup_content


def _update_hashtags_with_content(content):
    hashtags = HashtagsUtils.get_hashtags_from_text(content)
    for hashtag_str in hashtags:
        hashtag = HashtagDAO.get_hashtag(hashtag_str)
        if hashtag is None:
            HashtagDAO.save(hashtag_str)
        else:
            HashtagDAO.increment_count(hashtag_str)


@app.route('/api/entries', methods=['GET'])
def api_get_entries(hashtag=None,
    order_by=None,
    user_op_token=None,
    per_page=None,
    page=None):
    """Return entries.

    Parameters:
    hashtag -- if hashtag is specified it will return only items with specific
        hashtag. It'll behave the same like visiting /h/blstream page for
        #blstream hashtag.
    order_by -- Specifies whether entries should be sorted in a specific way.
      By default it is sorted by id desc, but you can specifify by votes_up desc.
    user_op_token -- This is op_token that users uses. If it is specified then
      every entry that have the same op_token will have op_user = True,
      otherwise False.
    per_page -- Specifies how many items will be returned by one page.
    page -- Specifies number of a page with results.
    """

    # Get params
    if hashtag is None:
        hashtag = flask.request.args.get('hashtag', None, type=str)

    if order_by is None:
        order_by = flask.request.args.get('order_by', None, type=str)

    if user_op_token is None:
        user_op_token = flask.request.args.get('user_op_token', None, type=str)

    if per_page is None:
        per_page = flask.request.args.get('per_page', 20, type=int)

    if page is None:
        page = flask.request.args.get('page', 1, type=int)

    # Validate params
    err_msg = _create_invalid_param_error_message({
        'hashtag': _is_hashtag_param_valid(hashtag),
        'order_by': _is_order_by_param_valid(order_by),
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
        'per_page': _is_per_page_param_valid(per_page),
        'page': _is_page_param_valid(page)
    })
    if err_msg is not None:
        return err_msg

    # Get entries
    page -= 1
    if hashtag is None:
        entries = EntryDAO.get_entries(cur_user_token=user_op_token,
            order_by=order_by,
            per_page=per_page,
            page=page)
    else:
        entries = EntryDAO.get_entries_with_hashtag(hashtag=hashtag,
            cur_user_token=user_op_token,
            order_by=order_by,
            per_page=per_page,
            page=page)

    return flask.jsonify({'entries': [e.to_json() for e in entries]}), 200


@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def api_get_entry(entry_id, user_op_token=None):
    """Return single entry

    Parameters:
    entry_id -- Id of an entry.
    user_op_token -- This is op_token that users uses. If it is specified then
      every entry that have the same op_token will have op_user = True,
      otherwise False.
    """
    # Get params
    if user_op_token is None:
        user_op_token = flask.request.args.get('user_op_token', None, type=str)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
        'entry_id': _is_entry_id_param_valid(entry_id)
    })
    if err_msg is not None:
        return err_msg

    # Prepare result
    entry = EntryDAO.get_entry(entry_id=entry_id, cur_user_token=user_op_token)
    if entry is None:
        return flask.jsonify({'error': 'Wpis nie istnieje.'}), 400

    return flask.jsonify({'entry': entry.to_json()}), 200


@app.route('/api/entries', methods=['POST'])
@limiter.limit("2/minute")
@limiter.limit("6/hour")
@limiter.limit("20/day")
def api_post_entry(content=None, user_op_token=None):
    # Get params
    content = _get_value_for_key_if_none(value=content, key='content', type=str)
    user_op_token = _get_value_for_key_if_none(value=user_op_token, key='user_op_token', type=str)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'content': _is_content_param_valid(content),
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
    })
    if err_msg is not None:
        return err_msg

    # Check token existence
    token_check_response, status = _api_check_if_token_exist(user_op_token)
    if status == 200:
        if json.loads(token_check_response.data)['exists'] is False:
            error = "Niepoprawny token. Wygeneruj nowy i spróbuj ponownie"
            return flask.jsonify({'error': error}), 400
    else:
        return flask.jsonify({'error': "Błąd podczas dodawania wpisu"}), 400

    content_valid, error = _is_entry_content_valid(content)
    if content_valid is False:
        return flask.jsonify({'error': error}), 400

    content = _cleanup_content(content).decode('utf-8')
    content = HashtagsUtils.convert_hashtags_to_lowercase(content)
    entry_id = EntryDAO.save(content=content,
        created_at=datetime.datetime.utcnow(),
        approved=1,
        op_token=user_op_token)

    if entry_id is None:
        return flask.jsonify({'error': 'Nie udało się dodać wpisu.'}), 400

    _update_hashtags_with_content(content)
    EmailNotifier.notify_new_entry(flask.url_for('single_entry', entry_id=entry_id))
    entry = EntryDAO.get_entry(entry_id=entry_id, cur_user_token=user_op_token)
    return flask.jsonify({'entry': entry.to_json()}), 201
