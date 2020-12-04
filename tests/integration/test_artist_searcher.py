from unittest import TestCase

from src.lyrics.searchers import ArtistSearcher
from src import configurations as config_module


class TestArtistSearcher(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config()

    def test_should_return_false_for_nonexistent_artist(self):
        artist_searcher = ArtistSearcher(self.config)

        is_valid = artist_searcher.is_this_artist_valid('Random Unknown Artist')
        self.assertEqual(is_valid, False)

    def test_should_return_true_for_existing_artist(self):
        artist_searcher = ArtistSearcher(self.config)

        is_valid = artist_searcher.is_this_artist_valid('Queen')
        self.assertEqual(is_valid, True)
