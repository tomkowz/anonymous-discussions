# -*- coding: utf-8 -*-

import datetime, flask

from application import app
from application.mod_api.models_entry import Entry
from application.mod_api.models_comment import Comment
from application.utils.sanitize_services import Sanitize

@app.route('/api/vote', methods=['GET'])
def api_vote():
    object_type = flask.request.args.get('object_type', None)
    object_id = flask.request.args.get('object_id', None)
    value = flask.request.args.get('value', None) # up, down

    is_object_type_valid = Sanitize.is_valid_input(object_type)
    is_object_id_valid = Sanitize.is_valid_input(object_id)
    is_value_valid = Sanitize.is_valid_input(value)

    if is_object_type_valid is False or \
        is_object_id_valid is False or \
        is_value_valid is False:
        return flask.jsonify({'error': 'input is not valid'}), 400

    if object_type == 'entry':
        Entry.vote(object_id, value)
        e = Entry.get_with_id(object_id)
        return flask.jsonify({'up': e.votes_up, 'down': e.votes_down}), 200
    elif object_type == 'comment':
        Comment.vote(object_id, value)
        c = Comment.get_with_id(object_id)
        return flask.jsonify({'up': c.votes_up, 'down': c.votes_down}), 200
    else:
        return flask.jsonify({'error': 'invalid object type'}), 400
