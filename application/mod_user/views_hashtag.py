# -*- coding: utf-8 -*-
import flask, json

from application import app
from application.mod_api.views_entries import api_get_entries
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_hashtag import Hashtag, HashtagDAO
from application.mod_api.models_recommended_hashtag import RecommendedHashtag, RecommendedHashtagDAO
from application.utils.pagination_services import Pagination
from application.mod_user.presentable_object import \
    PresentableEntry, PresentablePopularHashtag, PresentableRecommendedHashtag


@app.route('/tag', methods=['GET'], defaults={'value': '', 'page_number': 1})
@app.route('/tag/<string:value>', methods=['GET'], defaults={'page_number': 1})
@app.route('/tag/<string:value>/strona/<int:page_number>', methods=['GET'])
def show_entries_for_hashtag(value, page_number):
    if len(value) == 0:
        return flask.redirect(flask.url_for('main'))

    items_per_page = app.config['ITEMS_PER_PAGE']
    response, status = api_get_entries(hashtag=value, per_page=items_per_page, page_number=page_number)
    response_json = json.loads(response.data)

    p_entries = list()
    for entry_json in response_json["entries"]:
        entry = Entry.from_json(entry_json)
        p_entries.append(PresentableEntry(entry))

    if not p_entries and page_number != 1:
        flask.abort(404)

    hashtags = HashtagDAO.get_most_popular_hashtags(20)
    p_popular_hashtags = [PresentablePopularHashtag(h) for h in hashtags]

    recommended_hashtags = RecommendedHashtagDAO.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    entries_count = EntryDAO.get_entries_with_hashtag_count(hashtag=value)
    pagination = Pagination(page_number, items_per_page, entries_count)
    return flask.render_template('user/main.html', title='#' + value.lower(),
                                  p_entries=p_entries,
                                  p_recommended_hashtags=p_recommended_hashtags,
                                  p_popular_hashtags=p_popular_hashtags,
                                  pagination=pagination)
