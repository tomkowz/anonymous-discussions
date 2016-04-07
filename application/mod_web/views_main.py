# -*- coding: utf-8 -*-

import flask, json

from application import app
from application.mod_api.views_entries import api_get_entries
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_web.presentable_object import PresentableEntry
from application.utils.pagination_services import Pagination

from application.mod_web.utils_display_on_web import UtilsDisplayOnWeb
from application.mod_web.views_user_settings import generate_token


@app.route('/', methods=['GET'], defaults={'page': 1})
@app.route('/strona/<int:page>', methods=['GET'])
def main(page):
    if flask.request.cookies.get('op_token', None) is None:
        return generate_token(redirect_to=flask.url_for('main'))

    return _load_page_with_entries(title=u'Najnowsze', page=page)


@app.route('/najlepsze', methods=['GET'], defaults={'page': 1})
@app.route('/najlepsze/strona/<int:page>', methods=['GET'])
def main_top(page):
    return _load_page_with_entries(title=u'Top plusowane',
                                   order_by="votes_up desc",
                                   page=page)


def _load_page_with_entries(title=None, page=None, order_by=None):
    user_token = flask.request.cookies.get('op_token')
    items_per_page = app.config['ITEMS_PER_PAGE']
    response, status = api_get_entries(order_by=order_by,
                                       per_page=items_per_page,
                                       user_op_token=user_token,
                                       page=page)
    response_json = json.loads(response.data)

    p_entries = list()
    for entry_json in response_json["entries"]:
        entry = Entry.from_json(entry_json)
        p_entries.append(PresentableEntry(entry))

    if not p_entries and page != 1:
        flask.abort(404)

    disp_web = UtilsDisplayOnWeb(user_token=user_token)
    entries_count = EntryDAO.get_entries_count()

    pagination = Pagination(page, items_per_page, entries_count)
    return flask.render_template('web/main.html', title=title,
                                  p_entries=p_entries,
                                  p_recommended_hashtags=disp_web.get_recommended_hashtags(),
                                  p_popular_hashtags=disp_web.get_popular_hashtags(),
                                  user_notifications_count=disp_web.get_user_notifications_count(),
                                  user_settings=disp_web.get_user_settings(),
                                  pagination=pagination)
