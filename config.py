"""Config module"""

from configparser import SafeConfigParser

CONFIG = SafeConfigParser()
CONFIG.read('settings.cfg')
