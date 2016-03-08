# -*- coding: utf-8 -*-

import flask

from application import app
from models_admin import Admin
import controllers_approve
from application.utils.sanitize_services import Sanitize

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    func = None
    if flask.request.method == 'GET':
        func = admin_login_get
    else:
        func = admin_login_post

    return func()

def admin_login_get(username=None, password=None, error=None):
    return flask.render_template('admin_panel/login.html',
                                  username=username,
                                  password=password,
                                  title='Logowanie',
                                  error=error)

def admin_login_post():
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

    return admin_login_get(username, password, 'Niepoprawne dane.')
