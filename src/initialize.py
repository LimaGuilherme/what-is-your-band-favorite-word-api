from src import configurations as config_module
from src import web_app as web_app_module

from src.lyrics import endpoints
from src.lyrics.application_service import StorageWordsService, IndexService
from src.lyrics.searchers import AlbumsSearcher
from src.lyrics.searchers import ArtistSearcher
from src.lyrics.searchers import LyricsSearcher
from src.lyrics.searchers import TrackSearcher

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

storage_word_service = StorageWordsService(lyrics_searcher, statistic, repository, artist_searcher)
index_service = IndexService(lyrics_searcher, repository, artist_searcher)

endpoints.register(
    storage_word_service=storage_word_service,
    index_service=index_service
)
