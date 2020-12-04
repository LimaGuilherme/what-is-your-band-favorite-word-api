from unittest import TestCase, mock

from src.configurations import LocalStorageSimpleConfigRepository, EnvFullConfigRepository, SimpleConfig
from src.exceptions import ConfigError


class TestEnvFullConfigRepository(TestCase):

    @mock.patch('src.configurations.os')
    def test_should_get(self, os_mock):
        os_mock.environ = {
            'SPOTIFY_CLIENT_ID': 'V1',
            'SPOTIFY_CLIENT_SECRET': 'V2',
            'ELASTICSEARCH_HOST': 'V3',
            'ELASTICSEARCH_PORT': 'V4',
            'GENIUS_ACCESS_TOKEN': 'V5',
            'MONGO_HOST': 'V6',
            'MONGO_PORT': 'V7',
            'REPOSITORY': 'V8',
            'ELASTICSEARCH_INDEX': 'V9',
            'MONGO_COLLECTION': 'V10'
        }

        repository = EnvFullConfigRepository()
        full_config = repository.get()

        self.assertFalse(full_config.DEBUG)
        self.assertEqual(full_config.SPOTIFY_CLIENT_ID, 'V1')
        self.assertEqual(full_config.SPOTIFY_CLIENT_SECRET, 'V2')
        self.assertEqual(full_config.ELASTICSEARCH_HOST, 'V3')
        self.assertEqual(full_config.ELASTICSEARCH_PORT, 'V4')
        self.assertEqual(full_config.GENIUS_ACCESS_TOKEN, 'V5')
        self.assertEqual(full_config.MONGO_HOST, 'V6')
        self.assertEqual(full_config.MONGO_PORT, 'V7')
        self.assertEqual(full_config.REPOSITORY, 'V8')
        self.assertEqual(full_config.ELASTICSEARCH_INDEX, 'V9')
        self.assertEqual(full_config.MONGO_COLLECTION, 'V10')

    @mock.patch('src.configurations.os')
    def test_get_should_raise_config_error_when_any_attribute_env_is_missing(self, os_mock):
        os_mock.environ = {
            'SPOTIFY_CLIENT_ID': 'V1',
            'SPOTIFY_CLIENT_SECRET': 'V2',
            'ELASTICSEARCH_HOST': 'V3'
        }

        with self.assertRaises(ConfigError):
            repository = EnvFullConfigRepository()
            repository.get()


class TestLocalFileSimpleConfigRepository(TestCase):

    def test_should_save(self):
        config_repository = LocalStorageSimpleConfigRepository()
        simple_config = SimpleConfig(
            DEBUG=True,
            SPOTIFY_CLIENT_ID='fdsafsad',
            SPOTIFY_CLIENT_SECRET='FDSJOIdsja',
            GENIUS_ACCESS_TOKEN='aoijaa78',
        )
        config_repository.save(simple_config)

    def test_should_get(self):
        config_repository = LocalStorageSimpleConfigRepository()
        simple_config = SimpleConfig(
            DEBUG=True,
            SPOTIFY_CLIENT_ID='fdsafsad',
            SPOTIFY_CLIENT_SECRET='FDSJOIdsja',
            GENIUS_ACCESS_TOKEN='aoijaa78',
        )
        config_repository.save(simple_config)
        got_simple_config = config_repository.get()
        self.assertEqual(simple_config, got_simple_config)

    def test_get_should_raise_config_error_when_any_attribute_from_local_storage_is_missing(self):
        config_repository = LocalStorageSimpleConfigRepository()
        simple_config_mock = mock.MagicMock()
        simple_config_mock.as_dict = {
            'DEBUG': True,
            'SPOTIFY_CLIENT_ID': 'fdsafsad'
        }

        config_repository.save(simple_config_mock)

        with self.assertRaises(ConfigError):
            config_repository.get()
