from flask import Flask

from src import configurations as config_module
from src import web_app as web_app_module

from src.lyrics import endpoints
from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import ArtistSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

from src.lyrics.application_service import APIArtistLyricsService
from src.lyrics.repositories import create_repository
from src.lyrics.statitics import create_statistic

configurations = config_module.get_config(config_type='full')
web_app = web_app_module.get_web_app()
api = web_app_module.get_api()

albums_searcher = AlbumsSearcher(configurations)
track_searcher = TrackSearcher(configurations)
lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher, configurations)
artist_searcher = ArtistSearcher(configurations)

repository = create_repository(configurations)
statistic = create_statistic(repository)

artist_service = APIArtistLyricsService(lyrics_searcher, statistic, repository, artist_searcher)

endpoints.register(
    artist_service=artist_service,
)
