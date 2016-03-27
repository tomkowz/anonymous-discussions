# -*- coding: utf-8 -*-
import datetime, flask, json, re

from application import app, limiter
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_comment import Comment
from application.mod_api.models_hashtag import Hashtag

from application.utils.notification_services import EmailNotifier
from application.utils.text_decorator import TextDecorator

from application.mod_api.views_tokens import _api_check_if_token_exist

from application.mod_api.utils_params import \
    _is_hashtag_param_valid, \
    _is_order_by_param_valid, \
    _is_user_op_token_param_valid, \
    _is_per_page_param_valid, \
    _is_page_number_param_valid, \
    _is_entry_id_param_valid, \
    _is_comments_order_param_valid, \
    _is_content_param_valid, \
    _create_invalid_param_error_message, \
    _get_value_for_key_if_none, \
    _is_entry_content_valid, \
    _is_comment_content_valid

def _update_hashtags_with_content(content):
    hashtags = TextDecorator.get_hashtags_from_text(content)
    for hashtag_str in hashtags:
        hashtag = Hashtag.get_with_name(hashtag_str)
        if hashtag is None:
            hashtag = Hashtag(name=hashtag_str)
            hashtag.save()
        else:
            hashtag.increment_count()

@app.route('/api/entries', methods=['GET'])
def api_get_entries(hashtag=None,
                    order_by=None,
                    user_op_token=None,
                    per_page=None,
                    page_number=None):
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
    page_number -- Specifies number of a page with results.
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

    if page_number is None:
        page_number = flask.request.args.get('page_number', 1, type=int)

    # Validate params
    err_msg = _create_invalid_param_error_message({
        'hashtag': _is_hashtag_param_valid(hashtag),
        'order_by': _is_order_by_param_valid(order_by),
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
        'per_page': _is_per_page_param_valid(per_page),
        'page_number': _is_page_number_param_valid(page_number)
    })
    if err_msg is not None:
        return err_msg

    # Get entries
    offset = page_number - 1
    if hashtag is None:
        entries = Entry.get_all_approved(approved=True,
                                         order_by=order_by,
                                         limit=per_page,
                                         offset=offset)
    else:
        entries = Entry.get_with_hashtag(value=hashtag,
                                         order_by=order_by,
                                         limit=per_page,
                                         offset=offset)

    # Prepare result
    result = list()
    for e in entries:
        if e.op_token is not None:
            e.op_user = e.op_token == user_op_token

        e_json = e.to_json()
        del e_json['op_token']
        result.append(e_json)

    return flask.jsonify({'entries': result}), 200

@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def api_get_single_entry(entry_id,
    user_op_token=None):
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

@app.route('/api/entries/<int:entry_id>/comments', methods=['GET'])
def api_get_comments_for_entry(entry_id,
                               comments_order='desc',
                               user_op_token=None,
                               per_page=None,
                               page_number=None):
    """Return comments for entry id

    Parameters:
    entry_id -- Id of entry.
    comments_order -- Specifies how comments are ordered. asc/desc.
    user_op_token -- This is op_token that users uses. If it is specified then
      every entry that have the same op_token will have op_user = True,
      otherwise False.
    per_page -- Specifies how many items will be returned by one page.
    page_number -- Specifies number of a page with results.
    """
    # Get params
    if user_op_token is None:
        user_op_token = flask.request.args.get('user_op_token', None, type=str)

    if per_page is None:
        per_page = flask.request.args.get('per_page', 20, type=int)

    if page_number is None:
        page_number = flask.request.args.get('page_number', 1, type=int)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
        'per_page': _is_per_page_param_valid(per_page),
        'page_number': _is_page_number_param_valid(page_number),
        'comments_order': _is_comments_order_param_valid(comments_order)
    })
    if err_msg is not None:
        return err_msg

    # Prepare results
    _, status = api_get_single_entry(entry_id)
    if status != 200:
        return flask.jsonify({'error': 'Wpis nie istnieje.'}), 400

    comments = Comment.get_comments_with_entry_id(entry_id=entry_id,
                                                  order=comments_order,
                                                  limit=per_page,
                                                  offset=page_number - 1)

    entry = Entry.get_with_id(entry_id)

    result = list()
    for c in comments:
        if c.op_token is not None:
            c.op_author = c.op_token == entry.op_token
            c.op_user = c.op_token == user_op_token

        c_json = c.to_json()
        del c_json['op_token']

        result.append(c_json)

    return flask.jsonify({'comments': result}), 200

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

    content = _cleanup_content(content)
    entry = Entry(content=content,
                  created_at=datetime.datetime.utcnow(),
                  approved=1,
                  op_token=user_op_token)
    entry.save()

    if entry.id is None:
        return flask.jsonify({'error': 'Nie udało się dodać wpisu.'}), 400

    _update_hashtags_with_content(content)

    EmailNotifier.notify_new_entry(flask.url_for('single_entry', entry_id=entry.id))

    return flask.jsonify({'entry': entry.to_json()}), 201

@app.route('/api/entries/<int:entry_id>/comments', methods=['POST'])
@limiter.limit("5/minute")
def api_post_comment(entry_id=None, content=None, user_op_token=None):
    # Get params
    content = _get_value_for_key_if_none(value=content, key='content', type=str)
    user_op_token = _get_value_for_key_if_none(value=user_op_token, key='user_op_token', type=str)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'entry_id': _is_entry_id_param_valid(entry_id),
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

    content = _cleanup_content(content)
    comment = Comment(content=content,
                      created_at=datetime.datetime.utcnow(),
                      entry_id=entry_id,
                      op_token=user_op_token)
    comment.save()

    if comment.id is None:
        return flask.jsonify({'error': "Błąd podczas dodawania komentarza"}), 400

    _update_hashtags_with_content(content)

    EmailNotifier.notify_new_comment(flask.url_for('single_entry', entry_id=entry_id))

    return flask.jsonify({'comment': comment.to_json()}), 200

def _cleanup_content(content):
    # Cleanup content before saving
    content = content.strip()
    content = re.sub(' +', ' ', content)
    content = re.sub('\t+', '\t', content)
    content = re.sub('(\r\n){3,}', '\r\n\r\n', content)
    return content
