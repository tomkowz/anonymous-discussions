import flask
import sqlite3

from api import app

@app.before_request
def before():
    flask.g.db = sqlite3.connect(app.config['DATABASE'])

@app.teardown_request
def teardown(exception):
    db = getattr(flask.g, 'db', None)
    if db is not None:
        db.close()
