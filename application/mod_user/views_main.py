# -*- coding: utf-8 -*-

import flask
import json

from application import app
from application.mod_api.controllers_entries import api_get_entries
from application.mod_core.models_entry import Entry
from application.mod_core.models_hashtag import Hashtag
from presentable_object import PresentableEntry, PresentablePopularHashtag
from application.utils.pagination_services import Pagination

@app.route('/', methods=['GET'], defaults={'page_number': 1})
@app.route('/page/<int:page_number>', methods=['GET'])
def main(page_number):
    return _load_page_with_entries(title=u'Najnowsze',
                                   page_number=page_number)

@app.route('/top', methods=['GET'], defaults={'page_number': 1})
@app.route('/top/page/<int:page_number>', methods=['GET'])
def main_top(page_number):
    return _load_page_with_entries(title=u'Top plusowane',
                                   order_by="votes_up desc",
                                   page_number=page_number)

def _load_page_with_entries(title=None, page_number=None, order_by=None):
    items_per_page = app.config['ITEMS_PER_PAGE']
    response, status = api_get_entries(order_by=order_by,
                                       per_page=items_per_page,
                                       page_number=page_number)
    response_json = json.loads(response.data)

    p_entries = list()
    for entry_json in response_json["entries"]:
        entry = Entry.from_json(entry_json)
        p_entries.append(PresentableEntry(entry))

    if not p_entries and page_number != 1:
        flask.abort(404)

    hashtags = Hashtag.get_most_popular(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in hashtags]

    entries_count = Entry.get_count_all_approved()
    pagination = Pagination(page_number, items_per_page, entries_count)
    return flask.render_template('user/main.html', title=title,
                                  p_entries=p_entries,
                                  p_popular_hashtags=p_popular_hashtags,
                                  pagination=pagination)
