# -*- coding: utf-8 -*-
import flask

from application import app

@app.route('/add_entry', methods=['GET'])
def add_entry():
    return flask.render_template('user/add_entry.html', title=u'Nowy wpis', content='')
