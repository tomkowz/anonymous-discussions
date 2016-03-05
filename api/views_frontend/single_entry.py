# -*- coding: utf-8 -*-

import flask

from api import app
from api.models.entry import Entry
from api.views_frontend.presentable_entry import PresentableEntry

@app.route('/entry/<id>', methods=['GET'])
def show_entry(id):
    entry = Entry.get_with_id(id)
    if entry is not None:
        presentable = PresentableEntry(entry)
        return flask.render_template('single_entry.html', title='', entries=[presentable])
    return flask.render_template('show_entries.html')
