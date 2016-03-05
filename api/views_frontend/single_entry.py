# -*- coding: utf-8 -*-

import flask

from api import app
from api.models.entry import Entry
from api.models.comment import Comment
from api.views_frontend.presentable_entry import PresentableEntry
from api.utils.date_utils import DateUtils

@app.route('/entry/<id>', methods=['GET'])
def show_entry(id):
    entry = Entry.get_with_id(id)
    if entry is not None:
        presentable = PresentableEntry(entry)
        return flask.render_template('single_entry.html', title='', entries=[presentable])
    return flask.render_template('show_entries.html')

@app.route('/entry/<entry_id>', methods=['POST'])
def add_comment(entry_id):
    content = flask.request.form['content']
    min_len = 10
    max_len = 150

    if len(content) < min_len:
        error = u'Komentarz jest zbyt krótki (min. {} znaków).'.format(min_len)
    elif len(content) > max_len:
        error = u'Komentarz jest zbyt długi (max. {} znaków).'.format(max_len)
    else:
        comment = Comment()
        comment.content = content
        comment.timestamp = DateUtils.timestamp_for_now()
        comment.entry_id = entry_id
        comment.save()

        if comment is not None:
            return flask.redirect(flask.url_for('show_entry', id=entry_id))
        else:
            error = u'Nie udało się dodać komentarza. Spróbuj ponownie.'

    entry = Entry.get_with_id(entry_id)
    presentable = PresentableEntry(entry)

    return flask.render_template('single_entry.html',
                                 content=content,
                                 entries=[presentable],
                                 error=error)
