import re

from abc import ABC, abstractmethod
from typing import List

from src import exceptions
from src.lyrics.entity import Lyrics
from src.lyrics.repositories import MongoRepository, ElasticSearchRepository
from src.lyrics.stop_words import STOP_WORDS


class StatisticCount(ABC):

    @abstractmethod
    def count_words_frequency(self, lyrics_list: List[Lyrics]) -> dict:
        pass


class ESStaticsCount(StatisticCount):

    def __init__(self, elastic_search_repository):
        super(ESStaticsCount, self).__init__()
        self.__elastic_search_repository = elastic_search_repository

    def count_words_frequency(self, lyrics_list: List[Lyrics]) -> dict:
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


class CommonStatistical(StatisticCount):

    def count_words_frequency(self, lyrics_list: List[Lyrics], number_of_terms: int = None) -> dict:
        result = {}
        for lyrics in lyrics_list:

            for word in lyrics.words:
                word = word.lower()
                word = re.sub(r'\W+', '', word)

                if word in STOP_WORDS:
                    continue

                if word in result:
                    result[word] += 1
                    continue

                result[word] = 1

        result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))

        from itertools import islice

        if number_of_terms:
            return dict(islice(result.items(), number_of_terms))
        return result


def create_statistic(repository=None) -> StatisticCount:

    if not repository:
        return CommonStatistical()

    if isinstance(repository, MongoRepository):
        return CommonStatistical()

    if isinstance(repository, ElasticSearchRepository):
        return ESStaticsCount(repository)

    raise exceptions.InvalidRepository
