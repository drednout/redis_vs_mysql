#!/usr/bin/python
#coding: UTF-8
import logging
import logging.config
import re

try:
    import yaml
except ImportError:
    print("""You have to install PyYAML module. Now it's required
          for config parsing. See http://pyyaml.org/ .""")
    raise

from twisted.internet import reactor, defer



def defer_sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d


def include(loader, node):
    """Include another YAML file."""
    filename = loader.construct_scalar(node)
    data = yaml.load(open(filename))
    return data

def mega_include(config):
    config_as_str = config.read()
    include_list = re.findall('(!mega_include (\S+))', config_as_str)
    logging.debug("include_list is {0}".format(include_list))
    for include_entry in include_list:
        logging.debug("include_entry is {0}".format(include_entry))
        raw_yaml = open(include_entry[1]).read()
        config_as_str = config_as_str.replace(include_entry[0], raw_yaml)
    return config_as_str


def load_config(config_path):
    config_as_str = mega_include(open(config_path))
    yaml.add_constructor('!include', include)
    config = yaml.load(config_as_str)
    return config

