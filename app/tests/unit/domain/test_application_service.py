from unittest import TestCase, mock
from unittest.mock import MagicMock

from app.domain.application_service import ArtistLyricsService


class TestArtistLyricsService(TestCase):

    def test_count_frequency_works(self):
        lyrics_searcher_mock = MagicMock()

        statistic_mock = MagicMock()
        list_statistic_mock = MagicMock()
        statistic_mock.count_words_frequency.return_value = list_statistic_mock

        lyrics_list_mock = MagicMock()
        repository_mock = MagicMock()
        repository_mock.get_by_artist.return_value = lyrics_list_mock

        artist_lyrics_service = ArtistLyricsService(lyrics_searcher_mock, statistic_mock, repository_mock)
        result = artist_lyrics_service.count_frequency('Weiss')

        repository_mock.get_by_artist.assert_called_with('Weiss')
        statistic_mock.count_words_frequency.assert_called_with(lyrics_list_mock)
        self.assertEqual(list_statistic_mock, result)

    def test_index_works(self):
        lyrics_mock1 = MagicMock()
        lyrics_mock2 = MagicMock()
        lyrics_searcher_mock = MagicMock()
        lyrics_searcher_mock.get_lyrics.return_value = [lyrics_mock1, lyrics_mock2]

        statistic_mock = MagicMock()

        repository_mock = MagicMock()

        artist_lyrics_service = ArtistLyricsService(lyrics_searcher_mock, statistic_mock, repository_mock)
        artist_lyrics_service.index('Weiss')

        call1 = mock.call(lyrics_mock1)
        call2 = mock.call(lyrics_mock2)

        lyrics_searcher_mock.get_lyrics.assert_called_with('Weiss')
        repository_mock.save.assert_has_calls([call1, call2], any_order=False)
