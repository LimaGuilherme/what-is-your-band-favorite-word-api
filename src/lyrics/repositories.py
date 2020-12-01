import elasticsearch
import pymongo

from elasticsearch_dsl.connections import connections as es_connections
from elasticsearch_dsl import Document, Text, Index
from typing import List

from src import exceptions, elastisearch_configurations
from src.lyrics.entity import Lyrics

from src import configurations as config_module

config = config_module.get_config()


class ElasticSearchRepository(object):

    def __init__(self, elastic_search_connection):
        self.__elastic_search_connection = elastic_search_connection

    def find_terms(self, docs_ids: List[str]):
        return self.__elastic_search_connection.mtermvectors(index=config.ELASTICSEARCH_INDEX,
                                                             ids=docs_ids,
                                                             fields=['lyrics'],
                                                             field_statistics=False,
                                                             term_statistics=False,
                                                             payloads=True)

    def save(self, lyrics: Lyrics) -> None:
        if not self.__elastic_search_connection.indices.exists(config.ELASTICSEARCH_INDEX):
            self.create_index()

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

    def create_index(self):
        index = Index(name=config.ELASTICSEARCH_INDEX)
        index.create()
        self.__elastic_search_connection.indices.close(index=config.ELASTICSEARCH_INDEX)
        self.__elastic_search_connection.indices.put_settings(body=elastisearch_configurations.SETTINGS,
                                                              index=config.ELASTICSEARCH_INDEX)
        self.__elastic_search_connection.indices.put_mapping(doc_type='document',
                                                             body=elastisearch_configurations.MAPPING,
                                                             include_type_name=True,
                                                             index=config.ELASTICSEARCH_INDEX)
        self.__elastic_search_connection.indices.open(index=config.ELASTICSEARCH_INDEX)

    def delete_index(self):
        self.__elastic_search_connection.indices.delete(index=config.ELASTICSEARCH_INDEX)

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
        name = config.ELASTICSEARCH_INDEX


class MongoRepository:

    def __init__(self, mongo_db):
        self.__mongo_db = mongo_db
        self.__collection = self.__mongo_db[config.MONGO_COLLECTION]

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

    def delete_collection(self) -> None:
        self.__collection[config.ELASTICSEARCH_INDEX].drop()

    def save(self, lyrics: Lyrics) -> None:
        self.__collection.insert_one(
            {
                'artist': lyrics.artist,
                'lyrics': lyrics.lyrics,
                'track': lyrics.track,
                'album': lyrics.album
            }
        )


def create_repository():

    if config.REPOSITORY == 'mongodb':
        mongo_client = pymongo.MongoClient(config.MONGO_HOST, int(config.MONGO_PORT))
        mongo_lyrics_db = mongo_client['local']
        return MongoRepository(mongo_lyrics_db)

    if config.REPOSITORY == 'elasticsearch':
        elasticsearch_connection = es_connections.create_connection(
            hosts=[{'host': config.ELASTICSEARCH_HOST,
                    'port': int(config.ELASTICSEARCH_PORT),
                    'use_ssl': False}],
            verify_certs=False,
            connection_class=elasticsearch.RequestsHttpConnection)

        return ElasticSearchRepository(elasticsearch_connection)

    raise exceptions.InvalidRepository
