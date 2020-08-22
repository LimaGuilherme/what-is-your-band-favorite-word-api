from unittest import TestCase

from app import exceptions
from app.domain.searchers import TrackSearcher, AlbumsSearcher, LyricsSearcher


class TestTrackSearcher(TestCase):

    def test_should_raise_albums_not_found(self):
        track_searcher = TrackSearcher()
        with self.assertRaises(exceptions.AlbumsNotFound):
            track_searcher.get_album_tracks('MeteoroDaPaixão')


class TestLyricsSearcher(TestCase):

    def test_should_raise_albums_not_found(self):
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)
        with self.assertRaises(exceptions.AlbumsNotFound):
            lyrics_searcher.get_lyrics('Mc Magro da Leste')


class TestAlbumsSearcher(TestCase):

    def test_should_raise_albums_not_found(self):
        albums_searcher = AlbumsSearcher()
        with self.assertRaises(exceptions.AlbumsNotFound):
            albums_searcher.get_albums('Mc Magro da Leste')
