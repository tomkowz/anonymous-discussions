# -*- coding: utf-8 -*-
import flask

from application import app

@app.route('/faq', methods=['GET'])
def faq():
    return flask.render_template('user/faq.html', title=u'FAQ')
