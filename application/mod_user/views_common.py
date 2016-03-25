# -*- coding: utf-8 -*-
import flask

from application import app
from application.mod_api.models_recommended_hashtag import RecommendedHashtag
from application.mod_user.presentable_object import PresentableRecommendedHashtag

@app.route('/faq', methods=['GET'])
def faq():
    recommended_hashtags = RecommendedHashtag.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    return flask.render_template('user/faq.html',
                                 title=u'FAQ',
                                 p_recommended_hashtags=p_recommended_hashtags)
