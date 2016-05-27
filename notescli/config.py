import yaml
from os.path import expanduser
from collections import namedtuple

Config = namedtuple("Config", "indexdir notesdir")

def load_config(path):
  with open(expanduser(path)) as file:
    config_dict = yaml.load(file)
    return Config(config_dict["indexdir"], config_dict["notesdir"])

