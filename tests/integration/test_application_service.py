from unittest import TestCase

from src.lyrics import exceptions
from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import ArtistSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

from src.lyrics.statitics import create_statistic
from src.lyrics.application_service import IndexService, RunTimeWordsService, StorageWordsService
from src.lyrics.repositories import create_repository, MongoRepository, ElasticSearchRepository

from src import configurations as config_module


class TestIndexService(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        track_searcher = TrackSearcher(self.config)
        albums_searcher = AlbumsSearcher(self.config)
        artist_searcher = ArtistSearcher(self.config)
        self.repository = create_repository(self.config)

        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, self.config)
        self.index_service = IndexService(lyrics_searcher, self.repository, artist_searcher)

    def test_when_count_frequency_should_raise_artist_not_found(self):
        with self.assertRaises(exceptions.ArtistNotFound):
            self.index_service.index('Random Unknown Artist')

    def test_when_index_should_raise_artist_not_found(self):
        with self.assertRaises(exceptions.ArtistNotFound):
            self.index_service.index('Random Unknown Artist')

    def test_should_raise_lyrics_not_found(self):
        with self.assertRaises(exceptions.LyricsNotFound):
            self.index_service.index('Semper Soma')

    # def test_when_count_frequency_should_return_statistics_of_lyrics(self):
    #     self.index_service.index('Mc Rodolfinho')
    #     words_frequency = self.index_service.count_frequency('Mc Rodolfinho')
    #     self.assertIsInstance(words_frequency, dict)
    #
    #     if isinstance(self.repository, MongoRepository):
    #         self.repository.delete_collection()
    #
    #     if isinstance(self.repository, ElasticSearchRepository):
    #         self.repository.delete_index()


class TestRunTimeWordsService(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        track_searcher = TrackSearcher(self.config)
        albums_searcher = AlbumsSearcher(self.config)
        artist_searcher = ArtistSearcher(self.config)
        statistic = create_statistic()
        self.repository = create_repository(self.config)

        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, self.config)

        self.runtime_words_service = RunTimeWordsService(lyrics_searcher, statistic, artist_searcher)
        self.index_service = IndexService(lyrics_searcher, self.repository, artist_searcher)

    def test__should_raise_artist_not_found(self):
        with self.assertRaises(exceptions.ArtistNotFound):
            self.index_service.index('Random Unknown Artist')

    def test_when_count_frequency_should_return_statistics_of_lyrics(self):
        self.index_service.index('Mc Rodolfinho')
        words_frequency = self.runtime_words_service.count_frequency('Mc Rodolfinho', 10)
        self.assertIsInstance(words_frequency, dict)

        if isinstance(self.repository, MongoRepository):
            self.repository.delete_collection()

        if isinstance(self.repository, ElasticSearchRepository):
            self.repository.delete_index()

    def test_should_raise_lyrics_not_found(self):
        self.index_service.index('Mc Rodolfinho')

        with self.assertRaises(exceptions.LyricsNotFound):
            self.index_service.index('Semper Soma')
