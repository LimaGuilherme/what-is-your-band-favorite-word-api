import elasticsearch

from elasticsearch_dsl import Document, Text
from typing import List

from src import exceptions
from src.domain.entity import Lyrics


class ElasticSearchRepository(object):

    def __init__(self, elastic_search_connection):
        self.__elastic_search_connection = elastic_search_connection

    def save(self, lyrics: Lyrics) -> None:
        lyrics_document = ESLyricsDocument(artist=lyrics.artist,
                                           lyrics=lyrics.lyrics,
                                           track=lyrics.track,
                                           album=lyrics.album)
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
        documents = self.__query_documents(artist)
        for lyrics_document in documents['hits']['hits']:
            lyrics_list.append(Lyrics(lyrics_document['_source']['artist'],
                                      lyrics_document['_source']['album'],
                                      lyrics_document['_source']['track'],
                                      lyrics_document['_source']['lyrics'],
                                      lyrics_document['_id'])
                               )
        return lyrics_list

    def __query_documents(self, artist):
        try:
            searcher = ESLyricsDocument.search().query("match", artist=artist).params(size=1000, timeout='150s')
            documents = searcher.execute()
        except elasticsearch.ConnectionError:
            raise exceptions.ElasticSearchConnectionError
        return documents


class ESLyricsDocument(Document):

    artist = Text()
    lyrics = Text()
    track = Text()
    album = Text()

    class Index:
        name = 'lyrics'


class MongoRepository:

    def __init__(self, mongo_db):
        self.__mongo_db = mongo_db
        self.__collection = self.__mongo_db['lyrics']

    def get_by_artist(self, artist: str) -> List[Lyrics]:
        lyrics_list = []
        for lyrics_document in self.__collection.find({"artist": artist}):
            lyrics_list.append(Lyrics(lyrics_document['artist'],
                                      lyrics_document['album'],
                                      lyrics_document['track'],
                                      lyrics_document['lyrics'],
                                      lyrics_document['_id'])
                               )
        return lyrics_list

    def save(self, lyrics: Lyrics) -> None:
        self.__collection.insert_one(
            {
                'artist': lyrics.artist,
                'lyrics': lyrics.lyrics,
                'track': lyrics.track,
                'album': lyrics.album
            }
        )
