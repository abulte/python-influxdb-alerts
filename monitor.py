"""Monitoring CLI"""

from importlib import import_module

import click

from config import CONFIG, read_config


def setup(config):
    read_config(config)

    hosts = str(CONFIG.get('general', 'HOSTS')).split(',')

    indicator_module = import_module('indicators')
    indicator_classes = str(CONFIG.get('general', 'indicators')).split(',')
    indicators = [getattr(indicator_module, c_name)() for c_name in indicator_classes]

    alerter_module = import_module('alerters')
    alerter_classes = str(CONFIG.get('general', 'ALERTERS')).split(',')
    alerters = [getattr(alerter_module, c_name)() for c_name in alerter_classes]

    return hosts, indicators, alerters

@click.group()
def cli():
    pass

@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Output indicator value to console.')
@click.option('--config', '-c', default='settings.cfg', help='Path to config file.')
def run(verbose, config):
    """Parse indicator values and alert if needed"""
    hosts, indicators, alerters = setup(config)
    for host in hosts:
        for indicator in indicators:
            alert = False
            value = indicator.get_value(host)
            if value and indicator.is_alert(host, value=value):
                alert = True
                for alerter in alerters:
                    alerter.send(indicator, host, value)

            if verbose:
                prefix = '[%s](%s)' % (indicator.name.upper(), host)
                value_str = 'Value: %s' % value
                alert_str = 'Alert: %s' % ('on' if alert else 'off')
                click.echo(prefix.ljust(40) + value_str.ljust(30) + alert_str.ljust(30))

@cli.command()
@click.option('--config', '-c', default='settings.cfg', help='Path to config file.')
def test_email(config):
    """Test sending email"""
    setup(config)
    from alerters import MailAlerter
    from indicators import FreeRAMIndicator
    mail = MailAlerter()
    mail.send(FreeRAMIndicator(), 'test.host', 0)

@cli.command()
@click.option('--config', '-c', default='settings.cfg', help='Path to config file.')
def test_slack(config):
    """Test sending slack message"""
    setup(config)
    from alerters import SlackAlerter
    from indicators import FreeRAMIndicator
    slack = SlackAlerter()
    slack.send(FreeRAMIndicator(), 'test.host', 0)

if __name__ == '__main__':
    cli()
