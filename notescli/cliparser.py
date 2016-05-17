import argparse

def parse_options():
  parser = argparse.ArgumentParser()
  parser.add_argument("command",
                      choices=["ls", "add", "rm", "edit", "view", "reindex"])
  parser.add_argument("query", nargs="*")
  parser.add_argument("--file")
  return parser.parse_args()
