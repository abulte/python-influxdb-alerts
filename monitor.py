"""Monitoring CLI"""

from importlib import import_module

import click

from config import CONFIG

HOSTS = str(CONFIG.get('general', 'HOSTS')).split(',')

INDICATOR_MODULE = import_module('indicators')
INDICATORS_CLASSES = str(CONFIG.get('general', 'INDICATORS')).split(',')
INDICATORS = [getattr(INDICATOR_MODULE, c_name)() for c_name in INDICATORS_CLASSES]

ALERTER_MODULE = import_module('alerters')
ALERTERS_CLASSES = str(CONFIG.get('general', 'ALERTERS')).split(',')
ALERTERS = [getattr(ALERTER_MODULE, c_name)() for c_name in ALERTERS_CLASSES]


@click.group()
def cli():
    pass

@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Output indicator value to console.')
def run(verbose):
    """Parse indicator values and alert if needed"""
    for indicator in INDICATORS:
        for host in HOSTS:
            value = indicator.get_value(host)
            alert = indicator.is_alert(host, value=value)
            if alert:
                for alerter in ALERTERS:
                    alerter.send(indicator, host, value)

            if verbose:
                prefix = '[%s](%s)' % (indicator.name.upper(), host)
                value_str = 'Value: %s' % value
                alert_str = 'Alert: %s' % ('on' if alert else 'off')
                click.echo(prefix.ljust(40) + value_str.ljust(30) + alert_str.ljust(30))

@cli.command()
def test_email():
    """Test sending email"""
    from alerters import MailAlerter
    from indicators import FreeRAMIndicator
    mail = MailAlerter()
    mail.send(FreeRAMIndicator(), 'test.host', 0)

@cli.command()
def test_slack():
    """Test sending slack message"""
    from alerters import SlackAlerter
    from indicators import FreeRAMIndicator
    slack = SlackAlerter()
    slack.send(FreeRAMIndicator(), 'test.host', 0)

if __name__ == '__main__':
    cli()
