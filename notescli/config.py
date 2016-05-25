import yaml
from os.path import expanduser

def load_config(path):
  with open(expanduser(path)) as file:
    return yaml.load(file)
