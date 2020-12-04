from unittest import TestCase, mock

from src.configurations import LocalStorageSimpleConfigRepository, SimpleConfig
from src.exceptions import ConfigError


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
