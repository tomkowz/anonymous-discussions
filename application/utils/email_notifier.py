# -*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText

class EmailNotifier:

    @staticmethod
    def notify_about_new_post():
        msg = MIMEText('Nowy wpis oczekuje na moderację.')
        msg['Subject'] = 'spowiedzwszafie.pl - nowy wpis'
        msg['From'] = 'noreply@spowiedzwszafie.pl'
        msg['To'] = 'mail+spowiedzwszafie@szulctomasz.com'

        try:
            s = smtplib.SMTP('localhost')
            s.sendemail(msg['From'], [msg['To']], msg.as_string())
            s.quit()
        except:
            print 'Cannot send email about new post.'
