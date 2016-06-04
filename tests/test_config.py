import unittest
import os
from notescli import config

class TestConfig(unittest.TestCase):

  def test_load_config_with_full_path(self):
    loaded_conf = config.load_config("tests/fixtures/sample-config.yaml")
    self.assertEquals(loaded_conf.index_path, "/tmp/some/index/dir")
    self.assertEquals(loaded_conf.notes_path, "/tmp/some/notes/dir")

  def test_load_config_with_homedir(self):
    home = os.environ["HOME"]
    loaded_conf = config.load_config("tests/fixtures/config-with-homedir.yaml")
    self.assertEquals(loaded_conf.index_path, home + "/.tmp/index")
    self.assertEquals(loaded_conf.notes_path, home + "/.tmp/notes")
