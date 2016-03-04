# -*- coding: utf-8 -*-

import flask

from api import app

@app.route('/hashtag/<value>', methods=['GET'])
def show_entries_for_hashtag(value):
    return value
