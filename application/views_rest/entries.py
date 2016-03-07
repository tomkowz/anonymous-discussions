import datetime
import flask

from application import app
from application.models.entry import Entry

@app.route('/api/entries', methods=['GET'])
def entries_get_all():
    entries = list()
    for entry in Entry.get_all():
        entries.append(entry.to_json())
    return flask.jsonify({'entries': entries}), 200

@app.route('/api/entries/', methods=['POST'])
def entries_insert():
    json = flask.request.get_json()
    content = json.get('content', None)
    if content is not None:
        entry = Entry()
        entry.content = content
        entry.created_at = datetime.datetime.utcnow()
        entry.save()

        return flask.jsonify({'entry': entry.to_json()}), 201

    return flask.jsonify(), 400
