import unittest
from notescli import config

class TestConfig(unittest.TestCase):

  def test_load_config_with_full_path(self):
    loaded_conf = config.load_config("tests/fixtures/sample-config.yaml")
    self.assertEquals(loaded_conf.indexdir, "/tmp/some/index/dir")
    self.assertEquals(loaded_conf.notesdir, "/tmp/some/notes/dir")
