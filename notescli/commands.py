import config
import cliparser
import indexer
import io
import os

def command_ls(index):
  with index.searcher() as searcher:
    results = searcher.documents()
    print "Indexed files:"
    for result in results:
      print result["filename"]

def command_view(index, query):
  result_file = indexer.find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    print open(result_file).read()

def command_add(config, filename):
  full_path = os.path.join(config.notes_path, filename)
  io.edit_file(full_path)
  print "Added", full_path

def command_edit(index, query):
  result_file = indexer.find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    io.edit_file(result_file)

def command_rm(index, query):
  result_file = indexer.find_result(index, query)
  if result_file is None:
    print "No results found"
  else:
    print "Are you sure you want to delete %s? (y/n)" % result_file
    choice = io.get_choice()
    if choice == "y":
      os.remove(result_file)

def command_reindex(config):
  indexer.reindex(config)
