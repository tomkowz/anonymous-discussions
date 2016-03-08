# -*- coding: utf-8 -*-

import flask

from application import app
from application.mod_core.models_entry import Entry
from application.mod_user.presentable_object import PresentableEntry

@app.route('/admin/approve_entries', methods=['GET'])
def admin_show_approve_entries():
    if _authorized() == False:
        flask.abort(401)

    # Get entries waiting for approval
    p_entries = [PresentableEntry(e) for e in Entry.get_all_waiting_to_aprove()]
    return flask.render_template('admin_panel/approve_entries.html',
                                  title='Moderacja',
                                  p_entries=p_entries)

@app.route('/admin/approve_entries/<int:id>/<int:approved>', methods=['GET'])
def admin_approve_entry(id, approved):
    if _authorized() == False:
        flask.abort(401)

    # Update entry
    entry = Entry.get_with_id(id)
    if entry is not None:
        entry.approved = approved
        entry.save()

    return admin_show_approve_entries()

def _authorized():
    return flask.session.get('logged_in_admin', None) is not None
