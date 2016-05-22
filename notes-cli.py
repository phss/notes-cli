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

def command_ls(index):
  with index.searcher() as searcher:
    results = searcher.documents()
    print "Indexed files:"
    for result in results:
      print result["filename"]

def command_view(index, query):
  result_file = notescli.indexer.find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    print open(result_file).read()

def command_add(index, notes_path, filename):
  full_path = os.path.join(notes_path, filename)
  notescli.io.edit_file(full_path)
  print "Added", full_path

def command_edit(index, query):
  result_file = notescli.indexer.find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    notescli.io.edit_file(result_file)

def command_rm(index, query):
  result_file = notescli.indexer.find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    print "Are you sure you want to delete %s? (y/n)" % result_file
    choice = notescli.io.get_choice()
    if choice == "y":
      os.remove(result_file)

def command_reindex(index_path, notes_path):
  notescli.indexer.reindex(index_path, notes_path)

def main():
  config = notescli.config.load_config_from("~/.notes-cli/config.yaml")
  index_path = expanduser(config["indexdir"])
  notes_path = expanduser(config["notesdir"])
  options = notescli.cliparser.parse_options()
  index = notescli.indexer.create_or_load_index(index_path, notes_path)
  if options.command == "ls":
    command_ls(index)
  elif options.command == "view":
    command_view(index, options.query)
  elif options.command == "add":
    command_add(index, notes_path, options.file)
    command_reindex(index_path, notes_path)
  elif options.command == "edit":
    command_edit(index, options.query)
    command_reindex(index_path, notes_path)
  elif options.command == "rm":
    command_rm(index, options.query)
    command_reindex(index_path, notes_path)
  elif options.command == "reindex":
    command_reindex(index_path, notes_path)
  else:
    print "Not supported"

if __name__ == "__main__":
  main()
