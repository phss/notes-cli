import whoosh.index as ix
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm, Term, Or
from os.path import expanduser, isdir
import notescli.io

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
      choice = int(notescli.io.get_choice()) - 1
      result = results[choice]
    return result["filename"]

def create_or_load_index(index_path, notes_path):
  if isdir(index_path):
    return ix.open_dir(index_path)
  else:
    return command_reindex(index_path, notes_path)

