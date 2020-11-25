from unittest import TestCase

from src import exceptions
from src.domain.album_searcher import AlbumsSearcher
from src.domain.application_service import ArtistLyricsService
from src.domain.artist_searcher import ArtistSearcher
from src.domain.lyrics_searcher import LyricsSearcher
from src.domain.repositories import create_repository
from src.domain.statitics import create_statistic
from src.domain.track_searcher import TrackSearcher


class TestArtistLyrics(TestCase):

    def test_when_count_frequency_should_raise_artist_not_found(self):
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        artist_searcher = ArtistSearcher()
        repository = create_repository()
        statistic = create_statistic(repository)

        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)
        artist_service = ArtistLyricsService(lyrics_searcher, statistic, repository, artist_searcher)

        with self.assertRaises(exceptions.ArtistNotFound):
            artist_service.count_frequency('Random Unknown Artist')

    def test_when_index_should_raise_artist_not_found(self):
        track_searcher = TrackSearcher()
        albums_searcher = AlbumsSearcher()
        artist_searcher = ArtistSearcher()
        repository = create_repository()
        statistic = create_statistic(repository)

        lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)
        artist_service = ArtistLyricsService(lyrics_searcher, statistic, repository, artist_searcher)

        with self.assertRaises(exceptions.ArtistNotFound):
            artist_service.index('Random Unknown Artist')
