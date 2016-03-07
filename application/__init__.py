import os
import flask
from flask.ext.mysqldb import MySQL
import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = flask.Flask(__name__)

app.config.update(dict(
    MYSQL_HOST='mysql3.zenbox.pl',
    MYSQL_USER='szulc_root',
    MYSQL_PASSWORD='LnYZk9KfWsXQ4f',
    MYSQL_DB='szulc_spowiedzwszafie',
    MYSQL_PORT=3306,

    DEBUG=True,
    SECRET_KEY='asdc-48ds-djsc-bbkd'
))

mysql = MySQL(app)

from application.helpers import db_app_helper
from application.views_rest import entries
from application.views_frontend import main, add_entry, single_entry, faq
from application.views_frontend import login
