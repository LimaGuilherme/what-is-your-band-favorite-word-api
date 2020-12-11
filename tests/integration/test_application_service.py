from unittest import TestCase

from src.lyrics import exceptions
from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import ArtistSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

from src.lyrics.statitics import create_statistic
from src.lyrics.application_service import IndexService, RunTimeTopWordsService, StorageTopWordsService
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


class TestStorageTopWordsService(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        track_searcher = TrackSearcher(self.config)
        albums_searcher = AlbumsSearcher(self.config)
        artist_searcher = ArtistSearcher(self.config)
        statistic = create_statistic()
        self.repository = create_repository(self.config)

        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, self.config)

        self.storage_words_service = StorageTopWordsService(lyrics_searcher, statistic, self.repository, artist_searcher)
        self.index_service = IndexService(lyrics_searcher, self.repository, artist_searcher)

    def test__should_raise_artist_not_found(self):
        with self.assertRaises(exceptions.ArtistNotFound):
            self.index_service.index('Random Unknown Artist')

    def test_when_count_frequency_should_return_statistics_of_lyrics(self):
        self.index_service.index('Mc Rodolfinho')
        words_frequency = self.storage_words_service.count_frequency('Mc Rodolfinho', 10)
        self.assertIsInstance(words_frequency, dict)

        if isinstance(self.repository, MongoRepository):
            self.repository.delete_collection()

        if isinstance(self.repository, ElasticSearchRepository):
            self.repository.delete_index()

    def test_should_raise_lyrics_not_found(self):

        with self.assertRaises(exceptions.LyricsNotFound):
            self.index_service.index('Mc Rodolfinho')
            self.storage_words_service.count_frequency('Semper Soma', 10)


class TestRunTimeTopWordsService(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        track_searcher = TrackSearcher(self.config)
        albums_searcher = AlbumsSearcher(self.config)
        artist_searcher = ArtistSearcher(self.config)
        statistic = create_statistic()
        self.repository = create_repository(self.config)

        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, self.config)

        self.runtime_words_service = RunTimeTopWordsService(lyrics_searcher, statistic, artist_searcher)
        self.index_service = IndexService(lyrics_searcher, self.repository, artist_searcher)

    def test__should_raise_artist_not_found(self):
        with self.assertRaises(exceptions.ArtistNotFound):
            self.runtime_words_service.count_frequency('MC Magro Weiss', 10)

    def test_when_count_frequency_should_return_statistics_of_lyrics(self):
        self.index_service.index('Mc Rodolfinho')
        words_frequency = self.runtime_words_service.count_frequency('Mc Rodolfinho', 10)
        self.assertIsInstance(words_frequency, dict)

        if isinstance(self.repository, MongoRepository):
            self.repository.delete_collection()

        if isinstance(self.repository, ElasticSearchRepository):
            self.repository.delete_index()

    def test_should_raise_lyrics_not_found(self):

        with self.assertRaises(exceptions.LyricsNotFound):
            self.runtime_words_service.count_frequency('Semper Soma', 10)
