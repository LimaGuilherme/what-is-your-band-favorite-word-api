from unittest import TestCase
from src.lyrics.cli_commands import config_credentials, get_top_words
from src.lyrics.searchers import AlbumsSearcher

from src import configurations as config_module


class TestCLI(TestCase):

    def test_should_get_top_words(self):
        pass