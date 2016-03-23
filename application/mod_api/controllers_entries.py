# -*- coding: utf-8 -*-
import datetime
import flask
import json

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from application.utils.sanitize_services import Sanitize
from application.utils.notification_services import EmailNotifier

@app.route('/api/entries', methods=['GET'])
def api_entries(per_page=None, page_number=None):
    if per_page is None and page_number is None:
        per_page = flask.request.args.get('per_page', 20, type=int)
        page_number = flask.request.args.get('page_number', 1, type=int)

    if page_number == 0:
        return flask.jsonify({'error': 'first page is 1.'}), 400

    entries = Entry.get_all_approved(True, limit=per_page, offset=page_number - 1)

    result = list()
    for e in entries:
        result.append(e.to_json())

    return flask.jsonify({'entries': result}), 200

@app.route('/api/entries', methods=['POST'])
def api_post_entry(content=None):
    if content is None and flask.request.data is not None:
        try:
            content = json.loads(flask.request.data).get('content', None)
        except:
            pass

    if content is None and flask.request.form is not None:
        content = flask.request.form['content']

    if content is None:
        return flask.jsonify({'error': "Pole 'content' jest wymagane"}), 400

    content_valid, error = _is_entry_content_valid(content)
    if content_valid is False:
        return flask.jsonify({'error': error}), 400

    entry = Entry(content=content, created_at=datetime.datetime.utcnow(), approved=1)
    entry.save()

    if entry is None:
        return flask.jsonify({'error': 'Nie udało się dodać wpisu.'}), 400

    # EmailNotifier.notify_about_new_post() # Temporary

    return flask.jsonify({'entry': entry.to_json()}), 201

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
