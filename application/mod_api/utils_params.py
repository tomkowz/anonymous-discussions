# -*- coding: utf-8 -*-
import flask, json

from application.utils.sanitize_services import Sanitize

def _is_hashtag_param_valid(hashtag):
    if hashtag is not None and \
        Sanitize.is_valid_input(hashtag) is False:
        return False
    return True

def _is_order_by_param_valid(order_by):
    if order_by is not None and order_by != "votes_up desc":
        return False
    return True

def _is_user_op_token_param_valid(user_op_token):
    if user_op_token is not None and \
        Sanitize.is_valid_input(user_op_token) is False:
        return False
    return True

def _is_per_page_param_valid(per_page):
    if per_page is None or per_page == 0:
        return False
    return True

def _is_page_number_param_valid(page_number):
    if page_number is None or page_number == 0:
        return False
    return True

def _is_entry_id_param_valid(entry_id):
    return True if entry_id is not None else False

def _is_comments_order_param_valid(comments_order):
    if comments_order is None or Sanitize.is_valid_input(comments_order) is False:
        return False
    return True

def _is_content_param_valid(content):
    if content is None or Sanitize.is_valid_input(content) is False:
        return False
    return True

def _create_invalid_param_error_message(checks=dict()):
    for (k, is_valid) in checks.items():
        if is_valid is False:
            error = "Niepoprawna wartość parametru {}".format(k)
            return flask.jsonify({'error:': error}), 400
    return None

def _get_value_for_key_if_none(value, key, type):
    if value is None: # GET
        value = flask.request.args.get(key, None, type=type)

    if value is None: # POST
        value = flask.request.form.get(key, None, type=type)

    if value is None:
        try:
            value = json.loads(flask.request.data)[key]
        except:
            pass
    return value

def _is_entry_content_valid(content):
    char_len = (40, 3000)
    content_valid, invalid_symbol = Sanitize.is_valid_input(content)
    if content_valid == False:
        return False, 'Wpis zawiera niedozwolone elementy: {}'.format(invalid_symbol)
    elif len(content) < char_len[0]:
        return False, 'Wpis ma za mało znaków. Minimum {}'.format(char_len[0])
    elif len(content) > char_len[1]:
        return False, 'Wpis jest zbyt długi (max. {} znaków).'.format(char[1])

    return True, None

def _is_comment_content_valid(content):
    char_len = (5, 3000)

    content_valid, invalid_symbol = Sanitize.is_valid_input(content)
    if content_valid == False:
        return False, 'Komentarz zawiera niedozwolone elementy: {}'.format(invalid_symbol)
    elif len(content) < char_len[0]:
        return False, 'Komentarz ma za mało znaków. Minimum {}'.format(char_len[0])
    elif len(content) > char_len[1]:
        return False, 'Komentarz jest zbyt długi (max. {} znaków).'.format(char_len[1])

    return True, None
