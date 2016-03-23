# -*- coding: utf-8 -*-

import datetime
import flask

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from presentable_object import PresentableEntry, PresentableComment
from application.utils.sanitize_services import Sanitize
from application.utils.pagination_services import Pagination

@app.route('/entry/<int:entry_id>/vote_plus', methods=['GET'])
def entry_vote_plus(entry_id):
    Entry.vote(entry_id, 1)
    return flask.redirect(flask.url_for('single_entry', entry_id=entry_id))

@app.route('/entry/<int:entry_id>/vote_minus', methods=['GET'])
def entry_vote_minus(entry_id):
    Entry.vote(entry_id, -1)
    return flask.redirect(flask.url_for('single_entry', entry_id=entry_id))

@app.route('/entry/<int:entry_id>/comment/<int:comment_id>/vote_plus', methods=['GET'])
def comment_vote_plus(entry_id, comment_id):
    Comment.vote(comment_id, 1)
    return flask.redirect(flask.url_for('single_entry', entry_id=entry_id))

@app.route('/entry/<int:entry_id>/comment/<int:comment_id>/vote_minus', methods=['GET'])
def comment_vote_minus(entry_id, comment_id):
    Comment.vote(comment_id, -1)
    return flask.redirect(flask.url_for('single_entry', entry_id=entry_id))

@app.route('/entry/<int:entry_id>', methods=['GET', 'POST'], defaults={'comments_order': None, 'page_number': 1})
@app.route('/entry/<int:entry_id>/<string:comments_order>', methods=['GET', 'POST'], defaults={'page_number': 1})
@app.route('/entry/<int:entry_id>/page/<int:page_number>', methods=['GET', 'POST'], defaults={'comments_order': None})
@app.route('/entry/<int:entry_id>/page/<int:page_number>/<string:comments_order>', methods=['GET', 'POST'])
def single_entry(entry_id, comments_order, page_number):
    function = None
    if flask.request.method == 'GET':
        function = single_entry_get
    elif flask.request.method == 'POST':
        function = single_entry_post

    return function(entry_id, comments_order, page_number, app.config['ITEMS_PER_PAGE'])

def single_entry_get(entry_id, comments_order, page_number, items_per_page):
    comments_order = _get_comments_order(comments_order)
    p_entry, p_comments, total_comments_count = \
        _get_entry_and_comments_p(entry_id=entry_id, comments_order=comments_order,
                                  page_number=page_number, items_per_page=items_per_page)

    if p_entry is None or \
       (p_comments is None and page_number != 1):
        flask.abort(404)

    return _render_view(p_entry=p_entry,
                        p_comments=p_comments,
                        comments_order=comments_order,
                        pagination=Pagination(page_number, items_per_page, total_comments_count),
                        error=None, success=None)

def single_entry_post(entry_id, comments_order, page_number, items_per_page):
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
    p_entry, p_comments, total_comments_count = \
        _get_entry_and_comments_p(entry_id=entry_id, comments_order=comments_order,
                                  page_number=page_number, items_per_page=items_per_page)

    return _render_view(p_entry=p_entry,
                        p_comments=p_comments,
                        comments_order=comments_order,
                        pagination=Pagination(page_number, items_per_page, total_comments_count),
                        error=error, success=success)

# Helpers
def _insert_comment(content, entry_id):
    comment = Comment()
    comment.content = content
    comment.created_at = datetime.datetime.utcnow()
    comment.entry_id = entry_id
    comment.save()
    return comment

def _get_entry_and_comments_p(entry_id, comments_order, page_number, items_per_page):
    entry = Entry.get_with_id(entry_id)
    if entry is None:
        return None, None, None

    p_entry = PresentableEntry(entry)
    comments = Comment.get_comments_with_entry_id(entry_id, _comments_ordering_for_sql(comments_order),
                                                  limit=items_per_page, offset=page_number - 1)

    p_comments = [PresentableComment(c) for c in comments]
    total_comments_count = Comment.get_comments_count_with_entry_id(entry_id)

    return p_entry, p_comments, total_comments_count

def _render_view(p_entry, p_comments, comments_order, pagination, error=None, success=None):
    return flask.render_template(
            'user/single_entry.html',
            title='',
            p_entry=p_entry,
            p_comments=p_comments,
            comments_order=comments_order,
            pagination=pagination,
            error=error, success=success)

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
