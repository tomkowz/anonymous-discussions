# -*- coding: utf-8 -*-

import flask, json

from application import app
from application.mod_api.views_tokens import \
    _api_generate_token, \
    _api_check_if_token_exist


@app.route('/token/generuj', methods=['GET'])
def generate_token():
    response = app.make_response(flask.redirect(flask.url_for('main')))

    response_token, success = _api_generate_token()
    if success == 201:
        response_json = json.loads(response_token.data)['token']
        response.set_cookie('op_token', response_json['value'])

    return response


@app.route('/token/zmien', methods=['POST'])
def change_token():
    user_op_token = flask.request.form.get('user_op_token', None, type=str)
    response = app.make_response(flask.redirect(flask.url_for('main')))

    if user_op_token is not None:
        response_check, success = _api_check_if_token_exist(value=user_op_token)
        if success == 200:
            if json.loads(response_check.data)['exists'] is True:
                response.set_cookie('op_token', user_op_token)

    return response
