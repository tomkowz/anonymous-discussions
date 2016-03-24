# -*- coding: utf-8 -*-
import flask, json

from application import app
from application.mod_core.models_hashtag import Hashtag

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
