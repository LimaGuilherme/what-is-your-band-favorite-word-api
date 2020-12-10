from unittest import TestCase

from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

from src.lyrics.entity import Lyrics
from src import configurations as config_module


class TestLyricsSearcher(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')

    def test_should_return_a_empty_list_of_lyrics_when_given_a_invalid_artist(self):
        track_searcher = TrackSearcher(self.config)
        albums_searcher = AlbumsSearcher(self.config)
        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, self.config)

        lyrics = lyrics_searcher.get_lyrics('Mc Magro da Leste')
        self.assertEqual(lyrics, [])
        self.assertIsInstance(lyrics, list)

    def test_should_return_list_of_lyrics_when_given_a_valid_artist(self):
        track_searcher = TrackSearcher(self.config)
        albums_searcher = AlbumsSearcher(self.config)
        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, self.config)

        lyrics_list = lyrics_searcher.get_lyrics('Mc Rodolfinho')
        self.assertIsInstance(lyrics_list, list)

        for lyrics in lyrics_list:
            self.assertIsInstance(lyrics, Lyrics)
