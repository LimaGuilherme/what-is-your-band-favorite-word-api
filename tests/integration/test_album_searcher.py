from unittest import TestCase

from src.lyrics.searchers import AlbumsSearcher

from src import configurations as config_module


class TestAlbumsSearcher(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config()

    def test_should_bring_all_albums_from_given_artist(self):

        albums_searcher = AlbumsSearcher(self.config)
        albums = albums_searcher.get_albums('Aurora')
        self.assertEqual(albums, ['A Different Kind Of Human (Step II)',
                                  'A Different Kind of Human - Step 2',
                                  'A Different Kind Of Human – Step 2',
                                  'All My Demons Greeting Me As A Friend',
                                  'All My Demons Greeting Me as a Friend',
                                  'All My Demons Greeting Me As A Friend (Deluxe)',
                                  'All My Demons Greeting Me as a Friend (Deluxe)',
                                  'Infections Of A Different Kind',
                                  'Infections of a Different Kind (Step I)',
                                  'Infections of a Different Kind Step 1',
                                  'Infections Of A Different Kind – Step 1'])
        self.assertIsInstance(albums, list)

    def test_should_raise_albums_not_found(self):
        albums_searcher = AlbumsSearcher(self.config)
        albums = albums_searcher.get_albums('Mc Magro da Leste')
        self.assertEqual(albums, [])
        self.assertIsInstance(albums, list)

    def test_should_remove_remaster_or_live_albums(self):
        albums_searcher = AlbumsSearcher(self.config)
        albums = ['Mc Magro da Leste', 'Mc Magro da Leste (Live)', 'MC Magro da Leste (RJ Edition)']
        acceptable_albums = albums_searcher.remove_remaster_and_live_albums(albums)
        self.assertEqual(acceptable_albums, ['Mc Magro da Leste'])

    def test_should_not_remove_any_album(self):
        albums_searcher = AlbumsSearcher(self.config)
        albums = ['Mc Magro da Leste', 'Mc Magro da Lest Feat Paçoquinha', 'MC Magro Remix Proibidão']
        acceptable_albums = albums_searcher.remove_remaster_and_live_albums(albums)
        self.assertEqual(acceptable_albums, albums)
