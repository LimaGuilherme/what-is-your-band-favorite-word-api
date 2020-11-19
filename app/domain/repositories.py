
import elasticsearch
from app import exceptions
from elasticsearch_dsl import Document, Text

from typing import List
from app.domain.entity import Lyrics


class ElasticSearchRepository(object):

    def __init__(self, elastic_search_connection):
        self.__elastic_search_connection = elastic_search_connection

    def save(self, lyrics: Lyrics) -> None:
        lyrics_document = ESLyricsDocument(artist=lyrics.artist, lyrics=lyrics.lyrics, track=lyrics.track, album=lyrics.album)
        try:
            lyrics_document.save()
        except elasticsearch.TransportError as ex:
            print('transport', ex)
            return str(ex)
        except Exception as ex:
            print('ex generica', ex)
            return str(ex)

    def get_by_artist(self, artist: str) -> List[Lyrics]:
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
        if not lyrics_list:
            raise exceptions.LyricsNotFound
        return lyrics_list


class ESLyricsDocument(Document):

    artist = Text()
    lyrics = Text()
    track = Text()
    album = Text()

    class Index:
        name = 'lyrics'
