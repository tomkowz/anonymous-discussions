# -*- coding: utf-8 -*-

import flask

from api import app
from api.models.entry import Entry
from api.views_frontend.presentable_entry import PresentableEntry

@app.route('/hashtag/<value>', methods=['GET'])
def show_entries_for_hashtag(value):
    if len(value) == 0:
        return flask.redirect(flask.url_for('main'))

    entries = Entry.get_with_hashtag(value)
    presentable = list()
    for entry in entries:
        presentable.append(PresentableEntry(entry))

    return flask.render_template('show_entries.html',
                                 title=u'#{}'.format(value),
                                 entries=presentable)
