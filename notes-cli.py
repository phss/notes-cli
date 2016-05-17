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

EDITOR = os.environ.get('EDITOR','vim')


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

def edit_file(full_path):
  preread = ""
  if os.path.isfile(full_path):
    preread = open(full_path, "r").read()
  with open(full_path, "w") as f:
    f.write(preread)
    f.flush()
    call([EDITOR, f.name])

def command_add(index, notes_path, filename):
  full_path = os.path.join(notes_path, filename)
  edit_file(full_path)
  print "Added", full_path

def command_edit(index, query):
  result_file = find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    edit_file(result_file)

def command_rm(index, query):
  result_file = find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    print "Are you sure you want to delete %s? (y/n)" % result_file
    choice = notescli.io.get_choice()
    if choice == "y":
      os.remove(result_file)

def command_reindex(index_path, notes_path):
  shutil.rmtree(index_path, True)
  os.mkdir(index_path)
  schema = Schema(filename=TEXT(stored=True), content=TEXT)
  index = ix.create_in(index_path, schema)
  writer = index.writer()
  for note in os.listdir(notes_path):
    note_full_path = os.path.join(notes_path, note)
    with open(note_full_path) as note_file:
      writer.add_document(filename=unicode(note_full_path, "utf-8"), content=unicode(note_file.read(), "utf-8"))
  writer.commit()
  return index

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
