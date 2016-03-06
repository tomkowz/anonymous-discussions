# -*- coding: utf-8 -*-

import flask

from application import app
from application.models.entry import Entry
from application.models.comment import Comment
from application.views_frontend.presentable import PresentableEntry, PresentableComment
from application.utils.date_utils import DateUtils

@app.route('/entry/<entry_id>', methods=['GET'], defaults={'comments_order': 'newest'})
@app.route('/entry/<entry_id>/<comments_order>', methods=['GET'])
def show_entry(entry_id, comments_order):
    entry = Entry.get_with_id(entry_id)
    if entry is not None:
        p_entry = PresentableEntry(entry)

        comments = Comment.get_with_entry_id(entry_id, _comments_ordering_for_sql(comments_order))
        p_comments = [PresentableComment(c) for c in comments]

        return flask.render_template(
                'user/single_entry.html',
                title='',
                p_entry=p_entry,
                p_comments=p_comments,
                comments_order=comments_order)

    return flask.render_template('show_entries.html')

@app.route('/entry/<entry_id>', methods=['POST'], defaults={'comments_order': 'newest'})
@app.route('/entry/<entry_id>/<comments_order>', methods=['POST'])
def add_comment(entry_id, comments_order):
    content = flask.request.form['content']
    min_len = 10
    max_len = 500

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
            return flask.redirect(flask.url_for('show_entry', entry_id=entry_id, comments_order=comments_order))
        else:
            error = u'Nie udało się dodać komentarza. Spróbuj ponownie.'

    entry = Entry.get_with_id(entry_id)
    p_entry = PresentableEntry(entry)

    comments = Comment.get_with_entry_id(entry.id, _comments_ordering_for_sql(comments_order))
    p_comments = [PresentableComment(c) for c in comments]

    return flask.render_template('user/single_entry.html',
                                 comment_content=content,
                                 p_entry=p_entry,
                                 p_comments=p_comments,
                                 error=error)

def _comments_ordering_for_sql(comments_order):
    order = 'desc'
    if comments_order == 'oldest':
        order = 'asc'
    return order
