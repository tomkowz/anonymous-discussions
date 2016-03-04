# -*- coding: utf-8 -*-

import flask

from api import app
from api.dao.entry_dao import EntryDAO
from api.front.entry_view_model import EntryViewModel

@app.route('/hashtag/<value>', methods=['GET'])
def show_entries_for_hashtag(value):
    if len(value) == 0:
        return flask.redirect(flask.url_for('main'))

    entries = EntryDAO.get_with_hashtag(value)
    entry_view_models = list()
    for entry in entries:
        entry_view_models.append(EntryViewModel(entry))

    return flask.render_template('show_entries.html',
                                 title=u'#{}'.format(value),
                                 entries=entry_view_models)
