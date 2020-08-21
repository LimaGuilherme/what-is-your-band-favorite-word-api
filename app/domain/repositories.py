import elasticsearch
import elasticsearch_dsl

from app.domain.stop_words.english import STOP_WORDS
from app.domain.application_service import Lyrics


class ElasticSearchRepository(object):

    def __init__(self, elastic_search_connection):
        self.__elastic_search_connection = elastic_search_connection

    def save(self, lyrics):
        lyrics_document = ESLyricsDocument(artist=lyrics.artist, lyrics=lyrics.lyrics, track=lyrics.track, album=lyrics.album)
        try:
            lyrics_document.save()
        except elasticsearch.TransportError as ex:
            return str(ex)
        except Exception as ex:
            return str(ex)
        return lyrics

    def get_by_artist(self, artist):
        lyrics_list = []
        searcher = ESLyricsDocument.search().query("match", artist=artist).params(size=1000, timeout='150s')
        es_result = searcher.execute()
        for lyrics_document in es_result['hits']['hits']:
            lyrics_list.append(Lyrics(lyrics_document['_source']['artist'],
                                      lyrics_document['_source']['album'],
                                      lyrics_document['_source']['track'],
                                      lyrics_document['_source']['lyrics'],
                                      lyrics_document['_id'])
                               )
        return lyrics_list


class ESLyricsDocument(elasticsearch_dsl.DocType):

    artist = elasticsearch_dsl.Text()
    lyrics = elasticsearch_dsl.Text()
    track = elasticsearch_dsl.Text()
    album = elasticsearch_dsl.Text()

    class Index:
        name = 'lyrics'
        doc_type = '_doc'

    class Meta:
        doc_type = '_doc'


