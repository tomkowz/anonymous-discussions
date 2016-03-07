import os
import flask
from flask.ext.mysqldb import MySQL
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Configure app
app = flask.Flask(__name__)

app.config.update(dict(
    MYSQL_HOST='mysql3.zenbox.pl',
    MYSQL_USER='szulc_root',
    MYSQL_PASSWORD='LnYZk9KfWsXQ4f',
    MYSQL_DB='szulc_spowiedzwszafie',
    MYSQL_PORT=3306,

    DEBUG=True,
    SECRET_KEY='fe88a3d8-7fa1-46d3-a595-6eb0772501fc'
))

# Configure MySQL
mysql = MySQL(app)

from application.helpers import db_app_helper
from application.views_rest import entries
from application.views_frontend import main, add_entry, single_entry, faq
from application.views_frontend import login
