import unittest
import os
import tempfile
from notescli import config as c, indexer

class TestCreateIndex(unittest.TestCase):

  def test_create_index_from_scratch(self):
    config = self._config_with_temp_index_dir("tests/fixtures/docs_to_index/")

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)
    # TODO: add better assertion at some point

  def test_load_index_if_already_created(self):
    config = self._config_with_temp_index_dir("tests/fixtures/docs_to_index/")

    indexer.create_or_load_index(config)
    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)
    # TODO: add better assertion at some point

  def test_fail_to_create_if_notes_path_dont_exist(self):
    config = self._config_with_temp_index_dir("/tmp/no/notes/dir")

    index = indexer.create_or_load_index(config)

    self.assertIsNone(index)

  def _config_with_temp_index_dir(self, notes_dir):
    index_dir = tempfile.mktemp(prefix='notestest-')
    return c.Config(index_dir, notes_dir)

