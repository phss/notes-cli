import argparse
import yaml
import shutil
import os
from os.path import expanduser, isdir
import whoosh.index as ix
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm, Term, Or

def command_ls(index):
  with index.searcher() as searcher:
    results = searcher.documents()
    print "Indexed files:"
    for result in results:
      print result["filename"]

def command_view(index, query):
  with index.searcher() as searcher:
    terms = [FuzzyTerm("content", word, maxdist=2) for word in query.split()]
    search_query = Or(terms)
    results = searcher.search(search_query)
    if len(results) == 0:
      print "No results found"
    else:
      result = results[0]
      print open(result["filename"]).read()

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
  parser.add_argument("--query")
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
  elif options.command == "reindex":
    command_reindex(index_path, notes_path)
  else:
    print "Not supported"

if __name__ == "__main__":
  main()
