# -*- coding: utf-8 -*-

import flask

from application import app
from application.models.entry import Entry
from application.utils.date_utils import DateUtils
from application.utils.email_notifier import EmailNotifier

@app.route('/add', methods=['GET'])
def add():
    return flask.render_template('user/add_entry.html', title=u'Nowy wpis', content='')

@app.route('/add', methods=['POST'])
def add_post():
    content = flask.request.form['content']
    min_len = 10
    max_len = 500

    if len(content) < min_len:
        error = u'Wpis jest zbyt krótki (min. {} znaków).'.format(min_len)
    elif len(content) > max_len:
        error = u'Wpis jest zbyt długi (max. {} znaków).'.format(max_len)
    else:
        # Insert entry
        entry = Entry()
        entry.content = content
        entry.timestamp = DateUtils.timestamp_for_now()

        entry.save()

        if entry is not None:
            EmailNotifier.notify_about_new_post()
            return flask.render_template('user/add_entry.html',
                                         title=u'Nowy wpis',
                                         content='',
                                         success='Wpis został dodany pomyślnie. \
                                            Obecnie wszystkie wpisy podlegają moderacji, \
                                            aczkolwiek powinien pojawić się on niebawem. \
                                            Więcej informacji w FAQ.')
        else:
            error = u'Nie udało się dodać wpisu. Spróbuj ponownie.'

    return flask.render_template('user/add_entry.html',
                                 title=u'Nowy wpis',
                                 content=content,
                                 error=error)
