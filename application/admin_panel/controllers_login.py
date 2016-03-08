# -*- coding: utf-8 -*-

import flask

from application import app
from application.admin_panel.models import Admin
from application.admin_panel import controllers_approve
from application.utils.sanitize import Sanitize

@app.route('/admin/login', methods=['GET'])
def show_admin_login(username=None, password=None, error=None):
    return flask.render_template('admin_panel/login.html',
                                  username=username,
                                  password=password,
                                  title='Logowanie',
                                  error=error)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = flask.request.form['username']
    password = flask.request.form['password']

    if not username or not password:
        return show_admin_login(username, password, '')

    valid_username, _ = Sanitize.is_valid_input(username)
    valid_password, _ = Sanitize.is_valid_input(password)
    if valid_username == True and valid_password == True:
        admin = Admin(username, password)
        if admin.login() == True:
            # Set session's logged_in key.
            flask.session['logged_in_admin'] = True
            return flask.redirect(flask.url_for('admin_show_approve_entries'))

    return show_admin_login(username, password, 'Niepoprawne dane.')
