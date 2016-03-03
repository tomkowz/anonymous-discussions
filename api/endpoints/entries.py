import flask

from api import app

from api.dao.entry_dao import EntryDAO

@app.route('/api/entries', methods=['GET'])
def entries_get_all():
    print EntryDAO.get_all()
    return flask.jsonify(), 200

@app.route('/api/entries', methods=['POST'])
def entries_insert():
    pass
