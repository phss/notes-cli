import config
import cliparser
import io
import os

def command_ls(index):
  print "Indexed files:"
  for filename in index.list_files():
    print filename

def command_view(index, query):
  _search_and_do(index, query, io.print_file)

def command_add(config, filename):
  # TODO: add better error for not specifying param
  full_path = os.path.join(config.notes_path, filename)
  io.edit_file(full_path)
  print "Added", full_path

def command_edit(index, query):
  _search_and_do(index, query, io.edit_file)

def command_rm(index, query):
  _search_and_do(index, query, io.delete_file)

def _search_and_do(index, query, action):
  results = index.search(query)
  result_file = io.get_user_choice(results)
  if result_file is None:
    print "No results found"
  else:
    action(result_file)

