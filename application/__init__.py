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

    DEBUG=False,
    SECRET_KEY='fe88a3d8-7fa1-46d3-a595-6eb0772501fc',

    ITEMS_PER_PAGE = 20
))

# Configure MySQL
mysql = MySQL(app)

# Do imports
from application.utils import db_app

from application.mod_api import controllers_vote, controllers_entries, controllers_hashtags

from application.mod_user import views_main, views_hashtag, views_entries, views_common

from application.mod_admin_panel import controllers_login, controllers_approve

# error handling
@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return flask.render_template('500.html'), 500
