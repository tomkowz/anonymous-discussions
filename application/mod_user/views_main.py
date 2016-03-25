# -*- coding: utf-8 -*-

import flask, json

from application import app
from application.mod_api.views_entries import api_get_entries
from application.mod_api.models_entry import Entry
from application.mod_api.models_hashtag import Hashtag
from application.mod_api.models_recommended_hashtag import RecommendedHashtag
from application.mod_user.presentable_object import \
    PresentableEntry, PresentablePopularHashtag, PresentableRecommendedHashtag
from application.utils.pagination_services import Pagination

from application.mod_user.views_token import generate_token

@app.route('/', methods=['GET'], defaults={'page_number': 1})
@app.route('/strona/<int:page_number>', methods=['GET'])
def main(page_number):
    if flask.request.cookies.get('op_token', None) is None:
        return generate_token()

    return _load_page_with_entries(title=u'Najnowsze', page_number=page_number)

@app.route('/najlepsze', methods=['GET'], defaults={'page_number': 1})
@app.route('/najlepsze/strona/<int:page_number>', methods=['GET'])
def main_top(page_number):
    return _load_page_with_entries(title=u'Top plusowane',
                                   order_by="votes_up desc",
                                   page_number=page_number)

def _load_page_with_entries(title=None, page_number=None, order_by=None):
    items_per_page = app.config['ITEMS_PER_PAGE']
    response, status = api_get_entries(order_by=order_by,
                                       per_page=items_per_page,
                                       user_op_token=flask.request.cookies.get('op_token'),
                                       page_number=page_number)
    response_json = json.loads(response.data)

    p_entries = list()
    for entry_json in response_json["entries"]:
        entry = Entry.from_json(entry_json)
        p_entries.append(PresentableEntry(entry))

    if not p_entries and page_number != 1:
        flask.abort(404)

    hashtags = Hashtag.get_most_popular(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in hashtags]

    recommended_hashtags = RecommendedHashtag.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    entries_count = Entry.get_count_all_approved()
    pagination = Pagination(page_number, items_per_page, entries_count)
    return flask.render_template('user/main.html', title=title,
                                  p_entries=p_entries,
                                  p_recommended_hashtags=p_recommended_hashtags,
                                  p_popular_hashtags=p_popular_hashtags,
                                  pagination=pagination)
