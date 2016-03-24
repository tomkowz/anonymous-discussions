# -*- coding: utf-8 -*-
import datetime, flask, json

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from application.mod_core.models_hashtag import Hashtag

from application.utils.sanitize_services import Sanitize
from application.utils.notification_services import EmailNotifier
from application.utils.text_decorator import TextDecorator

@app.route('/api/entries', methods=['GET'])
def api_get_entries(hashtag=None, order_by=None, per_page=None, page_number=None):
    if hashtag is None:
        hashtag = flask.request.args.get('hashtag', None, type=str)

    if order_by is None:
        order_by = flask.request.args.get('order_by', None, type=str)

    if per_page is None:
        per_page = flask.request.args.get('per_page', 20, type=int)

    if page_number is None:
        page_number = flask.request.args.get('page_number', 1, type=int)

    if hashtag is not None and \
        Sanitize.is_valid_input(hashtag) is False:
        return flask.jsonify({'error': "Niepoprawna wartość parametru 'hashtag'."}), 400

    if order_by is not None and order_by != "votes_up desc":
        return flask.jsonify({'error': "Niepoprawna wartość parametru 'sorted_by'."}), 400

    if page_number == 0:
        return flask.jsonify({'error': 'Pierwsza strona = 1'}), 400

    if hashtag is None:
        entries = Entry.get_all_approved(True, order_by=order_by, limit=per_page, offset=page_number - 1)
    else:
        entries = Entry.get_with_hashtag(value=hashtag, order_by=order_by, limit=per_page, offset=page_number - 1)

    result = list()
    for e in entries:
        result.append(e.to_json())

    return flask.jsonify({'entries': result}), 200

@app.route('/api/entries/<int:entry_id>', methods=['GET'])
def api_get_single_entry(entry_id):
    if entry_id is None:
        return flask.jsonify({'error': 'Brak entry_id.'}), 400

    entry = Entry.get_with_id(entry_id)
    if entry is None:
        return flask.jsonify({'error': 'Wpis nie istnieje.'}), 400

    return flask.jsonify({'entry': entry.to_json()}), 200

@app.route('/api/entries/<int:entry_id>/comments', methods=['GET'])
def api_get_comments_for_entry(entry_id, comments_order='desc', per_page=None, page_number=None):
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

    result = [c.to_json() for c in comments]
    return flask.jsonify({'comments': result}), 200

@app.route('/api/entries/<int:entry_id>/comments', methods=['POST'])
def api_post_comment_for_entry(entry_id=None, content=None):
    if content is None:
        content = flask.request.args.get('content', None, type=str)

    if content is None:
        try:
            content = json.loads(flask.request.data)['content']
        except:
            pass

    if content is None:
        return flask.jsonify({'error': 'Brak content.'}), 400

    content_valid, error = _is_comment_content_valid(content)
    if content_valid is False:
        return flask.jsonify({'error': error}), 400

    comment = Comment(content=content, created_at=datetime.datetime.utcnow(), entry_id=entry_id)
    comment.save()

    if comment.id is None:
        return flask.jsonify({'error': 'Nie udało się dodać komentarza.'}), 400

    _update_hashtags_with_content(content)

    return flask.jsonify({'comment': comment.to_json()}), 200

@app.route('/api/entries', methods=['POST'])
def api_post_entry(content=None):
    # Request from client
    if content is None and flask.request.data is not None:
        try:
            content = json.loads(flask.request.data).get('content', None)
        except:
            pass

    # Request from form
    if content is None and flask.request.form is not None:
        content = flask.request.form['content']

    if content is None:
        return flask.jsonify({'error': "Pole 'content' jest wymagane"}), 400

    content_valid, error = _is_entry_content_valid(content)
    if content_valid is False:
        return flask.jsonify({'error': error}), 400

    entry = Entry(content=content, created_at=datetime.datetime.utcnow(), approved=1)
    entry.save()

    if entry.id is None:
        return flask.jsonify({'error': 'Nie udało się dodać wpisu.'}), 400

    # EmailNotifier.notify_about_new_post() # Temporary

    _update_hashtags_with_content(content)

    return flask.jsonify({'entry': entry.to_json()}), 201

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
