import argparse
import yaml
import shutil
import os
from subprocess import call
from os.path import expanduser, isdir

import notescli.config
import notescli.cliparser
import notescli.indexer
import notescli.io
import notescli.commands


def main():
  config = notescli.config.load_config_from("~/.notes-cli/config.yaml")
  index_path = expanduser(config["indexdir"])
  notes_path = expanduser(config["notesdir"])
  options = notescli.cliparser.parse_options()
  index = notescli.indexer.create_or_load_index(index_path, notes_path)
  if options.command == "ls":
    notescli.commands.command_ls(index)
  elif options.command == "view":
    notescli.commands.command_view(index, options.query)
  elif options.command == "add":
    notescli.commands.command_add(index, notes_path, options.file)
    notescli.commands.command_reindex(index_path, notes_path)
  elif options.command == "edit":
    notescli.commands.command_edit(index, options.query)
    notescli.commands.command_reindex(index_path, notes_path)
  elif options.command == "rm":
    notescli.commands.command_rm(index, options.query)
    notescli.commands.command_reindex(index_path, notes_path)
  elif options.command == "reindex":
    notescli.commands.command_reindex(index_path, notes_path)
  else:
    print "Not supported"

if __name__ == "__main__":
  main()
