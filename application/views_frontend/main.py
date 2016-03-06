# -*- coding: utf-8 -*-

import flask

from application import app
from application.models.entry import Entry
from application.views_frontend.presentable import PresentableEntry

@app.route('/', methods=['GET'])
def main():
    entries = Entry.get_all_approved(True)
    presentable = list()
    for entry in entries:
        presentable.append(PresentableEntry(entry))

    return flask.render_template('user/main.html',
                                 title=u'Najnowsze',
                                 entries=presentable)

@app.route('/hashtag/<value>', methods=['GET'])
def show_entries_for_hashtag(value):
    if len(value) == 0:
        return flask.redirect(flask.url_for('main'))

    entries = Entry.get_with_hashtag(value)
    presentable = list()
    for entry in entries:
        presentable.append(PresentableEntry(entry))

    return flask.render_template('user/main.html',
                                 title=u'#{}'.format(value),
                                 entries=presentable)
