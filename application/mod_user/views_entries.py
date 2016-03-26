# -*- coding: utf-8 -*-

import datetime, flask, json

from application import app
from application.mod_api.models_entry import Entry
from application.mod_api.models_comment import Comment
from application.mod_api.models_hashtag import Hashtag
from application.mod_api.models_recommended_hashtag import RecommendedHashtag
from application.mod_user.presentable_object import \
    PresentableEntry, PresentableComment, \
    PresentablePopularHashtag, PresentableRecommendedHashtag
from application.utils.sanitize_services import Sanitize
from application.utils.pagination_services import Pagination

from application.mod_api.views_entries import \
    api_get_single_entry, \
    api_get_comments_for_entry, \
    api_post_entry, \
    api_post_comment

@app.route('/wpis/<int:entry_id>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>',
            methods=['GET', 'POST'])

@app.route('/wpis/<int:entry_id>/sort/<string:comments_order>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>/sort/<string:comments_order>',
            methods=['GET', 'POST'])

@app.route('/wpis/<int:entry_id>/strona/<int:page_number>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>/strona/<int:page_number>',
            methods=['GET', 'POST'])

@app.route('/wpis/<int:entry_id>/strona/<int:page_number>/sort/<string:comments_order>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>/strona/<int:page_number>/sort/<string:comments_order>',
            methods=['GET', 'POST'])
def single_entry(entry_id, comments_order=None, page_number=1, per_page=None,
                 excerpt=None, error=None, success=None):
    # Set per_page
    if per_page is None:
        per_page = app.config['ITEMS_PER_PAGE']

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
        comments_order = 'asc'

    return function(entry_id=entry_id, comments_order=comments_order,
                    page_number=page_number, per_page=per_page,
                    excerpt=excerpt, error=error, success=success, comment_content='')

def single_entry_get(entry_id, page_number, per_page,
                     comments_order, excerpt=None,
                     error=None, success=None, comment_content=None):
    # get entry
    response, status = api_get_single_entry(entry_id=entry_id,
                                            user_op_token=flask.request.cookies.get('op_token', None))
    if status != 200:
        return flask.abort(404)

    entry = Entry.from_json(json.loads(response.data)['entry'])
    entry.op_author = True

    # store comments order globaly
    flask.session['comments_order'] = comments_order

    # get comments
    response, status = api_get_comments_for_entry(entry_id=entry_id,
                                                  comments_order=comments_order,
                                                  user_op_token=flask.request.cookies.get('op_token', None),
                                                  per_page=per_page, page_number=page_number)

    if status != 200:
        return flask.abort(404)

    comments = [Entry.from_json(c) for c in json.loads(response.data)['comments']]
    total_comments_count = Comment.get_comments_count_with_entry_id(entry_id)

    # prepare result
    p_entry = PresentableEntry(entry)
    p_comments = [PresentableComment(c) for c in comments]
    pagination = Pagination(page_number, per_page, total_comments_count)

    popular_hashtags = Hashtag.get_most_popular(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in popular_hashtags]

    recommended_hashtags = RecommendedHashtag.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    return flask.render_template('user/single_entry.html', title='',
                                 p_entry=p_entry,
                                 p_comments=p_comments,
                                 p_recommended_hashtags=p_recommended_hashtags,
                                 p_popular_hashtags=p_popular_hashtags,
                                 comments_order=comments_order,
                                 pagination=pagination,
                                 op_token=flask.request.cookies.get('op_token', None),
                                 error=error,
                                 success=success,
                                 comment_content=comment_content)

def post_comment_for_entry(entry_id, page_number, per_page, comments_order,
                           excerpt=None, error=None, success=None, comment_content=None):
    content = flask.request.form['content']
    op_token = flask.request.cookies.get('op_token', None)
    response, status = api_post_comment(entry_id=entry_id, content=content, user_op_token=op_token)

    if status == 200:
        error = ''
        success = "Komentarz dodano pomyślnie"
        return flask.redirect(flask.url_for('single_entry',
                       entry_id=entry_id, page_number=page_number,
                       per_page=per_page, comments_order=comments_order,
                       error=error, success=success))
    else:
        success = ''
        error = json.loads(response.data)['error']
        return single_entry_get(entry_id=entry_id, page_number=page_number,
                                per_page=per_page, comments_order=comments_order,
                                error=error, success=success, comment_content=content)

@app.route('/wpis/nowy', methods=['GET'])
def present_post_entry_view(content='', error=None):
    recommended_hashtags = RecommendedHashtag.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    return flask.render_template('user/add_entry.html',
                                  title=u'Nowy wpis',
                                  p_recommended_hashtags=p_recommended_hashtags,
                                  op_token=flask.request.cookies.get('op_token', None),
                                  content=content, error=error)

@app.route('/wpis/nowy', methods=['POST'])
def post_entry():
    content = flask.request.form.get('content', None, type=str)
    user_op_token = flask.request.form.get('user_op_token', None, type=str)

    response, status = api_post_entry(content=content, user_op_token=user_op_token)
    if status == 201:
        return flask.redirect(flask.url_for('main'))
    else:
        return present_post_entry_view(content=content, error=json.loads(response.data)['error'])
