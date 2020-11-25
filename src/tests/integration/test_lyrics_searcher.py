from unittest import TestCase

from src.domain.album_searcher import AlbumsSearcher
from src.domain.entity import Lyrics
from src.domain.lyrics_searcher import LyricsSearcher
from src.domain.track_searcher import TrackSearcher


class TestLyricsSearcher(TestCase):

    def test_should_return_a_empty_list_of_lyrics_when_given_a_invalid_artist(self):
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)

        lyrics = lyrics_searcher.get_lyrics('Mc Magro da Leste')
        self.assertEqual(lyrics, [])
        self.assertIsInstance(lyrics, list)

    def test_should_return_list_of_lyrics_when_given_a_valid_artist(self):
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)

        lyrics_list = lyrics_searcher.get_lyrics('Mc Rodolfinho')
        self.assertIsInstance(lyrics_list, list)

        for lyrics in lyrics_list:
            self.assertIsInstance(lyrics, Lyrics)
