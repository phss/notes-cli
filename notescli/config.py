import yaml
from os.path import expanduser
from collections import namedtuple

Config = namedtuple("Config", "indexdir notesdir")

def load_config(path):
  with open(expanduser(path)) as file:
    config_dict = yaml.load(file)
    return Config(expanduser(config_dict["indexdir"]),
                  expanduser(config_dict["notesdir"]))

