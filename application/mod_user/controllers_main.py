# -*- coding: utf-8 -*-

import flask

from application import app
from application.mod_core.models_entry import Entry
from presentable_object import PresentableEntry
from application.utils.pagination_services import Pagination

@app.route('/', methods=['GET'], defaults={'page_number': 1})
@app.route('/page/<int:page_number>', methods=['GET'])
def main(page_number):
    items_per_page = app.config['ITEMS_PER_PAGE']
    entries = Entry.get_all_approved(True, limit=items_per_page, offset=page_number - 1)
    p_entries = [PresentableEntry(x) for x in entries]

    if not p_entries and page_number != 1:
        flask.abort(404)

    entries_count = Entry.get_count_all_approved()
    return flask.render_template('user/main.html',
                                  title=u'Najnowsze',
                                  p_entries=p_entries,
                                  pagination=Pagination(page_number, items_per_page, entries_count))
