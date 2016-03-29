# -*- coding: utf-8 -*-
import flask

from application import app
from application.mod_api.models_recommended_hashtag import RecommendedHashtag, RecommendedHashtagDAO
from application.mod_web.presentable_object import PresentableRecommendedHashtag
from application.mod_web.utils_user_notifications import utils_get_user_notifications_count

@app.route('/najczesciej-zadawane-pytania', methods=['GET'])
def faq():
    recommended_hashtags = RecommendedHashtagDAO.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    user_token = flask.request.cookies.get('op_token')
    user_notifications_count = utils_get_user_notifications_count(user_token)
    return flask.render_template('web/faq.html',
                                 title=u'FAQ',
                                 p_recommended_hashtags=p_recommended_hashtags,
                                 user_notifications_count=user_notifications_count)
