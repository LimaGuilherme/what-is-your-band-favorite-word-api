from unittest import TestCase

from src.domain.track_searcher import TrackSearcher


class TestTrackSearcher(TestCase):

    def test_should_return_tracks_from_given_album(self):
        track_searcher = TrackSearcher()

        tracks = track_searcher.get_tracks('Meteora')
        self.assertEqual(tracks, ['Foreword', "Don't Stay", 'Somewhere I Belong',
                                  'Lying from You', 'Hit the Floor', 'Easier to Run',
                                  'Faint', 'Figure.09', 'Breaking the Habit', 'From the Inside',
                                  "Nobody's Listening", 'Session', 'Numb'])
        self.assertIsInstance(tracks, list)

    def test_should_raise_albums_not_found(self):
        track_searcher = TrackSearcher()

        album_tracks = track_searcher.get_tracks('MeteoroDaPaixão')
        self.assertEqual(album_tracks, [])
        self.assertIsInstance(album_tracks, list)
