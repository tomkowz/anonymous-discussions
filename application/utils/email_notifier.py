# -*- coding: utf-8 -*-

import requests #mailgun

from email.mime.text import MIMEText

class EmailNotifier:

    @staticmethod
    def notify_about_new_post():
        notification_email = 'notification@spowiedzwszafie.pl'
        key = 'key-834b6ffa64e1d46bc418369d7c25c88a'
        sandbox = 'sandboxea724f4294444c2fbc6090aa621fdcc7.mailgun.org'
        recipient = notification_email

        request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
        request = requests.post(request_url, auth=('api', key), data={
            'from': notification_email,
            'to': 'spowiedzwszafie@gmail.com',
            'subject': 'Nowy wpis oczekuje na moderację.',
            'text': 'Nowy wpis oczekuje na moderację - http://spowiedzwszafie.pl/admin/login'
        })

        # print 'Status: {0}'.format(request.status_code)
        # print 'Body:   {0}'.format(request.text)
