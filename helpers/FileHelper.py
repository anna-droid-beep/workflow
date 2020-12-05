"""
Helper file for file utilities.
"""
from collections import namedtuple
import json
import logging

log = logging.getLogger(__name__)


def load_config(config_path):
    log.info(f"Loading configuration file from {config_path}")
    with open(config_path, 'rt') as f:
        config = json.load(f)
        config = namedtuple('Configuration', config.keys())(*config.values())
    return config

