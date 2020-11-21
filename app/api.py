# -*- coding: utf-8 -*-

import elasticsearch

from flask_restful import Api
from elasticsearch_dsl.connections import connections

from app.domain.application_service import ArtistLyricsService
from app.domain.repositories import ElasticSearchRepository
from app.domain.searchers import AlbumsSearcher, TrackSearcher, LyricsSearcher
from app.domain.statitics import ESStaticsCount

from app import resources, config as config_module


config = config_module.get_config()

elasticsearch_connection = connections.create_connection(
    hosts=[{'host': config.ELASTICSEARCH_HOST,
            'port': int(config.ELASTICSEARCH_PORT),
            'use_ssl': False}],
    verify_certs=False,
    connection_class=elasticsearch.RequestsHttpConnection)

albums_searcher = AlbumsSearcher()
track_searcher = TrackSearcher()
lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)
elastic_searcher_repository = ElasticSearchRepository(elasticsearch_connection)
statistic = ESStaticsCount(elasticsearch_connection)

artist_service = ArtistLyricsService(lyrics_searcher, statistic, elastic_searcher_repository)


def create_api(app):
    api = Api(app)
    api.add_resource(resources.ArtistResource,
                     '/api/artists/<string:artist>/lyrics',
                     resource_class_kwargs={'artist_service': artist_service})
