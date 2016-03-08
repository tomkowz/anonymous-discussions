# -*- coding: utf-8 -*-

import flask

from application import app
from application.models.entry import Entry
from presentable_object import PresentableEntry
from application.utils.sanitize import Sanitize

@app.route('/hashtag', methods=['GET'], defaults={'value': ''})
@app.route('/hashtag/', methods=['GET'], defaults={'value': ''})
@app.route('/hashtag/<string:value>', methods=['GET'])
def show_entries_for_hashtag(value):
    value_valid, _ = Sanitize.is_valid_input(value)
    if len(value) == 0 and value_valid == True:
        # Just fall back to '/'
        return flask.redirect(flask.url_for('main'))

    p_entries = [PresentableEntry(x) for x in Entry.get_with_hashtag(value)]
    return flask.render_template('user/main.html',
                                  title='#' + value.lower(),
                                  p_entries=p_entries)
