"""Query influxdb"""

from influxdb import InfluxDBClient

from config import CONFIG


class Query(object):
    """The influxdb Query class"""

    def __init__(self):
        self.client = InfluxDBClient(
            CONFIG.get('influxdb', 'INFLUX_HOST'),
            CONFIG.get('influxdb', 'INFLUX_PORT'),
            CONFIG.get('influxdb', 'INFLUX_USER'),
            CONFIG.get('influxdb', 'INFLUX_PASSWORD'),
            CONFIG.get('influxdb', 'INFLUX_DATABASE'),
        )

    def query_last_mean(self, indicator, host, timeframe='10m', filters=None):
        """Get the last mean value of the indicator"""
        if filters is not None:
            filters_str = ' AND '
            for k, v in filters.items():
                filters_str += "%s = '%s'" % (k, v)
            filters_str += ' '
        else:
            filters_str = ''

        query = "select mean(value) from %s where host = '%s' %s \
            and time > now() - %s  group by time(%s) order by time desc limit 1;" % (
                indicator, host, filters_str, timeframe, timeframe
            )
        result = self.client.query(query)

        return next(result[indicator])['mean']
