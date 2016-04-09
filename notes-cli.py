import argparse
import yaml
from os.path import expanduser


def load_config_from(path):
  with open(expanduser(path)) as file:
    return yaml.load(file)

def parse_options():
  parser = argparse.ArgumentParser()
  parser.add_argument("command",
                      choices=["ls", "add", "rm", "edit", "view", "reindex"])
  parser.add_argument("--query")
  return parser.parse_args()

def main():
  config = load_config_from("~/.notes-cli/config.yaml")
  options = parse_options()
  print options

if __name__ == "__main__":
  main()
