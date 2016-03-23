import flask

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment

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
