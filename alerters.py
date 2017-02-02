"""Alerter module"""

import smtplib
from email.mime.text import MIMEText

import click
from slacker import Slacker

from config import CONFIG


class SlackAlerter(object):
    """SlackAlerter class"""

    def __init__(self):
        token = CONFIG.get('slack', 'API_TOKEN')
        self.slack = Slacker(token)
        self.channel = CONFIG.get('slack', 'CHANNEL')


    def send(self, indicator, host, value):
        """Send a slack alert"""
        message = """Monitoring alert for *%(host)s*. Indicator `%(indicator)s` is %(comparison)s threshold.
Value: `%(value).2f%(unit)s`, threshold: `%(threshold)s%(unit)s`.""" % {
            'host': host,
            'indicator': indicator.name.upper(),
            'comparison': 'above' if indicator.comparison == 'gt' else 'below',
            'value': value,
            'threshold': indicator.threshold,
            'unit': indicator.unit
        }

        try:
            self.slack.chat.post_message('#%s' % self.channel, message)
        except Exception as e:
            click.secho('Slack send error: %s' % e, fg='red')


class MailAlerter(object):
    """MailAlerter class"""

    def __init__(self):
        self.smtp_host = CONFIG.get('mail', 'SMTP_HOST')

    def send(self, indicator, host, value):
        """Send an email alert"""
        msg = MIMEText("""
Monitoring alert for %(host)s. Indicator %(indicator)s is %(comparison)s threshold.
Value: %(value).2f%(unit)s, threshold: %(threshold)s%(unit)s.""" % {
            'host': host,
            'indicator': indicator.name.upper(),
            'comparison': 'above' if indicator.comparison == 'gt' else 'below',
            'value': value,
            'threshold': indicator.threshold,
            'unit': indicator.unit
        })
        msg['Subject'] = '[%s] Monitoring alert for %s' % (
            host,
            indicator.name.upper()
        )
        smtp_i = None
        try:
            smtp_i = smtplib.SMTP(self.smtp_host)
            smtp_i.sendmail(
                CONFIG.get('mail', 'MAIL_FROM'),
                str(CONFIG.get('mail', 'MAIL_TO')).split(','),
                msg.as_string()
            )
        except Exception as e:
            click.secho('Mail send error: %s' % e, fg='red')
        finally:
            if smtp_i:
                smtp_i.quit()
