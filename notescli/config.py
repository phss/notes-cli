import yaml
from os.path import expanduser
from collections import namedtuple

Config = namedtuple("Config", "indexdir notesdir")

def load_config(path):
  with open(expanduser(path)) as file:
    expand_dict = lambda key: expanduser(config_dict[key])
    config_dict = yaml.load(file)
    return Config(expand_dict("indexdir"), expand_dict("notesdir"))

