# -*- coding: utf-8 -*-

import flask

from api import app

@app.route('/about', methods=['GET'])
def about():
    return flask.render_template('about.html', title=u'O szafie')
