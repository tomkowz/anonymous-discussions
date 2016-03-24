# -*- coding: utf-8 -*-

import flask
import json

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_hashtag import Hashtag
from presentable_object import PresentableEntry, PresentablePopularHashtag
from application.utils.pagination_services import Pagination
from application.mod_api.controllers_entries import api_get_entries

@app.route('/h', methods=['GET'], defaults={'value': '', 'page_number': 1})
@app.route('/h/<string:value>', methods=['GET'], defaults={'page_number': 1})
@app.route('/h/<string:value>/page/<int:page_number>', methods=['GET'])
def show_entries_for_hashtag(value, page_number):
    if len(value) == 0:
        return flask.redirect(flask.url_for('main'))

    items_per_page = app.config['ITEMS_PER_PAGE']
    response, status = api_get_entries(hashtag=value, per_page=items_per_page, page_number=page_number)
    response_json = json.loads(response.data)

    p_entries = list()
    for entry_json in response_json["entries"]:
        entry = Entry.from_json(entry_json)
        p_entries.append(PresentableEntry(entry))

    if not p_entries and page_number != 1:
        flask.abort(404)

    hashtags = Hashtag.get_most_popular(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in hashtags]

    entries_count = Entry.get_count_all_with_hashtag(value)
    pagination = Pagination(page_number, items_per_page, entries_count)
    return flask.render_template('user/main.html', title='#' + value.lower(),
                                  p_entries=p_entries,
                                  p_popular_hashtags=p_popular_hashtags,
                                  pagination=pagination)
