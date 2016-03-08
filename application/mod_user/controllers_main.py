# -*- coding: utf-8 -*-

import flask

from application import app
from application.mod_core.models_entry import Entry
from presentable_object import PresentableEntry

@app.route('/', methods=['GET'])
def main():
    p_entries = [PresentableEntry(x) for x in Entry.get_all_approved(True)]
    return flask.render_template('user/main.html',
                                  title=u'Najnowsze',
                                  p_entries=p_entries)
