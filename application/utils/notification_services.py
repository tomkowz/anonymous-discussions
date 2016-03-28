# -*- coding: utf-8 -*-

import requests #mailgun

from email.mime.text import MIMEText


class EmailNotifier:

    @staticmethod
    def notify_new_entry(entry_url):
        subject = 'Nowy wpis'
        message = 'Link do nowego wpisu: http://spowiedzwszafie.pl{}'.format(entry_url)
        EmailNotifier._send(subject, message)


    @staticmethod
    def notify_new_comment(entry_url):
        subject = 'Nowy komentarz'
        message = 'Link do nowego wpisu: http://spowiedzwszafie.pl{}'.format(entry_url)
        EmailNotifier._send(subject, message)


    @staticmethod
    def _send(subject, message):
        notification_email = 'notification@spowiedzwszafie.pl'
        key = 'key-834b6ffa64e1d46bc418369d7c25c88a'
        sandbox = 'sandboxea724f4294444c2fbc6090aa621fdcc7.mailgun.org'
        recipient = notification_email

        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
        request = requests.post(request_url, auth=('api', key), data={
            'from': notification_email,
            'to': 'spowiedzwszafie@gmail.com',
            'subject': subject,
            'text': message
        })
