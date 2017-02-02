"""Indicators to monitor"""

import click
from configparser import NoOptionError

from query import Query
from config import CONFIG


class BaseIndicator(object):

    client = Query()
    # name of the metric in influxdb
    name = 'base_indicator'
    # unit (displays in alerts)
    unit = ''
    # alert when value gt (>) than threshold or lt (<)
    comparison = 'gt'
    # timeframe to compute mean of indicator values on
    timeframe = '10m'
    # some filters to pass to the influx db query (where clause)
    filters = None
    # divide the raw value from influx by this (eg convert bytes to Mb, Gb...)
    divider = 1

    def __init__(self):
        try:
            self.threshold = float(CONFIG.get('thresholds', self.name))
        except NoOptionError:
            raise click.ClickException('No threshold configured for indicator %s' % self.name)

    def get_value(self, host):
        """Get the value from influx for this indicator"""
        value = self.client.query_last_mean(
            self.name,
            host,
            timeframe=self.timeframe,
            filters=self.filters
        )
        if value:
            return value / self.divider

    def is_alert(self, host, value=None):
        """Is this indicator in alert state?"""
        value = self.get_value(host) if not value else value
        if self.comparison == 'gt' and value > self.threshold:
            return True
        elif self.comparison == 'lt' and value < self.threshold:
            return True
        else:
            return False


class LoadIndicator(BaseIndicator):

    name = 'load_longterm'
    unit = ''
    comparison = 'gt'
    timeframe = '10m'
    filters = None
    divider = 1


class FreeRAMIndicator(BaseIndicator):

    name = 'memory_value'
    unit = 'Mb'
    comparison = 'lt'
    timeframe = '10m'
    filters = {
        'type_instance': 'free'
    }
    divider = 1000000


class FreeDiskIndicator(BaseIndicator):

    name = 'df_value'
    unit = 'Mb'
    comparison = 'lt'
    timeframe = '10m'
    filters = {
        'type_instance': 'free'
    }
    divider = 1000000
