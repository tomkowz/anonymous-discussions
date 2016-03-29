import os, sys
import flask
from flask.ext.mysqldb import MySQL
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

    ITEMS_PER_PAGE = 15
))

# Configure MySQL
mysql = MySQL(app)

# Configure Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits = []
)


@limiter.request_filter
def ip_whitelist():
    return flask.request.remote_addr == "127.0.0.1"

# Do imports
from application.utils import db_app

from application.mod_api import \
    views_comments, \
    views_entries, \
    views_followed_entries, \
    views_popular_hashtags, \
    views_recommended_hashtags, \
    views_tokens, \
    views_user_notifications, \
    views_vote

from application.mod_web import \
    views_common, \
    views_entries, \
    views_hashtag, \
    views_main, \
    views_token, \
    views_user_notifications


# error handling
@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('errors/404.html'), 404


@app.errorhandler(429)
def to_many_requests(e):
    return flask.render_template('errors/429.html'), 429


@app.errorhandler(500)
def internal_server_error(e):
    return flask.render_template('errors/500.html'), 500
