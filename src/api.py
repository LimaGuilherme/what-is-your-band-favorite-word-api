# -*- coding: utf-8 -*-

import elasticsearch
import pymongo

from flask_restful import Api
from elasticsearch_dsl.connections import connections as es_connections

from src.domain.application_service import ArtistLyricsService
from src.domain.repositories import ElasticSearchRepository, MongoRepository
from src.domain.searchers import AlbumsSearcher, TrackSearcher, LyricsSearcher
from src.domain.statitics import ESStaticsCount, MongoStaticsCount

from src import resources, configurations as config_module

config = config_module.get_config()

elasticsearch_connection = es_connections.create_connection(
    hosts=[{'host': config.ELASTICSEARCH_HOST,
            'port': int(config.ELASTICSEARCH_PORT),
            'use_ssl': False}],
    verify_certs=False,
    connection_class=elasticsearch.RequestsHttpConnection)

mongo_client = pymongo.MongoClient(config.MONGO_HOST, int(config.MONGO_PORT))
mongo_lyrics_db = mongo_client['local']
mongo_lyrics_db.products.create_index("sku", unique=True)

albums_searcher = AlbumsSearcher()
track_searcher = TrackSearcher()
lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)

repository = MongoRepository(mongo_lyrics_db)
statistic = MongoStaticsCount(mongo_lyrics_db)

# statistic = ESStaticsCount(elasticsearch_connection)
# repository = ElasticSearchRepository(elasticsearch_connection)

artist_service = ArtistLyricsService(lyrics_searcher, statistic, repository)


def create_api(app):
    api = Api(app)
    api.add_resource(resources.ArtistResource,
                     '/api/artists/<string:artist>/lyrics',
                     resource_class_kwargs={'artist_service': artist_service})
