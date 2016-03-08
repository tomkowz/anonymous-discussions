# -*- coding: utf-8 -*-

import flask

from application import app
from application.mod_core.models_entry import Entry
from presentable_object import PresentableEntry
from application.utils.sanitize_services import Sanitize
from application.utils.pagination_services import Pagination

@app.route('/hashtag', methods=['GET'], defaults={'value': '', 'page_number': 1})
@app.route('/hashtag/<string:value>', methods=['GET'], defaults={'page_number': 1})
@app.route('/hashtag/<string:value>/page/<int:page_number>', methods=['GET'])
def show_entries_for_hashtag(value, page_number):
    value_valid, _ = Sanitize.is_valid_input(value)
    if len(value) == 0 and value_valid == True:
        # Just fall back to '/'
        return flask.redirect(flask.url_for('main'))

    items_per_page = app.config['ITEMS_PER_PAGE']
    entries = Entry.get_with_hashtag(value, limit=items_per_page, offset=page_number - 1)
    p_entries = [PresentableEntry(x) for x in entries]

    if not p_entries and page_number != 1:
        flask.abort(404)

    entries_count = Entry.get_count_all_with_hashtag(value)
    return flask.render_template('user/main.html',
                                  title='#' + value.lower(),
                                  p_entries=p_entries,
                                  pagination=Pagination(page_number, items_per_page, entries_count))
