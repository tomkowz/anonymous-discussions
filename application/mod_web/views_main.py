# -*- coding: utf-8 -*-

import flask, json

from application import app
from application.mod_api.views_entries import api_get_entries
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_hashtag import Hashtag, HashtagDAO
from application.mod_api.models_recommended_hashtag import RecommendedHashtag, RecommendedHashtagDAO
from application.mod_web.utils_user_notifications import utils_get_user_notifications_count
from application.mod_web.presentable_object import \
    PresentableEntry, PresentablePopularHashtag, PresentableRecommendedHashtag
from application.utils.pagination_services import Pagination

from application.mod_web.views_token import generate_token


@app.route('/', methods=['GET'], defaults={'page': 1})
@app.route('/strona/<int:page>', methods=['GET'])
def main(page):
    if flask.request.cookies.get('op_token', None) is None:
        return generate_token(redirect_to=flask.url_for('main'))

    return _load_page_with_entries(title=u'Najnowsze', page=page)


@app.route('/najlepsze', methods=['GET'], defaults={'page': 1})
@app.route('/najlepsze/strona/<int:page>', methods=['GET'])
def main_top(page):
    return _load_page_with_entries(title=u'Top plusowane',
                                   order_by="votes_up desc",
                                   page=page)


def _load_page_with_entries(title=None, page=None, order_by=None):
    user_token = flask.request.cookies.get('op_token')
    items_per_page = app.config['ITEMS_PER_PAGE']
    response, status = api_get_entries(order_by=order_by,
                                       per_page=items_per_page,
                                       user_op_token=user_token,
                                       page=page)
    response_json = json.loads(response.data)

    p_entries = list()
    for entry_json in response_json["entries"]:
        entry = Entry.from_json(entry_json)
        p_entries.append(PresentableEntry(entry))

    if not p_entries and page != 1:
        flask.abort(404)

    hashtags = HashtagDAO.get_most_popular_hashtags(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in hashtags]

    recommended_hashtags = RecommendedHashtagDAO.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    entries_count = EntryDAO.get_entries_count()

    # Get active user notifications count
    user_notifications_count = utils_get_user_notifications_count(user_token)

    pagination = Pagination(page, items_per_page, entries_count)
    return flask.render_template('web/main.html', title=title,
                                  p_entries=p_entries,
                                  p_recommended_hashtags=p_recommended_hashtags,
                                  p_popular_hashtags=p_popular_hashtags,
                                  user_notifications_count=user_notifications_count,
                                  pagination=pagination)
