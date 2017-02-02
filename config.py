"""Config module"""

from configparser import SafeConfigParser

CONFIG = SafeConfigParser()

def read_config(config_file):
    CONFIG.read(config_file)
