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

from application.utils import db_app

from application.mod_user import controllers_main, controllers_hashtag, \
    controllers_add_entry, controllers_single_entry, controllers_faq

from application.mod_admin_panel import controllers_login, controllers_approve
