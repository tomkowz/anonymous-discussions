# -*- coding: utf-8 -*-

import flask

from application import app
from application.models.admin import Admin
from application.models.entry import Entry
from application.views_frontend.presentable import PresentableEntry

@app.route('/admin/login', methods=['GET'])
def show_admin_login(username=None, password=None, error=None):
    return flask.render_template('admin/login.html',
                                  username=username,
                                  password=password,
                                  title='Logowanie (Admin)',
                                  error=error)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = flask.request.form['username']
    password = flask.request.form['password']

    valid_username, _ = Sanitize.is_valid_input(username)
    valid_password, _ = Sanitize.is_valid_input(password)

    admin = Admin(username, password)
    if admin.login() == True and \
       valid_username == True and \
       valid_password == True:
        flask.session['logged_in'] = True
        p_entries = [PresentableEntry(e) for e in Entry.get_all_waiting_to_aprove()]
        return flask.render_template('admin/entries_to_approve.html',
                                      title='Moderacja',
                                      p_entries=p_entries)
    else:
        return show_admin_login(username, password, 'Niepoprawne dane.')
