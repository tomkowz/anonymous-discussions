# -*- coding: utf-8 -*-

import flask

from api import app
from api.model.entry import Entry
from api.frontend.entry_view_model import EntryViewModel

@app.route('/', methods=['GET'])
def main():
    entries = Entry.get_all()
    entry_view_models = list()
    for entry in entries:
        entry_view_models.append(EntryViewModel(entry))

    return flask.render_template('show_entries.html',
                                 title=u'Szafa',
                                 entries=entry_view_models)
