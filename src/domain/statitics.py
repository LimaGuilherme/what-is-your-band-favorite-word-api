import re

from abc import ABC, abstractmethod
from typing import List

from src import exceptions
from src.domain.entity import Lyrics
from src.domain.repositories import MongoRepository, ElasticSearchRepository
from src.domain.stop_words import STOP_WORDS


class StatisticCount(ABC):

    @abstractmethod
    def count_words_frequency(self, lyrics_list: List[Lyrics]) -> dict:
        pass


class ESStaticsCount(StatisticCount):

    def __init__(self, elastic_search_repository):
        super(ESStaticsCount, self).__init__()
        self.__elastic_search_repository = elastic_search_repository

    def count_words_frequency(self, lyrics_list: List[Lyrics]) -> dict:
        if not lyrics_list:
            raise exceptions.LyricsNotFound

        docs_ids = [str(lyrics.id) for lyrics in lyrics_list]
        result = {}

        es_result = self.__elastic_search_repository.find_terms(docs_ids)

        for documents in es_result['docs']:
            for term, frequency in documents['term_vectors']['lyrics']['terms'].items():
                term = re.sub(r'\W+', '', term)
                if term in STOP_WORDS:
                    continue

                if term in result:
                    result[term] += frequency['term_freq']
                    continue

                result[term] = frequency['term_freq']
        return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))


class MongoStaticsCount(StatisticCount):

    def count_words_frequency(self, lyrics_list: List[Lyrics]) -> dict:
        if not lyrics_list:
            raise exceptions.LyricsNotFound

        result = {}
        for lyrics in lyrics_list:
            lyrics_words = lyrics.lyrics.split(' ')

            for lyrics_word in lyrics_words:
                lyrics_word = lyrics_word.lower()

                if lyrics_word in STOP_WORDS:
                    continue

                if lyrics_word in result:
                    result[lyrics_word] += 1
                    continue

                result[lyrics_word] = 1

        return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))


def create_statistic(repository):

    if isinstance(repository, MongoRepository):
        return MongoStaticsCount()

    if isinstance(repository, ElasticSearchRepository):
        return ESStaticsCount(repository)

    raise exceptions.InvalidRepository
