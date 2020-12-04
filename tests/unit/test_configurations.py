from unittest import TestCase

from src.configurations import SimpleConfig, FullConfig, create_config


class TestSimpleConfig(TestCase):

    def test_should_init(self):
        simple_config = SimpleConfig(
            DEBUG=True,
            SPOTIFY_CLIENT_ID='fdsafsad',
            SPOTIFY_CLIENT_SECRET='FDSJOIdsja',
            GENIUS_ACCESS_TOKEN='aoijaa78'
        )
        self.assertTrue(simple_config.DEBUG)
        self.assertEqual(simple_config.SPOTIFY_CLIENT_ID, 'fdsafsad')
        self.assertEqual(simple_config.SPOTIFY_CLIENT_SECRET, 'FDSJOIdsja')
        self.assertEqual(simple_config.GENIUS_ACCESS_TOKEN, 'aoijaa78')


class TestFullConfig(TestCase):

    def test_should_init(self):
        simple_config = FullConfig(
            DEBUG=True,
            SPOTIFY_CLIENT_ID='fdsafsad',
            SPOTIFY_CLIENT_SECRET='FDSJOIdsja',
            GENIUS_ACCESS_TOKEN='aoijaa78',
            ELASTICSEARCH_HOST='localhost',
            ELASTICSEARCH_PORT='9200',
            MONGO_HOST='localhost',
            MONGO_PORT='1111',
            REPOSITORY='elasticsearch',
            ELASTICSEARCH_INDEX='blabla',
            MONGO_COLLECTION='bleble'
        )
        self.assertTrue(simple_config.DEBUG)
        self.assertEqual(simple_config.SPOTIFY_CLIENT_ID, 'fdsafsad')
        self.assertEqual(simple_config.SPOTIFY_CLIENT_SECRET, 'FDSJOIdsja')
        self.assertEqual(simple_config.GENIUS_ACCESS_TOKEN, 'aoijaa78')
        self.assertEqual(simple_config.ELASTICSEARCH_HOST, 'localhost')
        self.assertEqual(simple_config.ELASTICSEARCH_PORT, '9200')
        self.assertEqual(simple_config.MONGO_HOST, 'localhost')
        self.assertEqual(simple_config.MONGO_PORT, '1111')
        self.assertEqual(simple_config.REPOSITORY, 'elasticsearch')
        self.assertEqual(simple_config.ELASTICSEARCH_INDEX, 'blabla')
        self.assertEqual(simple_config.MONGO_COLLECTION, 'bleble')
