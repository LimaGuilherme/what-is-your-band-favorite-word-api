# -*- coding: utf-8 -*-

from flask_restful import Api

from src.domain.album_searcher import AlbumsSearcher
from src.domain.application_service import ArtistLyricsService
from src.domain.artist_searcher import ArtistSearcher
from src.domain.repositories import create_repository
from src.domain.lyrics_searcher import LyricsSearcher
from src.domain.track_searcher import TrackSearcher
from src.domain.statitics import create_statistic

from src import resources, configurations as config_module

config = config_module.get_config()

albums_searcher = AlbumsSearcher()
track_searcher = TrackSearcher()
lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)
artist_searcher = ArtistSearcher()

repository = create_repository()
statistic = create_statistic(repository)

artist_service = ArtistLyricsService(lyrics_searcher, statistic, repository, artist_searcher)


def create_api(app):
    api = Api(app)
    api.add_resource(resources.ArtistResource,
                     '/api/artists/<string:artist>/lyrics',
                     resource_class_kwargs={'artist_service': artist_service})
