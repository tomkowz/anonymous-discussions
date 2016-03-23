# -*- coding: utf-8 -*-

import datetime
import flask

from application import app
from application.mod_core.models_entry import Entry
from application.mod_core.models_comment import Comment
from application.utils.sanitize_services import Sanitize

@app.route('/_votebox')
def votebox():
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
        up, down = Entry.votes_with_id(object_id)
        return flask.jsonify({'up': up, 'down': down}), 200
    elif object_type == 'comment':
        Comment.vote(object_id, value)
        up, down = Comment.votes_with_id(object_id)
        return flask.jsonify({'up': up, 'down': down}), 200
    else:
        return flask.jsonify({'error': 'invalid object type'}), 400
