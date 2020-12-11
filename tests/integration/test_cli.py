import json
import os
from unittest import TestCase

from click.testing import CliRunner

from src.lyrics.cli_commands import config_credentials


class TestCLI(TestCase):

    def setUp(self) -> None:
        self.cli_runner = CliRunner()

    def tearDown(self, ) -> None:
        try:
            os.remove('.localstorage')
        except OSError:
            pass

    def assert_file_exists(self):
        self.assertTrue(os.path.exists('.localstorage'))

    def assert_credentials_in_localstorage(self, spotify_client_id, spotify_client_secret, genius_access_token):
        with open('.localstorage', 'r') as localstorage:
            localstorage_credentials = json.load(localstorage)

        self.assertIn('SPOTIFY_CLIENT_ID', localstorage_credentials)
        self.assertIn('SPOTIFY_CLIENT_SECRET', localstorage_credentials)
        self.assertIn('GENIUS_ACCESS_TOKEN', localstorage_credentials)

        self.assertEqual(localstorage_credentials['SPOTIFY_CLIENT_ID'], spotify_client_id)
        self.assertEqual(localstorage_credentials['SPOTIFY_CLIENT_SECRET'], spotify_client_secret)
        self.assertEqual(localstorage_credentials['GENIUS_ACCESS_TOKEN'], genius_access_token)

    def test_should_create_credentials_using_prompt(self):
        self.cli_runner.invoke(config_credentials, input='a\nb\nc')
        self.assert_file_exists()
        self.assert_credentials_in_localstorage(spotify_client_id='a', spotify_client_secret='b', genius_access_token='c')

    def test_should_create_credentials_using_options(self):
        self.cli_runner.invoke(config_credentials, ['--spotify-client-id', 'a',
                                                    '--spotify-client-secret', 'b',
                                                    '--genius-access-token', 'c'])
        self.assert_file_exists()
        self.assert_credentials_in_localstorage(spotify_client_id='a', spotify_client_secret='b', genius_access_token='c')

    def test_should_exit_when_given_a_invalid_key_using_options(self):
        result = self.cli_runner.invoke(config_credentials, ['--spotify-client-id', 'a',
                                                             '--spotify-client-secret', 'b',
                                                             '--whatever-key', 'c'])
        self.assertTrue(result.exit_code, 2)
