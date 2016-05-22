import whoosh.index as ix
import shutil
import os
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm, Term, Or
from os.path import expanduser, isdir
import io

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
      choice = int(io.get_choice()) - 1
      result = results[choice]
    return result["filename"]

def reindex(index_path, notes_path):
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

def create_or_load_index(index_path, notes_path):
  if isdir(index_path):
    return ix.open_dir(index_path)
  else:
    return reindex(index_path, notes_path)

