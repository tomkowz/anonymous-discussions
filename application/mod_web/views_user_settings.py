# -*- coding: utf-8 -*-
import flask, json

from application import app
from application.mod_api.models_recommended_hashtag import \
    RecommendedHashtag, RecommendedHashtagDAO

from application.mod_api.utils_user_settings import \
    utils_get_user_settings

from application.mod_web.presentable_object import PresentableRecommendedHashtag
from application.mod_web.utils_user_notifications import \
    utils_get_user_notifications_count

from application.mod_api.views_tokens import \
    _api_generate_token, \
    _api_check_if_token_exist


def _render_settings(error=None):
    user_token = flask.request.cookies.get('op_token')
    user_notifications_count = utils_get_user_notifications_count(user_token)

    user_settings = utils_get_user_settings(token=user_token)
    print user_settings
    recommended_hashtags = RecommendedHashtagDAO.get_all()
    p_recommended_hashtags = [PresentableRecommendedHashtag(h) for h in recommended_hashtags]

    return flask.render_template('web/user_settings.html',
        title=u'Ustawienia',
        user_token=user_token,
        user_settings=user_settings,
        p_recommended_hashtags=p_recommended_hashtags,
        user_notifications_count=user_notifications_count,
        error=error)


@app.route('/ustawienia', methods=['GET'])
def show_user_settings():
    return _render_settings(error=None)


@app.route('/ustawienia/token/generuj', methods=['GET'])
def generate_token(redirect_to=None):
    user_token = None
    response_token, success = _api_generate_token()
    if success == 201:
        response_json = json.loads(response_token.data)['token']
        user_token = response_json['value']

        response = None
        if redirect_to is None:
            response = app.make_response(flask.redirect(flask.url_for('show_user_settings')))
        else:
            response = app.make_response(flask.redirect(redirect_to))

        response.set_cookie('op_token', user_token)
        return response
    else:
        return _render_settings(error="Nie udało się wygenerować \
            nowego tokena. Spróbuj ponownie.")

@app.route('/ustawienia/token/uzyj', methods=['POST'])
def change_token():
    user_op_token = flask.request.form.get('user_op_token', None, type=str)
    response_check, success = _api_check_if_token_exist(value=user_op_token)
    if success == 200:
        # Change only to token if it exists (in db), do not allow to pass custom ones
        if json.loads(response_check.data)['exists'] is True:
            response = app.make_response(flask.redirect(flask.url_for('show_user_settings')))
            response.set_cookie('op_token', user_op_token)
            return response

    # If error during changing token
    return _render_settings(error="Nie udało się zmienić tokena. \
        Upewnij się, że jest poprawny lub wygeneruj nowy.")
