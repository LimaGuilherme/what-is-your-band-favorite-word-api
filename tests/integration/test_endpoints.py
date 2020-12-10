from unittest import TestCase

from src import initialize
from src.lyrics.repositories import create_repository, MongoRepository, ElasticSearchRepository

from src import configurations as config_module


class TestApi(TestCase):

    def setUp(self) -> None:
        self.app = initialize.web_app.test_client()
        self.config = config_module.get_config(config_type='full')
        self.repository = create_repository(self.config)

    def tearDown(self) -> None:
        if isinstance(self.repository, MongoRepository):
            self.repository.delete_collection()

        if isinstance(self.repository, ElasticSearchRepository):
            self.repository.delete_index()

    def test_post_should_return_ok_when_lyrics_are_correctly_create(self):
        self.url = '/api/artists/Mc Rodolfinho/lyrics'
        response = self.app.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'result': 'OK'})

    def test_post_should_raise_artist_not_found_when_given_a_invalid_artist(self):
        self.url = '/api/artists/Mc Kweiss/lyrics'
        response = self.app.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'result': 'error',
                                         'exception': 'This artist seems invalid, perhaps you misspelled'})

    def test_get_should_raise_artist_not_found_when_given_a_invalid_artist(self):
        self.url = '/api/artists/Mc Kweiss/lyrics'
        response = self.app.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'result': 'error',
                                         'exception': 'This artist seems invalid, perhaps you misspelled'})

    # def test_get_should_raise_lyrics_not_found_when_theres_no_lyrics_yet(self):
    #     self.url = '/api/artists/Mc Rodolfinho/lyrics'
    #     response = self.app.get(self.url)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json, {'result': 'error',
    #                                      'exception': 'sadly no lyrics were found'})

    def test_delete_should_return_method_not_allowed(self):
        self.url = '/api/artists/Mc Rodolfinho/lyrics'
        response = self.app.delete(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json, {'error': 'Method Not Allowed', 'result': 'error'})

    def test_put_should_return_method_not_allowed(self):
        self.url = '/api/artists/Mc Rodolfinho/lyrics'
        response = self.app.put(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json, {'error': 'Method Not Allowed', 'result': 'error'})
