# -*- coding: utf-8 -*-
import flask

from application import app
from application.mod_api.models_recommended_hashtag import RecommendedHashtag, RecommendedHashtagDAO
from application.mod_web.presentable_object import PresentableRecommendedHashtag


@app.route('/najczesciej-zadawane-pytania', methods=['GET'])
def faq():
    recommended_hashtags = RecommendedHashtagDAO.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    return flask.render_template('web/faq.html',
                                 title=u'FAQ',
                                 p_recommended_hashtags=p_recommended_hashtags)
