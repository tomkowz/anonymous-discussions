# -*- coding: utf-8 -*-
import datetime, flask, json

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from application.mod_core.models_hashtag import Hashtag

from application.utils.sanitize_services import Sanitize
from application.utils.notification_services import EmailNotifier
from application.utils.text_decorator import TextDecorator

def _is_hashtag_param_valid(hashtag):
    if hashtag is not None and \
        Sanitize.is_valid_input(hashtag) is False:
        return False
    return True

def _is_order_by_param_valid(order_by):
    if order_by is not None and order_by != "votes_up desc":
        return False
    return True

def _is_user_op_token_param_valid(user_op_token):
    if user_op_token is not None and \
        Sanitize.is_valid_input(user_op_token) is False:
        return False
    return True

def _is_per_page_param_valid(per_page):
    if per_page is None or per_page == 0:
        return False
    return True

def _is_page_number_param_valid(page_number):
    if page_number is None or page_number == 0:
        return False
    return True

def _is_entry_id_param_valid(entry_id):
    return True if entry_id is not None else False

def _invalid_param_error(param):
    return "Niepoprawna wartość parametru {}".format(param)


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
    checks = {
        'hashtag': _is_hashtag_param_valid(hashtag),
        'order_by': _is_order_by_param_valid(order_by),
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
        'per_page': _is_per_page_param_valid(per_page),
        'page_number': _is_page_number_param_valid(page_number)
    }

    for (k, is_valid) in checks.items():
        if is_valid is False:
            error = _invalid_param_error(k)
            return flask.jsonify({'error:': error}), 400

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
    checks = {
        'user_op_token': _is_user_op_token_param_valid(user_op_token),
        'entry_id': _is_entry_id_param_valid(entry_id)
    }

    for (k, is_valid) in checks.items():
        if is_valid is False:
            error = _invalid_param_error(k)
            return flask.jsonify({'error:': error}), 400

    # Prepare result
    entry = Entry.get_with_id(entry_id)
    if entry is None:
        return flask.jsonify({'error': 'Wpis nie istnieje.'}), 400

    if entry.op_token is not None:
        entry.op_user = entry.op_token == user_op_token

    entry_json = entry.to_json()
    del entry_json['op_token']

    return flask.jsonify({'entry': entry_json}), 200

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
    if user_op_token is None:
        user_op_token = flask.request.args.get('user_op_token', None, type=str)

    if user_op_token is not None and \
        Sanitize.is_valid_input(user_op_token) is False:
        return flask.jsonify({'error': "Niepoprawna wartość parametru 'user_op_token'"}), 400

    if per_page is None and page_number is None:
        per_page = flask.request.args.get('per_page', 20, type=int)
        page_number = flask.request.args.get('page_number', 1, type=int)

    if comments_order is None or Sanitize.is_valid_input(comments_order) is False:
        return flask.jsonify({'error': 'Niepoprawne dane.'}), 400

    _, status = api_get_single_entry(entry_id)
    if status != 200:
        return flask.jsonify({'error': 'Wpis nie istnieje.'}), 400

    comments = Comment.get_comments_with_entry_id(entry_id=entry_id, order=comments_order,
                                                  limit=per_page, offset=page_number - 1)

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
def api_post_entry(content=None, op_token=None):
    content = _get_value_for_key_if_none(value=content, key='content', type=str)
    op_token = _get_value_for_key_if_none(value=op_token, key='op_token', type=str)

    if content is None:
        return flask.jsonify({'error': "Pole 'content' jest wymagane"}), 400

    content_valid, error = _is_entry_content_valid(content)
    if content_valid is False:
        return flask.jsonify({'error': error}), 400

    if op_token is not None:
        if Sanitize.is_valid_input(op_token) is False or \
            " " in op_token:
            return flask.jsonify({'error': 'Token jest niepoprawny'}), 400

    entry = Entry(content=content,
                  created_at=datetime.datetime.utcnow(),
                  approved=1,
                  op_token=op_token)
    entry.save()

    if entry.id is None:
        return flask.jsonify({'error': 'Nie udało się dodać wpisu.'}), 400

    # EmailNotifier.notify_about_new_post() # Temporary

    _update_hashtags_with_content(content)

    return flask.jsonify({'entry': entry.to_json()}), 201

@app.route('/api/entries/<int:entry_id>/comments', methods=['POST'])
def api_post_comment_for_entry(entry_id=None, content=None, op_token=None):
    content = _get_value_for_key_if_none(value=content, key='content', type=str)
    op_token = _get_value_for_key_if_none(value=op_token, key='op_token', type=str)

    if content is None:
        return flask.jsonify({'error': "Brak parametru 'content'."}), 400

    content_valid, error = _is_comment_content_valid(content)
    if content_valid is False:
        return flask.jsonify({'error': error}), 400

    if op_token is not None:
        if Sanitize.is_valid_input(op_token) is False or \
            " " in op_token:
            return flask.jsonify({'error': 'Token jest niepoprawny'}), 400

    comment = Comment(content=content, created_at=datetime.datetime.utcnow(), entry_id=entry_id, op_token=op_token)
    comment.save()

    if comment.id is None:
        return flask.jsonify({'error': 'Nie udało się dodać komentarza.'}), 400

    _update_hashtags_with_content(content)

    return flask.jsonify({'comment': comment.to_json()}), 200

def _get_value_for_key_if_none(value, key, type):
    if value is None:
        value = flask.request.args.get(key, None, type=type)

    if value is None:
        value = flask.request.form.get(key, None, type=type)

    if value is None:
        try:
            value = json.loads(flask.request.data)[key]
        except:
            pass

    return value

def _update_hashtags_with_content(content):
    hashtags = TextDecorator.get_hashtags_from_text(content)
    for hashtag_str in hashtags:
        hashtag = Hashtag.get_with_name(hashtag_str)
        if hashtag is None:
            hashtag = Hashtag(name=hashtag_str)
            hashtag.save()
        else:
            hashtag.increment_count()

def _is_entry_content_valid(content):
    char_len = (5, 500)
    content_valid, invalid_symbol = Sanitize.is_valid_input(content)
    if content_valid == False:
        return False, 'Wpis zawiera niedozwolone elementy: {}'.format(invalid_symbol)
    elif len(content) < char_len[0]:
        return False, 'Wpis jest zbyt krótki.'
    elif len(content) > char_len[1]:
        return False, 'Wpis jest zbyt długi (max. {} znaków).'.format(max_len)

    return True, None

def _is_comment_content_valid(content):
    char_len = (2, 500)

    content_valid, invalid_symbol = Sanitize.is_valid_input(content)
    if content_valid == False:
        return False, 'Komentarz zawiera niedozwolone elementy: {}'.format(invalid_symbol)
    elif len(content) < char_len[0]:
        return False, 'Komentarz jest zbyt krótki.'
    elif len(content) > char_len[1]:
        return False, 'Komentarz jest zbyt długi (max. {} znaków).'.format(max_len)

    return True, None
