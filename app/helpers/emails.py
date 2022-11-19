import smtplib
from os import environ
import datetime

class Emails:
    def __init__(self):
        self.email = environ.get("SMTP_EMAIL")

    def send_email(self, content):
        try:
            server_ssl = smtplib.SMTP_SSL(environ.get("SMTP_HOST"), environ.get("SMTP_PORT"))
            server_ssl.login(environ.get('SMTP_EMAIL'), environ.get('SMTP_PASSWORD'))
            server_ssl.sendmail(environ.get('SMTP_EMAIL'), self.email, content)
            server_ssl.close()
        except Exception as e:
            raise Exception(e)

    def players_update(self, amount_of_players):
        to = self.email
        subject = 'Player Database Updated'
        body = f'Player Database Updated with {amount_of_players} players. Completed time: {datetime.datetime.now()}'
        content = f'Subject: {subject}\n\n{body}'

        self.send_email(content)

    def unknown_cards(self):
        to = self.email
        subject = 'Unknown cards found'
        body = f'Unknown cards found. Please check database and update cards.'
        content = f'Subject: {subject}\n\n{body}'

        self.send_email(content)

    def exception_occurred(self, exception):
        to = self.email
        subject = 'Exception occurred'
        body = f'Exception occurred: {exception}. Time: {datetime.datetime.now()}'
        content = f'Subject: {subject}\n\n{body}'

        self.send_email(content)