from time import sleep

import elasticsearch
import pymongo

from elasticsearch_dsl.connections import connections as es_connections
from elasticsearch_dsl import Document, Text, Index
from typing import List

from src.lyrics import exceptions, elastisearch_configurations
from src.lyrics.entity import Lyrics

from src import configurations as config_module
from src.lyrics.exceptions import ConfigError

'''
This is so because there is a coupling between the statistics module 
and the repository in the case of the CLI
'''
try:
    full_config = config_module.get_config('full')
    elasticsearch_index = full_config.ELASTICSEARCH_INDEX
except ConfigError:
    elasticsearch_index = 'lyrics'
    pass


class ElasticSearchRepository(object):

    def __init__(self, elastic_search_connection, configurations):
        self.__elastic_search_connection = elastic_search_connection
        self.__configurations = configurations

    def find_terms(self, docs_ids: List[str]):
        return self.__elastic_search_connection.mtermvectors(index=self.__configurations.ELASTICSEARCH_INDEX,
                                                             ids=docs_ids,
                                                             fields=['lyrics'],
                                                             field_statistics=False,
                                                             term_statistics=False,
                                                             payloads=True)

    def save(self, lyrics: Lyrics) -> None:
        if not self.__elastic_search_connection.indices.exists(self.__configurations.ELASTICSEARCH_INDEX):
            self.create_index()

        lyrics_document = ESLyricsDocument(artist=lyrics.artist,
                                           lyrics=lyrics.lyrics,
                                           track=lyrics.track,
                                           album=lyrics.album)
        lyrics_document.save()

    def create_index(self):
        index = Index(name=self.__configurations.ELASTICSEARCH_INDEX)
        index.create()
        self.__elastic_search_connection.indices.close(index=self.__configurations.ELASTICSEARCH_INDEX)
        self.__elastic_search_connection.indices.put_settings(body=elastisearch_configurations.SETTINGS,
                                                              index=self.__configurations.ELASTICSEARCH_INDEX)
        self.__elastic_search_connection.indices.put_mapping(doc_type='document',
                                                             body=elastisearch_configurations.MAPPING,
                                                             include_type_name=True,
                                                             index=self.__configurations.ELASTICSEARCH_INDEX)
        self.__elastic_search_connection.indices.open(index=self.__configurations.ELASTICSEARCH_INDEX)

    def delete_index(self):
        self.__elastic_search_connection.indices.delete(index=self.__configurations.ELASTICSEARCH_INDEX)

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
        sleep(2)
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
        name = elasticsearch_index


class MongoRepository:

    def __init__(self, mongo_db, configurations):
        self.__mongo_db = mongo_db
        self.__collection = self.__mongo_db[configurations.MONGO_COLLECTION]
        self.__configurations = configurations

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
        self.__collection.drop()

    def save(self, lyrics: Lyrics) -> None:
        self.__collection.insert_one(
            {
                'artist': lyrics.artist,
                'lyrics': lyrics.lyrics,
                'track': lyrics.track,
                'album': lyrics.album
            }
        )


def create_repository(configurations):

    if configurations.REPOSITORY == 'mongodb':
        mongo_client = pymongo.MongoClient(configurations.MONGO_HOST, int(configurations.MONGO_PORT))
        mongo_lyrics_db = mongo_client['local']
        return MongoRepository(mongo_lyrics_db, configurations)

    if configurations.REPOSITORY == 'elasticsearch':
        elasticsearch_connection = es_connections.create_connection(
            hosts=[{'host': configurations.ELASTICSEARCH_HOST,
                    'port': int(configurations.ELASTICSEARCH_PORT),
                    'use_ssl': False}],
            verify_certs=False,
            connection_class=elasticsearch.RequestsHttpConnection)

        return ElasticSearchRepository(elasticsearch_connection, configurations)

    raise exceptions.InvalidRepository
