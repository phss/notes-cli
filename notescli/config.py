import yaml
from os.path import expanduser

def load_config_from(path):
  with open(expanduser(path)) as file:
    return yaml.load(file)
