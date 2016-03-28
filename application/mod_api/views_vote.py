# -*- coding: utf-8 -*-

import datetime, flask

from application import app
from application.mod_api.models_entry import Entry, EntryDAO
from application.mod_api.models_comment import Comment, CommentDAO
from application.utils.sanitize_services import Sanitize
from application.mod_api.models_tokens_votes_cache import TokensVotesCacheItem, TokensVotesCacheDAO

from application.mod_api.utils_params import \
    _get_value_for_key_if_none, \
    _create_invalid_param_error_message, \
    _is_user_op_token_param_valid


@app.route('/api/vote', methods=['POST'])
def api_vote(user_token=None, object_id=None, object_type=None, value=None):
    # Get params
    if user_token is None:
        user_token = _get_value_for_key_if_none(user_token, 'user_token', str)

    if object_type is None:
        object_type = _get_value_for_key_if_none(object_type, 'object_type', str)

    if object_id is None:
        try:
            object_id = int(_get_value_for_key_if_none(object_id, 'object_id', int))
        except:
            pass

    if value is None:
        value = _get_value_for_key_if_none(value, 'value', str)

    # Check params
    err_msg = _create_invalid_param_error_message({
        'user_token': _is_user_op_token_param_valid(user_token),
        'object_type': _is_object_type_param_valid(object_type),
        'object_id': _is_object_id_param_valid(object_id),
        'value': _is_value_param_valid(value)
    })
    if err_msg is not None:
        return err_msg

    # Check whether voted object exists.
    success, error = _does_object_exist(object_id=object_id,
                                        object_type=object_type)
    if success is False:
        return flask.jsonify({'error': error}), 400

    # Check whether user voted already for this item
    if TokensVotesCacheDAO.get_vote(user_token=user_token,
                                    object_id=object_id,
                                    object_type=object_type) is not None:
        return flask.jsonify({'error': 'Głos został już oddany wcześniej'}), 400

    # Cache vote
    TokensVotesCacheDAO.set_vote(user_token=user_token,
                              object_id=object_id,
                              object_type=object_type,
                              value=value)

    # Perform vote
    if object_type == 'entry':
        if value == 'up':
            EntryDAO.vote_up(entry_id=object_id)
        else:
            EntryDAO.vote_down(entry_id=object_id)

        e = EntryDAO.get_entry(object_id, cur_user_token=user_token)
        return flask.jsonify({'up': e.votes_up, 'down': e.votes_down}), 200
    elif object_type == 'comment':
        if value == 'up':
            CommentDAO.vote_up(comment_id=object_id)
        else:
            CommentDAO.vote_down(comment_id=object_id)

        c = CommentDAO.get_comment(object_id, cur_user_token=user_token)
        return flask.jsonify({'up': c.votes_up, 'down': c.votes_down}), 200
    else: # never happen
        return flask.jsonify({'error': 'Nieprawidłowy typ obiektu'}), 400

def _is_object_type_param_valid(object_type):
    if (object_type in ['entry', 'comment']) is True:
        valid, _ = Sanitize.is_valid_input(object_type)
        return valid
    return False

def _is_object_id_param_valid(object_id):
    return isinstance(object_id, int) == True

def _is_value_param_valid(value):
    if (value in ['up', 'down']) is True:
        valid, _ = Sanitize.is_valid_input(value)
        return valid
    return False

def _does_object_exist(object_id, object_type):
    if object_type == 'entry':
        if EntryDAO.get_entry(object_id, cur_user_token='') is None:
            return False, 'Taki wpis nie istnieje'
    elif object_type == 'comment':
        if CommentDAO.get_comment(object_id, cur_user_token='') is None:
            return False, 'Taki komentarz nie istnieje'
    else:
        return False, None
    return True, None
