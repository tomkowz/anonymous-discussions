# -*- coding: utf-8 -*-

import flask, uuid

from application import app
from application.mod_api.models_token import Token, TokenDAO
from application.mod_api.utils_params import \
    _is_user_op_token_param_valid, \
    _create_invalid_param_error_message


@app.route('/_api/tokens/<string:value>', methods=['GET'])
def _api_check_if_token_exist(value):
    checks = {'value': _is_user_op_token_param_valid(value)}
    if _create_invalid_param_error_message(checks) is not None:
        return flask.jsonify({'error': 'Niepoprawne parametry'}), 400

    exist = TokenDAO.get_token(value) is not None
    return flask.jsonify({'exists': exist}), 200


@app.route('/api/tokens/generate', methods=['GET'])
def api_generate_token():
    t_str = uuid.uuid4()
    TokenDAO.save(t_str)
    return flask.jsonify({'token': TokenDAO.get_token(t_str).to_json()}), 201
