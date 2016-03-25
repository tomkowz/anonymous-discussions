# -*- coding: utf-8 -*-
import flask, json

from application import app
from application.mod_api.models_comment import Comment
from application.mod_api.models_entry import Entry
from application.mod_api.models_hashtag import Hashtag

from application.mod_api.views_entries import _update_hashtags_with_content

from application.utils.sanitize_services import Sanitize

@app.route('/api/popular_hashtags', methods=['GET'])
def api_get_popular_hashtags(limit=None):
    if limit is None:
        limit = flask.request.args.get('limit', None, type=int)

    if limit is None:
        return flask.jsonify({'error': "Brak parametru 'limit'"}), 400

    hashtags = Hashtag.get_most_popular(limit=limit)
    result = [h.to_json() for h in hashtags]
    return flask.jsonify({'hashtags': result}), 200

@app.route('/api/deployment/populate_popular_hashtags', methods=['GET'])
def api_populate_popular_hashtags():
    entries = Entry.get_all()
    comments = Comment.get_all()

    contents = list()
    for entry in entries:
        contents.append(entry.content)

    for comment in comments:
        contents.append(comment.content)

    [_update_hashtags_with_content(c) for c in contents]

    return flask.jsonify({'success': 'ok'}), 200
