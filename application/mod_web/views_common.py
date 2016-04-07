# -*- coding: utf-8 -*-
import flask

from application import app
from application.mod_web.utils_display_on_web import UtilsDisplayOnWeb


@app.route('/najczesciej-zadawane-pytania', methods=['GET'])
def faq():
    user_token = flask.request.cookies.get('op_token')
    disp_web = UtilsDisplayOnWeb(user_token=user_token)

    return flask.render_template('web/faq.html',
        title=u'FAQ',
        p_recommended_hashtags=disp_web.get_recommended_hashtags(),
        user_notifications_count=disp_web.get_user_notifications_count())
