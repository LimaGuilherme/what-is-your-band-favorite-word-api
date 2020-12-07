# -*- coding: utf-8 -*-

from flask_restful import Api

from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import ArtistSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

from src.lyrics.application_service import APIArtistLyricsService
from src.lyrics.repositories import create_repository
from src.lyrics.statitics import create_statistic

from src import resources, configurations as config_module

configurations = config_module.create_config(config_type='full')

albums_searcher = AlbumsSearcher(configurations)
track_searcher = TrackSearcher(configurations)
lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, configurations)
artist_searcher = ArtistSearcher(configurations)

repository = create_repository(configurations)
statistic = create_statistic(repository)

artist_service = APIArtistLyricsService(lyrics_searcher, statistic, repository, artist_searcher)


def create_api(app):
    api = Api(app)
    api.add_resource(resources.ArtistResource,
                     '/api/artists/<string:artist>/lyrics',
                     resource_class_kwargs={'artist_service': artist_service})
