from unittest import TestCase

from src.lyrics.searchers import TrackSearcher

from src import configurations as config_module


class TestTrackSearcher(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')

    def test_should_return_tracks_from_given_album(self):
        track_searcher = TrackSearcher(self.config)

        tracks = track_searcher.get_tracks('Meteora')
        self.assertEqual(tracks, ['Foreword', "Don't Stay", 'Somewhere I Belong',
                                  'Lying from You', 'Hit the Floor', 'Easier to Run',
                                  'Faint', 'Figure.09', 'Breaking the Habit', 'From the Inside',
                                  "Nobody's Listening", 'Session', 'Numb'])
        self.assertIsInstance(tracks, list)

    def test_should_raise_albums_not_found(self):
        track_searcher = TrackSearcher(self.config)

        album_tracks = track_searcher.get_tracks('MeteoroDaPaixão')
        self.assertEqual(album_tracks, [])
        self.assertIsInstance(album_tracks, list)
