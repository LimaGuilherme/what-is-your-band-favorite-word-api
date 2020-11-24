from typing import List

from src import exceptions
from src.domain.entity import Lyrics
from src.domain.stop_words import STOP_WORDS


class StatisticCount:
    pass


class ESStaticsCount(object):

    def __init__(self, elastic_search_connection):
        self.__elastic_search_connection = elastic_search_connection

    def count_words_frequency(self, lyrics_list: List[Lyrics]) -> dict:
        if not lyrics_list:
            raise exceptions.LyricsNotFound

        docs_ids = []
        result = {}

        for lyrics in lyrics_list:
            docs_ids.append(str(lyrics.id))

        es_result = self.__elastic_search_connection.mtermvectors(index='lyrics',
                                                                  ids=docs_ids,
                                                                  fields=['lyrics'],
                                                                  field_statistics=False,
                                                                  term_statistics=False,
                                                                  payloads=True)

        for documents in es_result['docs']:
            for term, frequency in documents['term_vectors']['lyrics']['terms'].items():
                if term in STOP_WORDS:
                    continue

                if term in result:
                    result[term] += frequency['term_freq']
                    continue

                result[term] = frequency['term_freq']
        return dict(sorted(result.items(), key=lambda item: item[1], reverse=True))


class MongoStaticsCount(object):

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
