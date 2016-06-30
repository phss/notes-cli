import unittest
import os
import tempfile
from notescli import config as c, indexer
from notescli.indexer import IndexerException

class TestCreateIndex(unittest.TestCase):
  TEST_INDEX_PATH='tests/fixtures/docs_to_index/'

  def test_create_index_from_scratch_in_inexistent_index_dir(self):
    config = self._config_with_temp_index_dir(self.TEST_INDEX_PATH)

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

  def test_create_index_from_scratch_in_empty_index_dir(self):
    config = self._config_with_temp_index_dir(self.TEST_INDEX_PATH)
    os.mkdir(config.index_path)

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

  def test_load_index_if_already_created(self):
    config = self._config_with_temp_index_dir(self.TEST_INDEX_PATH)

    indexer.create_or_load_index(config)
    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

  def test_fail_to_create_if_index_dir_contains_non_index(self):
    config = c.Config(self.TEST_INDEX_PATH, self.TEST_INDEX_PATH)

    self.assertRaises(IndexerException, indexer.create_or_load_index, config)

  def test_creates_index_even_if_notes_path_dont_exist(self):
    config = self._config_with_temp_index_dir("/tmp/no/notes/dir")

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

  def _config_with_temp_index_dir(self, notes_dir):
    index_dir = tempfile.mktemp(prefix='notestest-')
    return c.Config(index_dir, notes_dir)

