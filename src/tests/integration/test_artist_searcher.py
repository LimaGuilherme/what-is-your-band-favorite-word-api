from unittest import TestCase

from src.domain.searchers import ArtistSearcher


class TestArtistSearcher(TestCase):

    def test_should_return_false_for_nonexistent_artist(self):
        artist_searcher = ArtistSearcher()

        is_valid = artist_searcher.is_this_artist_valid('Random Unknown Artist')
        self.assertEqual(is_valid, False)

    def test_should_return_true_for_existing_artist(self):
        artist_searcher = ArtistSearcher()

        is_valid = artist_searcher.is_this_artist_valid('Queen')
        self.assertEqual(is_valid, True)
