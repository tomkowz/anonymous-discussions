# -*- coding: utf-8 -*-

import flask
import json

from application import app
from application.mod_api.controllers_entries import api_entries
from application.mod_core.models_entry import Entry
from presentable_object import PresentableEntry
from application.utils.pagination_services import Pagination

@app.route('/', methods=['GET'], defaults={'page_number': 1})
@app.route('/page/<int:page_number>', methods=['GET'])
def main(page_number):
    items_per_page = app.config['ITEMS_PER_PAGE']
    response, status = api_entries(per_page=items_per_page, page_number=page_number)
    response_json = json.loads(response.data)

    p_entries = list()
    for entry_json in response_json["entries"]:
        entry = Entry.from_json(entry_json)
        p_entries.append(PresentableEntry(entry))

    if not p_entries and page_number != 1:
        flask.abort(404)

    entries_count = Entry.get_count_all_approved()
    pagination = Pagination(page_number, items_per_page, entries_count)
    return flask.render_template('user/main.html', title=u'Najnowsze',
                                  p_entries=p_entries, pagination=pagination)
