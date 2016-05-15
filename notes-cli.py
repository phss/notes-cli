import argparse
import yaml
import shutil
import os
from subprocess import call
from os.path import expanduser, isdir
import whoosh.index as ix
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm, Term, Or

EDITOR = os.environ.get('EDITOR','vim')

def command_ls(index):
  with index.searcher() as searcher:
    results = searcher.documents()
    print "Indexed files:"
    for result in results:
      print result["filename"]

def find_result(index, query):
  with index.searcher() as searcher:
    terms = [FuzzyTerm("content", word, maxdist=2) for word in query]
    search_query = Or(terms)
    results = searcher.search(search_query)
    if len(results) == 0:
      return None
    elif len(results) == 1:
      result = results[0]
    else:
      print "Options:"
      for i, result in enumerate(results):
        print "%d) %s" % (i+1, result["filename"])
      print "Which one?"
      choice = int(input()) - 1
      result = results[choice]
    return result["filename"]

def command_view(index, query):
  result_file = find_result(index, query)
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

def load_config_from(path):
  with open(expanduser(path)) as file:
    return yaml.load(file)

def parse_options():
  parser = argparse.ArgumentParser()
  parser.add_argument("command",
                      choices=["ls", "add", "rm", "edit", "view", "reindex"])
  parser.add_argument("query", nargs="*")
  parser.add_argument("--file")
  return parser.parse_args()

def create_or_load_index(index_path, notes_path):
  if isdir(index_path):
    return ix.open_dir(index_path)
  else:
    return command_reindex(index_path, notes_path)

def main():
  config = load_config_from("~/.notes-cli/config.yaml")
  index_path = expanduser(config["indexdir"])
  notes_path = expanduser(config["notesdir"])
  options = parse_options()
  index = create_or_load_index(index_path, notes_path)
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
