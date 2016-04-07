# -*- coding: utf-8 -*-

import datetime, flask, json

from application import app, limiter
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_comment import Comment, CommentDAO
from application.mod_api.models_hashtag import Hashtag, HashtagDAO
from application.mod_api.models_recommended_hashtag import RecommendedHashtag, RecommendedHashtagDAO
from application.mod_web.utils_user_notifications import utils_get_user_notifications_count
from application.mod_web.presentable_object import \
    PresentableEntry, PresentableComment, \
    PresentablePopularHashtag, PresentableRecommendedHashtag
from application.utils.sanitize_services import Sanitize
from application.utils.pagination_services import Pagination

from application.mod_api.views_entries import \
    api_get_entry, \
    api_post_entry

from application.mod_api.views_comments import \
    api_get_comments_for_entry, \
    api_post_comment

from application.mod_web.views_user_settings import generate_token


@app.route('/wpis/<int:entry_id>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>',
            methods=['GET', 'POST'])

@app.route('/wpis/<int:entry_id>/sort/<string:comments_order>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>/sort/<string:comments_order>',
            methods=['GET', 'POST'])

@app.route('/wpis/<int:entry_id>/strona/<int:page>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>/strona/<int:page>',
            methods=['GET', 'POST'])

@app.route('/wpis/<int:entry_id>/strona/<int:page>/sort/<string:comments_order>',
            methods=['GET', 'POST'])
@app.route('/wpis/<int:entry_id>/<string:excerpt>/strona/<int:page>/sort/<string:comments_order>',
            methods=['GET', 'POST'])
def single_entry(entry_id, comments_order=None, page=1, per_page=None,
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
                    page=page, per_page=per_page,
                    excerpt=excerpt, error=error, success=success, comment_content='')


def single_entry_get(entry_id, page, per_page,
                     comments_order, excerpt=None,
                     error=None, success=None, comment_content=None):
    # For new user app need to check whether they have user_token generated.
    # If not, they will not be able to enter this endpoint.
    user_token = flask.request.cookies.get('op_token', None)
    if user_token is None:
        return generate_token(flask.url_for('single_entry',
                       entry_id=entry_id,
                       page=page,
                       per_page=per_page,
                       comments_order=comments_order,
                       error=error,
                       success=success))


    # get entry
    response, status = api_get_entry(entry_id=entry_id,
        user_op_token=user_token)

    if status != 200:
        return flask.abort(404)

    entry = Entry.from_json(json.loads(response.data)['entry'])

    # store comments order globaly
    flask.session['comments_order'] = comments_order

    # get comments
    user_token = flask.request.cookies.get('op_token', None)
    response, status = api_get_comments_for_entry(entry_id=entry_id,
                                                  comments_order=comments_order,
                                                  user_op_token=user_token,
                                                  per_page=per_page, page=page)

    if status != 200:
        return flask.abort(404)

    comments = [Comment.from_json(c) for c in json.loads(response.data)['comments']]
    total_comments_count = CommentDAO.get_comments_count(entry_id)

    # prepare result
    p_entry = PresentableEntry(entry)
    p_comments = [PresentableComment(c) for c in comments]
    pagination = Pagination(page, per_page, total_comments_count)

    popular_hashtags = HashtagDAO.get_most_popular_hashtags(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in popular_hashtags]

    recommended_hashtags = RecommendedHashtagDAO.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    user_notifications_count = utils_get_user_notifications_count(user_token)

    return flask.render_template('web/single_entry.html', title='',
                                 p_entry=p_entry,
                                 p_comments=p_comments,
                                 p_recommended_hashtags=p_recommended_hashtags,
                                 p_popular_hashtags=p_popular_hashtags,
                                 comments_order=comments_order,
                                 pagination=pagination,
                                 op_token=flask.request.cookies.get('op_token', None),
                                 error=error,
                                 success=success,
                                 user_notifications_count=user_notifications_count,
                                 comment_content=comment_content)


def post_comment_for_entry(entry_id, page, per_page, comments_order,
                           excerpt=None, error=None, success=None, comment_content=None):
    content = flask.request.form['content']
    op_token = flask.request.cookies.get('op_token', None)
    response, status = api_post_comment(entry_id=entry_id, content=content, user_op_token=op_token)

    if status == 200:
        error = ''
        success = "Komentarz dodano pomyślnie"
        return flask.redirect(flask.url_for('single_entry',
                       entry_id=entry_id, page=page,
                       per_page=per_page, comments_order=comments_order,
                       error=error, success=success))
    else:
        success = ''
        error = json.loads(response.data)['error']
        return single_entry_get(entry_id=entry_id, page=page,
                                per_page=per_page, comments_order=comments_order,
                                error=error, success=success, comment_content=content)


@app.route('/wpis/nowy', methods=['GET'])
def present_post_entry_view(content='', error=None):
    recommended_hashtags = RecommendedHashtagDAO.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    user_token = flask.request.cookies.get('op_token', None)
    user_notifications_count = utils_get_user_notifications_count(user_token)

    return flask.render_template('web/add_entry.html',
                                  title=u'Nowy wpis',
                                  p_recommended_hashtags=p_recommended_hashtags,
                                  op_token=user_token,
                                  user_notifications_count=user_notifications_count,
                                  content=content, error=error)


@app.route('/wpis/nowy', methods=['POST'])
@limiter.limit("2/minute")
@limiter.limit("6/hour")
@limiter.limit("20/day")
def post_entry():
    content = flask.request.form.get('content', None, type=str)
    user_op_token = flask.request.form.get('user_op_token', None, type=str)

    response, status = api_post_entry(content=content, user_op_token=user_op_token)
    if status == 201:
        return flask.redirect(flask.url_for('main'))
    else:
        return present_post_entry_view(content=content, error=json.loads(response.data)['error'])
