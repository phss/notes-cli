import argparse
import yaml
import os
from os.path import expanduser, isdir
import whoosh.index as ix
from whoosh.fields import *


def load_config_from(path):
  with open(expanduser(path)) as file:
    return yaml.load(file)

def parse_options():
  parser = argparse.ArgumentParser()
  parser.add_argument("command",
                      choices=["ls", "add", "rm", "edit", "view", "reindex"])
  parser.add_argument("--query")
  return parser.parse_args()

def create_or_load_index(index_path):
  index_full_path = expanduser(index_path)
  if isdir(index_full_path):
    return ix.open_dir(index_full_path)
  else:
    os.mkdir(index_full_path)
    schema = Schema(filename=TEXT(stored=True), content=TEXT)
    return ix.create_in(index_full_path, schema)

def main():
  config = load_config_from("~/.notes-cli/config.yaml")
  options = parse_options()
  index = create_or_load_index(config["indexdir"])
  print options

if __name__ == "__main__":
  main()
