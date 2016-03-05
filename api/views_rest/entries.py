import datetime
import flask

from api import app
from api.models.entry import Entry
from api.utils.date_utils import DateUtils

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
        entry.timestamp = DateUtils.timestamp_for_now()
        entry.save()

        return flask.jsonify({'entry': entry.to_json()}), 201

    return flask.jsonify(), 400
