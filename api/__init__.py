import os
import sqlite3
import flask

app = flask.Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'resources/db.db'),
    DEBUG=True
))

import api.helpers
import api.model
import api.endpoints
import api.dao
