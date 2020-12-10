from unittest import TestCase

from src.lyrics import exceptions
from src.lyrics.entity import Lyrics
from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import ArtistSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

from src.lyrics.statitics import create_statistic
from src.lyrics.application_service import IndexService, RunTimeWordsService, StorageWordsService
from src.lyrics.repositories import create_repository, MongoRepository, ElasticSearchRepository

from src import configurations as config_module


class TestElasticSearchRepository(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        self.config.REPOSITORY = 'elasticsearch'
        self.elasticsearch_repository = create_repository(self.config)

    def tearDown(self) -> None:
        self.elasticsearch_repository.delete_index()

    def test_should_save_lyrics(self):
        lyrics = Lyrics(artist='Mc Rodolfinho', lyrics='a me deus', album='vida loca', track='como e bom ser vida loca')
        self.elasticsearch_repository.save(lyrics)
        lyrics_list = self.elasticsearch_repository.get_by_artist('Mc Rodolfinho')
        self.assertIsInstance(lyrics_list, list)

    def test_should_get_terms(self):
        lyrics = Lyrics(artist='Mc Rodolfinho', lyrics='a me deus', album='vida loca', track='como e bom ser vida loca')
        self.elasticsearch_repository.save(lyrics)
        lyrics_list = self.elasticsearch_repository.get_by_artist('Mc Rodolfinho')
        self.assertIsInstance(lyrics_list, list)


class TestMongoRepository(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        self.config.REPOSITORY = 'mongodb'
        self.mongodb_repository = create_repository(self.config)

    def tearDown(self) -> None:
        self.mongodb_repository.delete_collection()

    def test_should_save_lyrics(self):
        lyrics = Lyrics(artist='Mc Rodolfinho', lyrics='a me deus', album='vida loca', track='como e bom ser vida loca')
        self.mongodb_repository.save(lyrics)
        lyrics_list = self.mongodb_repository.get_by_artist('Mc Rodolfinho')
        self.assertIsInstance(lyrics_list, list)
        self.assertTrue(len(lyrics_list), 1)

    def test_should_return_a_list_of_lyrics_when_search_for_artist(self):
        lyrics = Lyrics(artist='Mc Rodolfinho', lyrics='a me deus', album='vida loca', track='como e bom ser vida loca')
        self.mongodb_repository.save(lyrics)
        lyrics_list = self.mongodb_repository.get_by_artist('Mc Rodolfinho')
        self.assertIsInstance(lyrics_list, list)
        self.assertTrue(len(lyrics_list), 1)
        self.assertTrue(lyrics_list[0].artist, 'Mc Rodolfinho')
        self.assertTrue(lyrics_list[0].lyrics, 'a me deus')
        self.assertTrue(lyrics_list[0].album, 'vida loca')
        self.assertTrue(lyrics_list[0].track, 'como e bom ser vida loca')
        self.assertTrue(lyrics_list[0].words, ['a', 'me', 'deus'])
        self.assertTrue(len(lyrics_list[0].words), 3)


