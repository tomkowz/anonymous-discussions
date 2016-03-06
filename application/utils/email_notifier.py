# -*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText

class EmailNotifier:

    @staticmethod
    def notify_about_new_post():
        email = 'spowiedzwszafie@gmail.com'
        msg = MIMEText('Nowy wpis oczekuje na moderację.')
        msg['Subject'] = 'spowiedzwszafie.pl - nowy wpis'
        msg['From'] = email
        msg['To'] = 'email

        try:
            s = smtplib.SMTP('localhost')
            s.sendemail(email, [email], msg.as_string())
            s.quit()
        except:
            print 'Cannot send email about new post.'
