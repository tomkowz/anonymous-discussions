# -*- coding: utf-8 -*-

import flask

from application import app
from application.models.entry import Entry
from application.views_frontend.presentable import PresentableEntry

@app.route('/', methods=['GET'])
def main():
    p_entries = [PresentableEntry(x) for x in Entry.get_all_approved(True)]
    return flask.render_template('user/main.html', title=u'Najnowsze', p_entries=p_entries)

@app.route('/hashtag', methods=['GET'], defaults={'value': ''})
@app.route('/hashtag/', methods=['GET'], defaults={'value': ''})
@app.route('/hashtag/<value>', methods=['GET'])
def show_entries_for_hashtag(value):
    if len(value) == 0:
        return main()

    p_entries = [PresentableEntry(x) for x in Entry.get_with_hashtag(value)]
    return flask.render_template('user/main.html', title='#' + value, p_entries=p_entries)
