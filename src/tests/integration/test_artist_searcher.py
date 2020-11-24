from unittest import TestCase

from src.domain.artist_searcher import ArtistSearcher


class TestArtistSearcher(TestCase):

    def test_should_return_false_for_nonexistent_artist(self):
        artist_searcher = ArtistSearcher()

        exists = artist_searcher.check_if_artist_exists('Random Unkown Artist')
        self.assertEqual(exists, False)

    def test_should_return_true_for_existing_artist(self):
        artist_searcher = ArtistSearcher()

        exists = artist_searcher.check_if_artist_exists('Queen')
        self.assertEqual(exists, True)



