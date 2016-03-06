import os
import sqlite3
import flask
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = flask.Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '../db.db'),
    DEBUG=True,
    SECRET_KEY='asdc-48ds-djsc-bbkd'
))

from application.helpers import db_app_helper
from application.views_rest import entries
from application.views_frontend import main, add_entry, single_entry, faq
from application.views_frontend import login
