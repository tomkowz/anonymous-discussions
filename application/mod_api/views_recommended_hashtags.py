# -*- coding: utf-8 -*-
import flask, json

from application import app
from application.mod_api.models_recommended_hashtag import RecommendedHashtag

@app.route('/api/recommended_hashtags', methods=['GET'])
def api_get_recommended_hashtags():
    hashtags = RecommendedHashtag.get_all()
    result = [h.to_json() for h in hashtags]
    return flask.jsonify({'recommended_hashtags': result}), 200
