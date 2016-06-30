import whoosh.index as ix
import shutil
import os
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm, Term, Or
from os.path import expanduser, isdir
import io

class IndexerException(Exception):
      pass

class Index:
  def __init__(self, index):
    self.index = index

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

def reindex(config):
  shutil.rmtree(config.index_path, True)
  os.mkdir(config.index_path)
  schema = Schema(filename=TEXT(stored=True), content=TEXT)
  index = ix.create_in(config.index_path, schema)
  writer = index.writer()
  for note in os.listdir(config.notes_path):
    note_full_path = os.path.join(config.notes_path, note)
    with open(note_full_path) as note_file:
      writer.add_document(filename=unicode(note_full_path, "utf-8"), content=unicode(note_file.read(), "utf-8"))
  writer.commit()
  return index

def create_or_load_index(config):
  if _invalid_index_path(config.index_path):
    raise IndexerException("index location %s doesn't contain index" % config.index_path)

  if not isdir(config.notes_path):
    os.makedirs(config.notes_path)

  return Index(reindex(config))

def _invalid_index_path(path):
  return isdir(path) and os.listdir(path) != [] \
      and not os.path.isfile(os.path.join(path, '_MAIN_1.toc'))
