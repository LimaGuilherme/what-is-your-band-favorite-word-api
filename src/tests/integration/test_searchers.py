from unittest import TestCase

from src.domain.searchers import AlbumsSearcher, LyricsSearcher
from src.domain.track_searcher import TrackSearcher


class TestLyricsSearcher(TestCase):

    def test_should_raise_albums_not_found(self):
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)

        lyrics = lyrics_searcher.get_lyrics('Mc Magro da Leste')
        self.assertEqual(lyrics, [])
        self.assertIsInstance(lyrics, list)


class TestAlbumsSearcher(TestCase):

    def test_should_raise_albums_not_found(self):
        albums_searcher = AlbumsSearcher()
        albums = albums_searcher.get_albums('Mc Magro da Leste')
        self.assertEqual(albums, [])
        self.assertIsInstance(albums, list)

    def test_should_remove_remaster_or_live_albums(self):
        albums_searcher = AlbumsSearcher()
        albums = ['Mc Magro da Leste', 'Mc Magro da Leste (Live)', 'MC Magro da Leste (RJ Edition)']
        acceptable_albums = albums_searcher.remove_remaster_and_live_albums(albums)
        self.assertEqual(acceptable_albums, ['Mc Magro da Leste'])

    def test_should_not_remove_any_album(self):
        albums_searcher = AlbumsSearcher()
        albums = ['Mc Magro da Leste', 'Mc Magro da Lest Feat Paçoquinha', 'MC Magro Remix Proibidão']
        acceptable_albums = albums_searcher.remove_remaster_and_live_albums(albums)
        self.assertEqual(acceptable_albums, albums)
