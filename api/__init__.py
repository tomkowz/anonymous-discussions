import os
import sqlite3
import flask

app = flask.Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'resources/db.db'),
    DEBUG=True
))

from api.helpers import db_app_helper
import api.model
from api.endpoints import entries
import api.dao
