import unittest
import os
from notescli import config as c, indexer

class TestIndexer(unittest.TestCase):

  def test_create_index_from_scratch(self):
    config = c.Config("/tmp/fakeindex", "tests/fixtures/docs_to_index/")
    index = indexer.create_or_load_index(config)
    # assert something
    
  def test_load_index_if_already_created(self):
    None

  def test_fail_to_create_if_notes_path_dont_exist(self):
    None

