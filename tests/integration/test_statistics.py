from unittest import TestCase

from src.lyrics import exceptions
from src.lyrics.entity import Lyrics
from src.lyrics.repositories import create_repository
from src import configurations as config_module
from src.lyrics.statitics import create_statistic


class TestCommonStatistical(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        self.config.REPOSITORY = 'mongodb'
        self.mongodb_repository = create_repository(self.config)
        self.statistical = create_statistic(self.mongodb_repository)

    def tearDown(self) -> None:
        self.mongodb_repository.delete_collection()

    def test_should_count_words_frequency(self):
        lyrics = [Lyrics(artist='Mc Rodolfinho', lyrics='a me deus', album='vida loca', track='como e bom ser vida loca')]
        words_frequency = self.statistical.count_words_frequency(lyrics, 10)
        self.assertIsInstance(words_frequency, dict)
        self.assertEqual(len(words_frequency), 1)


class TestESStatistical(TestCase):

    def setUp(self) -> None:
        self.config = config_module.get_config(config_type='full')
        self.config.REPOSITORY = 'elasticsearch'
        self.elasticsearch_repository = create_repository(self.config)
        self.statistical = create_statistic(self.elasticsearch_repository)

    def tearDown(self) -> None:
        try:
            self.elasticsearch_repository.delete_index()
        except:
            pass

    def test_should_count_words_frequency(self):
        lyrics_list = [Lyrics(artist='Mc Rodolfinho',
                              lyrics='a me deus',
                              album='vida loca',
                              track='como e bom ser vida loca'),
                       Lyrics(artist='Mc Rodolfinho',
                              lyrics='a me deus',
                              album='vida loca',
                              track='como e bom ser vida loca')]

        for lyrics in lyrics_list:
            self.elasticsearch_repository.save(lyrics)

        lyrics = self.elasticsearch_repository.get_by_artist('Mc Rodolfinho')
        words_frequency = self.statistical.count_words_frequency(lyrics, 10)
        self.assertIsInstance(words_frequency, dict)
        self.assertEqual(len(words_frequency), 1)

    def test_should_raise_invalid_repository(self):
        with self.assertRaises(exceptions.InvalidRepository):
            self.statistical = create_statistic('invalid-repository')
