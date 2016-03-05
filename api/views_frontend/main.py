# -*- coding: utf-8 -*-

import flask

from api import app
from api.models.entry import Entry
from api.views_frontend.presentable_entry import PresentableEntry

@app.route('/', methods=['GET'])
def main():
    entries = Entry.get_all()
    presentable = list()
    for entry in entries:
        presentable.append(PresentableEntry(entry))

    return flask.render_template('show_entries.html',
                                 title=u'Najnowsze',
                                 entries=presentable)
