# -*- coding: utf-8 -*-

import flask
from api import app
from api.dao.entry_dao import EntryDAO
from api.front.entry_view_model import EntryViewModel

@app.route('/', methods=['GET'])
def main():
    entries = EntryDAO.get_all()
    entry_view_models = list()
    for entry in entries:
        entry_view_models.append(EntryViewModel(entry))

    return flask.render_template('show_entries.html', title=u'Główna', entries=entry_view_models)
