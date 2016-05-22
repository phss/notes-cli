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
