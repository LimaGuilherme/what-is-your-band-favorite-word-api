from unittest import TestCase

from src import exceptions
from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import ArtistSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

from src.lyrics.statitics import create_statistic
from src.lyrics.application_service import APIArtistLyricsService
from src.lyrics.repositories import create_repository, MongoRepository, ElasticSearchRepository


class TestAPIArtistLyricsService(TestCase):

    def setUp(self) -> None:
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        artist_searcher = ArtistSearcher()
        self.repository = create_repository()
        statistic = create_statistic(self.repository)

        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)
        self.artist_service = APIArtistLyricsService(lyrics_searcher, statistic, self.repository, artist_searcher)

    def test_when_count_frequency_should_raise_artist_not_found(self):
        with self.assertRaises(exceptions.ArtistNotFound):
            self.artist_service.count_frequency('Random Unknown Artist')

    def test_when_count_frequency_should_return_statistics_of_lyrics(self):
        self.artist_service.index('Mc Rodolfinho')
        words_frequency = self.artist_service.count_frequency('Mc Rodolfinho')
        self.assertIsInstance(words_frequency, dict)

        if isinstance(self.repository, MongoRepository):
            self.repository.delete_collection()

        if isinstance(self.repository, ElasticSearchRepository):
            self.repository.delete_index()

    def test_when_index_should_raise_artist_not_found(self):
        with self.assertRaises(exceptions.ArtistNotFound):
            self.artist_service.index('Random Unknown Artist')
