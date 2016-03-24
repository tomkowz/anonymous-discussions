# -*- coding: utf-8 -*-

import datetime, flask, json

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from application.mod_core.models_hashtag import Hashtag
from presentable_object import PresentableEntry, PresentableComment, PresentablePopularHashtag
from application.utils.sanitize_services import Sanitize
from application.utils.pagination_services import Pagination

from application.mod_api.controllers_entries import \
    api_get_single_entry, \
    api_get_comments_for_entry, \
    api_post_comment_for_entry

@app.route('/entries/<int:entry_id>',
            methods=['GET', 'POST'],
            defaults={'comments_order': None, 'page_number': 1})
@app.route('/entries/<int:entry_id>/<string:comments_order>',
            methods=['GET', 'POST'],
            defaults={'page_number': 1})
@app.route('/entries/<int:entry_id>/page/<int:page_number>',
            methods=['GET', 'POST'],
            defaults={'comments_order': None})
@app.route('/entries/<int:entry_id>/page/<int:page_number>/<string:comments_order>',
            methods=['GET', 'POST'])
def single_entry(entry_id, comments_order, page_number):
    # select proper function
    function = None
    if flask.request.method == 'GET':
        function = single_entry_get
    elif flask.request.method == 'POST':
        function = post_comment_for_entry

    # get comments_order
    if comments_order is None:
        # Make sure that comments_order is correctly set.
        comments_order = flask.session.get('comments_order', None)

    # Check against asc and desc because in the past it was oldest and newest.
    if comments_order == 'newest' or \
        comments_order == 'oldest' or \
        comments_order is None:
        comments_order = 'desc'

    return function(entry_id=entry_id, comments_order=comments_order,
                    page_number=page_number, per_page=app.config['ITEMS_PER_PAGE'])

def single_entry_get(entry_id, page_number, per_page,
                     comments_order, error=None, success=None):
    # get entry
    response, status = api_get_single_entry(entry_id)
    if status != 200:
        return flask.abort(404)

    entry = Entry.from_json(json.loads(response.data)['entry'])

    # store comments order globaly
    flask.session['comments_order'] = comments_order

    # get comments
    response, status = api_get_comments_for_entry(entry_id=entry_id, comments_order=comments_order,
                                                  per_page=per_page, page_number=page_number)

    if status != 200:
        return flask.abort(404)

    comments = [Entry.from_json(c) for c in json.loads(response.data)['comments']]
    total_comments_count = Comment.get_comments_count_with_entry_id(entry_id)

    # prepare result
    p_entry = PresentableEntry(entry)
    p_comments = [PresentableComment(c) for c in comments]
    pagination = Pagination(page_number, per_page, total_comments_count)

    hashtags = Hashtag.get_most_popular(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in hashtags]

    return flask.render_template('user/single_entry.html', title='',
                                 p_entry=p_entry, p_comments=p_comments,
                                 p_popular_hashtags=p_popular_hashtags,
                                 comments_order=comments_order, pagination=pagination,
                                 error=error, success=success)

def post_comment_for_entry(entry_id, page_number, per_page, comments_order):
    content = flask.request.form['content']
    response, status = api_post_comment_for_entry(entry_id=entry_id, content=content)

    success = None
    error = None
    if status == 200:
        success = "Komentarz dodano pomyślnie"
    else:
        error = json.loads(response.data)['error']

    return single_entry_get(entry_id=entry_id, page_number=page_number, \
                           per_page=per_page, comments_order=comments_order, \
                           error=error, success=success)
