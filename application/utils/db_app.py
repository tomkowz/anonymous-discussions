import flask

from application import app, mysql


@app.before_request
def before():
    flask.g.db = mysql.connect


@app.teardown_request
def teardown(exception):
    db = getattr(flask.g, 'db', None)
    if db is not None:
        db.close()
