from typing import List

from app.domain.entity import Lyrics
from app.domain.stop_words import STOP_WORDS


class ESStaticsCount(object):

    def __init__(self, elastic_search_connection):
        self.__elastic_search_connection = elastic_search_connection

    def count_words_frequency(self, lyrics_list: List[Lyrics]) -> List:
        docs_ids = []
        result = {}

        for lyrics in lyrics_list:
            docs_ids.append(str(lyrics.id))

        es_result = self.__elastic_search_connection.mtermvectors(index='lyrics',
                                                                  doc_type='_doc',
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
        sorted_result = sorted(result.items(), key=lambda x: x[1])
        return sorted_result
