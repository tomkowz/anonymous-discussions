# -*- coding: utf-8 -*-

import flask, json

from application import app
from application.mod_api.views_tokens import \
    _api_generate_token, \
    _api_check_if_token_exist

from application.mod_web.utils_user_notifications import \
    utils_get_user_notifications_count

@app.route('/ustawienia/twoj_token', methods=['GET'])
def show_your_token_settings():
    user_token = flask.request.cookies.get('op_token', None)
    return _render_view(user_token=user_token, error=None)


@app.route('/token/generuj', methods=['GET'])
def generate_token(redirect_to=None):
    user_token = None
    response_token, success = _api_generate_token()
    if success == 201:
        response_json = json.loads(response_token.data)['token']
        user_token = response_json['value']

        response = None
        if redirect_to is None:
            response = app.make_response(flask.redirect(flask.url_for('show_your_token_settings',
                user_token=user_token)))
        else:
            response = app.make_response(flask.redirect(redirect_to))

        response.set_cookie('op_token', user_token)
        return response
    else:
        return _render_view(user_token=flask.request.cookies.get('op_token', None),
                    error="Nie udało się wygenerować nowego tokena. Spróbuj ponownie." )


@app.route('/token/zmien', methods=['POST'])
def change_token():
    user_op_token = flask.request.form.get('user_op_token', None, type=str)
    response_check, success = _api_check_if_token_exist(value=user_op_token)
    if success == 200:
        # Change only to token if it exists (in db), do not allow to pass custom ones
        if json.loads(response_check.data)['exists'] is True:
            response = app.make_response(flask.redirect(flask.url_for('show_your_token_settings',
                user_token=user_op_token,
                error=None)))
            response.set_cookie('op_token', user_op_token)
            return response

    # If error during changing token
    return  _render_view(user_token=flask.request.cookies.get('op_token', None),
                error="Nie udało się zmienić tokena. Upewnij się, że jest \
                    poprawny lub wygeneruj nowy.")


def _render_view(user_token=None, error=None):
    user_notifications_count = utils_get_user_notifications_count(user_token)
    return flask.render_template('web/token_management.html',
        title=u'Twój token',
        user_token=user_token,
        user_notifications_count=user_notifications_count,
        error=error)
