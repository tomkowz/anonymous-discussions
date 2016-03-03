import flask

from api import app

from api.dao.entry_dao import EntryDAO
from api.dto.entry_dto import EntryDTO

@app.route('/api/entries', methods=['GET'])
def entries_get_all():
    entries = list()
    for entry in EntryDAO.get_all():
        entries.append(EntryDTO.to_json(entry))
    return flask.jsonify({'entries': entries}), 200

@app.route('/api/entries', methods=['POST'])
def entries_insert():
    json = flask.request.get_json()
    if json is not None:
        entry = EntryDTO.from_json(json)
        EntryDAO.insert(entry)
        return flask.jsonify({'entry': EntryDTO.to_json(entry)}), 201
    return flask.jsonify(), 400
