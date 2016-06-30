import unittest
import os
import tempfile
from notescli import config as c, indexer
from notescli.indexer import IndexerException

class TestCreateIndex(unittest.TestCase):

  def test_create_index_from_scratch_in_inexistent_index_dir(self):
    config = _config_with_temp_index_dir(FIXTURE_NOTES_PATH)

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

  def test_create_index_from_scratch_in_empty_index_dir(self):
    config = _config_with_temp_index_dir(FIXTURE_NOTES_PATH)
    os.mkdir(config.index_path)

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

  def test_load_index_if_already_created(self):
    config = _config_with_temp_index_dir(FIXTURE_NOTES_PATH)

    indexer.create_or_load_index(config)
    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

  def test_fail_to_create_if_index_dir_contains_non_index(self):
    config = c.Config(FIXTURE_NOTES_PATH, FIXTURE_NOTES_PATH)

    self.assertRaises(IndexerException, indexer.create_or_load_index, config)

  def test_creates_index_even_if_notes_path_dont_exist(self):
    config = _config_with_temp_index_dir("/tmp/no/notes/dir")

    index = indexer.create_or_load_index(config)

    self.assertIsNotNone(index)

class TestListFilesInIndex(unittest.TestCase):

  def test_list_files_in_index(self):
    config = _config_with_temp_index_dir(FIXTURE_NOTES_PATH)

    index = indexer.create_or_load_index(config)

    self.assertEqual(index.list_files(),
        ['tests/fixtures/docs_to_index/first_doc.txt',
         'tests/fixtures/docs_to_index/second_doc.txt',
         'tests/fixtures/docs_to_index/unique_document.txt'])


# Common methods
FIXTURE_NOTES_PATH='tests/fixtures/docs_to_index/'
    
def _config_with_temp_index_dir(notes_dir):
  index_dir = tempfile.mktemp(prefix='notestest-')
  return c.Config(index_dir, notes_dir)

