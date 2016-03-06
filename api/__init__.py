import os
import sqlite3
import flask

app = flask.Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'resources/db.db'),
    DEBUG=True,
    SECRET_KEY='asdc-48ds-djsc-bbkd'
))

from api.helpers import db_app_helper
from api.views_rest import entries
from api.views_frontend import main, add_entry, single_entry, faq
