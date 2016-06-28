import unittest
import os
import tempfile
from notescli import config as c, indexer

class TestCreateIndex(unittest.TestCase):

  def test_create_index_from_scratch(self):
    index_dir = tempfile.mktemp(prefix='notestest-')
    config = c.Config(index_dir, "tests/fixtures/docs_to_index/")

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index) 
    # TODO: add better assertion at some point
    
  def test_load_index_if_already_created(self):
    index_dir = tempfile.mktemp(prefix='notestest-')
    config = c.Config(index_dir, "tests/fixtures/docs_to_index/")

    indexer.create_or_load_index(config)
    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index) 
    # TODO: add better assertion at some point

  def test_fail_to_create_if_notes_path_dont_exist(self):
    None

