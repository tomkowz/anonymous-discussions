# -*- coding: utf-8 -*-

import flask

from application import app
from application.models.admin import Admin
from application.models.entry import Entry
from application.views_frontend.presentable import PresentableEntry

@app.route('/admin/login', methods=['GET'])
def show_admin_login(username=None, password=None, error=None):
    return flask.render_template('admin/login.html', username=username, password=password,
                                 title='Logowanie (Admin)', error=error)

@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = flask.request.form['username']
    password = flask.request.form['password']
    if Admin.login(username, password) == True:
        p_entries = [PresentableEntry(e) for e in Entry.get_all_waiting_to_aprove()]
        return flask.render_template('admin/entries_to_approve.html', title='Moderacja', p_entries=p_entries)
    else:
        return show_admin_login(username, password, 'Niepoprawne dane.')

@app.route('/admin/entries/<id>/approve/<approved>')
def admin_approve_entry(id, approved):
    # Update entry
    entry = Entry.get_with_id(id)
    entry.approved = approved
    entry.save()

    # Refresh
    p_entries = [PresentableEntry(e) for e in Entry.get_all_waiting_to_aprove()]
    return flask.render_template('admin/entries_to_approve.html', title='Moderacja', p_entries=p_entries)
