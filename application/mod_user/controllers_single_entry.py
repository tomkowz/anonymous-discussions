# -*- coding: utf-8 -*-

import datetime
import flask

from application import app
from application.models.entry import Entry
from application.models.comment import Comment
from presentable_object import PresentableEntry, PresentableComment
from application.utils.sanitize import Sanitize

@app.route('/entry/<int:entry_id>', methods=['GET'], defaults={'comments_order': None})
@app.route('/entry/<int:entry_id>/<string:comments_order>', methods=['GET'])
def show_entry(entry_id, comments_order):
    comments_order = _get_comments_order(comments_order)

    p_entry, p_comments = _get_entry_and_comments_p(entry_id, comments_order)
    if p_entry is not None:
        return _render_view(p_entry, p_comments,
                            comments_order, error=None, success=None)

    # Entry not found, show main page
    return flask.redirect(flask.url_for('main'))

@app.route('/entry/<int:entry_id>', methods=['POST'], defaults={'comments_order': 'oldest'})
@app.route('/entry/<int:entry_id>/<string:comments_order>', methods=['POST'])
def add_comment(entry_id, comments_order):
    content = flask.request.form['content']
    valid_content, error = _is_comment_content_valid(content)
    success = None

    if valid_content == True:
        comment = _insert_comment(content, entry_id)
        if comment is None:
            error = 'Nie udało się dodać komentarza. Spróbuj ponownie.'
        else:
            success = 'Komentarz dodano pomyślnie.'

    # Refresh
    p_entry, p_comments = _get_entry_and_comments_p(entry_id, comments_order)
    return _render_view(p_entry, p_comments, comments_order, error, success)

# Helpers
def _insert_comment(content, entry_id):
    comment = Comment()
    comment.content = content
    comment.created_at = datetime.datetime.utcnow()
    comment.entry_id = entry_id
    comment.save()
    return comment

def _get_entry_and_comments_p(entry_id, comments_order):
    entry = Entry.get_with_id(entry_id)
    if entry is None:
        return None, None

    p_entry = PresentableEntry(entry)

    comments = Comment.get_with_entry_id(entry_id, _comments_ordering_for_sql(comments_order))
    p_comments = [PresentableComment(c) for c in comments]
    return p_entry, p_comments

def _render_view(p_entry, p_comments, comments_order, error=None, success=None):
    return flask.render_template(
            'user/single_entry.html',
            title='',
            p_entry=p_entry,
            p_comments=p_comments,
            comments_order=comments_order,
            error=error,
            success=success)

def _get_comments_order(comments_order):
    # Take comments_order from session variable and updates comments_order
    if comments_order is None:
        if flask.session.get('comments_order') is None:
            flask.session['comments_order'] = 'newest'
        comments_order = flask.session['comments_order']

    # Update comments_order in case when passed one is not None
    flask.session['comments_order'] = comments_order

    return comments_order

def _comments_ordering_for_sql(comments_order):
    order = 'desc'
    if comments_order == 'oldest':
        order = 'asc'
    return order

def _is_comment_content_valid(content):
    char_len = (2, 500)

    content_valid, invalid_symbol = Sanitize.is_valid_input(content)
    if content_valid == False:
        return False, 'Komentarz zawiera niedozwolone elementy: {}'.format(invalid_symbol)
    elif len(content) < char_len[0]:
        return False, 'Komentarz jest zbyt krótki.'
    elif len(content) > char_len[1]:
        return False, 'Komentarz jest zbyt długi (max. {} znaków).'.format(max_len)

    return True, None
