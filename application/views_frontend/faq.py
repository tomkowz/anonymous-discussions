# -*- coding: utf-8 -*-

import flask

from application import app

@app.route('/faq', methods=['GET'])
def about():
    return flask.render_template('faq.html', title=u'FAQ')
