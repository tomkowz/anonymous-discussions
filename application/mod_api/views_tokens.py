# -*- coding: utf-8 -*-

import flask, uuid

from application import app
from application.mod_api.models_token import Token
from application.mod_api.utils_params import \
    _is_user_op_token_param_valid, \
    _create_invalid_param_error_message

@app.route('/_api/tokens/<string:value>', methods=['GET'])
def _api_check_if_token_exist(value):
    checks = {'value': _is_user_op_token_param_valid(value)}
    if _create_invalid_param_error_message(checks) is not None:
        return flask.jsonify({'error': 'Niepoprawne parametry'}), 400

    exist = Token.get_with_value(value) is not None
    return flask.jsonify({'exists': exist}), 200

@app.route('/_api/tokens/generate', methods=['GET'])
def _api_generate_token():
    t_str = uuid.uuid4()
    token = Token(value=t_str)
    token.save()
    return flask.jsonify({'token': token.to_json()}), 201
