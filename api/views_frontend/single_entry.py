# -*- coding: utf-8 -*-

import flask

from api import app
from api.models.entry import Entry
from api.views_frontend.entry_view_model import EntryViewModel

@app.route('/entry/<id>', methods=['GET'])
def show_entry(id):
    entry = Entry.get_with_id(id)
    if entry is not None:
        entry_to_display = EntryViewModel(entry)
        return flask.render_template('single_entry.html', title='', entries=[entry_to_display])
    return flask.render_template('show_entries.html')
