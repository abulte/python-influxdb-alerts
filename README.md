# python-influxdb-alerts

An extensible and configurable script to send some alerts (email and/or slack ATM) when a measurement in your InfluxDB database is reaching or falling below a defined threshold.

Tested on Python `2.7` and `3.6`.

## Installation

This project uses [Pipenv](http://docs.pipenv.org/en/latest/).

```
pipenv install
```

Alternatively, you can extract the dependencies from `Pipfile` and install them via pip.

## Configuration

```
cp settings-example.cfg settings.cfg
```

Then edit this file to configure the script.

## Usage

This tool is meant to be run via cron quite frequently (eg 10 min).

```
python monitor.py run
```

## Commands

Specify a config file path.

```
python monitor.py run -c other-settings.cfg
```

Run with measurement output.

```
python monitor.py run --verbose
```

Send a test email.

```
python monitor.py test_email
```

Send a test slack message.

```
python monitor.py test_slack
```
