# -*- coding: utf-8 -*-

import flask, json

from application import app
from application.mod_api.views_tokens import _api_generate_token

@app.route('/token/new', methods=['GET'])
def generate_token():
    response = app.make_response(flask.redirect(flask.url_for('main')))

    response_token, success = _api_generate_token()
    if success == 201:
        response_json = json.loads(response_token.data)['token']
        response.set_cookie('op_token', response_json['value'])

    return response
