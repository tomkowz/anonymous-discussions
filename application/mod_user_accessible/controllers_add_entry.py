# -*- coding: utf-8 -*-

import datetime
import flask

from application import app
from application.models.entry import Entry
from application.utils.email_notifier import EmailNotifier
from application.utils.sanitize import Sanitize

@app.route('/add', methods=['GET'])
def add():
    return flask.render_template('user/add_entry.html',
                                  title=u'Nowy wpis', content='')

@app.route('/add', methods=['POST'])
def add_post():
    content = flask.request.form['content']
    valid_content, error = _is_entry_content_valid(content)
    success = None

    if valid_content:
        # Insert entry
        entry = Entry()
        entry.content = content
        entry.created_at = datetime.datetime.utcnow()
        entry.save()

        if entry is None:
            error = 'Nie udało się dodać wpisu. Spróbuj ponownie.'
        else:
            EmailNotifier.notify_about_new_post()
            content = '' # reset content so user does not see sent message anymore
            success = 'Wpis został dodany pomyślnie. Obecnie wszystkie wpisy \
                       podlegają moderacji, aczkolwiek powinien pojawić się on \
                       niebawem. Więcej informacji w FAQ.'

    return flask.render_template('user/add_entry.html',
                                  title=u'Nowy wpis',
                                  content=content,
                                  error=error,
                                  success=success)

def _is_entry_content_valid(content):
    char_len = (10, 500)

    valid_content, invalid_symbol = Sanitize.is_valid_input(content)
    if valid_content == False:
        return False, 'Wpis zawiera niedozwolone elementy: {}'.format(invalid_symbol)
    elif len(content) < char_len[0]:
        return False, 'Wpis jest zbyt krótki.'
    elif len(content) > char_len[1]:
        return False, 'Wpis jest zbyt długi (max. {} znaków).'.format(max_len)

    return True, None
