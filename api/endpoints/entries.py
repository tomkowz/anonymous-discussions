import datetime
import flask

from api import app
from api.model.entry import Entry
from api.helpers.insert_entry_coordinator import InsertEntryCoordinator

@app.route('/api/entries', methods=['GET'])
def entries_get_all():
    entries = list()
    for entry in Entry.get_all():
        entries.append(entry.to_json())
    return flask.jsonify({'entries': entries}), 200

@app.route('/api/entries/', methods=['POST'])
def entries_insert():
    json = flask.request.get_json()
    if json is not None and \
       json.get('content') is not None:
        entry = InsertEntryCoordinator.insert_entry(json)
        return flask.jsonify({'entry': entry.to_json()}), 201

    return flask.jsonify(), 400
