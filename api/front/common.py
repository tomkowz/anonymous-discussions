# -*- coding: utf-8 -*-

import flask

from api import app
from api.dao.entry_dao import EntryDAO
from api.front.entry_view_model import EntryViewModel
from api.helpers.insert_entry_coordinator import InsertEntryCoordinator

@app.route('/', methods=['GET'])
def main():
    entries = EntryDAO.get_all()
    entry_view_models = list()
    for entry in entries:
        entry_view_models.append(EntryViewModel(entry))

    return flask.render_template('show_entries.html', title=u'Główna', entries=entry_view_models)

@app.route('/add', methods=['GET'])
def add():
    return flask.render_template('add.html', title=u'Nowy wpis', content='')

@app.route('/add', methods=['POST'])
def add_post():
    content = flask.request.form['content']
    min_len = 10
    if len(content) > min_len:
        entry = InsertEntryCoordinator.insert_entry({'content': content})
        if entry is not None:
            return flask.redirect(flask.url_for('main'))
        else:
            error = u'Nie udało się dodać wpisu. Spróbuj ponownie.'
    else:
        error = u'Wpis jest zbyt krótki (min. {} znaków).'.format(min_len)

    return flask.render_template('add.html', title=u'Nowy wpis', content=content, error=error)
