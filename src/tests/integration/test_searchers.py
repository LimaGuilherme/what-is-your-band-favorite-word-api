from unittest import TestCase

from src.domain.album_searcher import AlbumsSearcher
from src.domain.lyrics_searcher import LyricsSearcher
from src.domain.track_searcher import TrackSearcher


class TestLyricsSearcher(TestCase):

    def test_should_raise_albums_not_found(self):
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)

        lyrics = lyrics_searcher.get_lyrics('Mc Magro da Leste')
        self.assertEqual(lyrics, [])
        self.assertIsInstance(lyrics, list)
