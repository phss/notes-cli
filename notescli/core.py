import argparse
import yaml
import shutil
import os
from subprocess import call
from os.path import expanduser, isdir

from config import load_config
import cliparser
import indexer
import io
import commands


def main():
  config = load_config("~/.notes-cli/config.yaml")
  options = cliparser.parse_options()
  index = indexer.create_or_load_index(config)
  if options.command == "ls":
    commands.command_ls(index)
  elif options.command == "view":
    commands.command_view(index, options.query)
  elif options.command == "add":
    commands.command_add(config, options.file)
  elif options.command == "edit":
    commands.command_edit(index, options.query)
  elif options.command == "rm":
    commands.command_rm(index, options.query)
  elif options.command == "reindex":
    commands.command_reindex(config)
  else:
    print "Not supported"

if __name__ == "__main__":
  main()
