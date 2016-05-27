import argparse
import yaml
import shutil
import os
from subprocess import call
from os.path import expanduser, isdir

import config
import cliparser
import indexer
import io
import commands


def main():
  conf = config.load_config("~/.notes-cli/config.yaml")
  index_path = conf.indexdir
  notes_path = conf.notesdir
  options = cliparser.parse_options()
  index = indexer.create_or_load_index(index_path, notes_path)
  if options.command == "ls":
    commands.command_ls(index)
  elif options.command == "view":
    commands.command_view(index, options.query)
  elif options.command == "add":
    commands.command_add(index, notes_path, options.file)
    commands.command_reindex(index_path, notes_path)
  elif options.command == "edit":
    commands.command_edit(index, options.query)
    commands.command_reindex(index_path, notes_path)
  elif options.command == "rm":
    commands.command_rm(index, options.query)
    commands.command_reindex(index_path, notes_path)
  elif options.command == "reindex":
    commands.command_reindex(index_path, notes_path)
  else:
    print "Not supported"

if __name__ == "__main__":
  main()
