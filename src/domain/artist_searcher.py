import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

from src import configurations as config_module

config = config_module.get_config()


class ArtistSearcher:

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIFY_CLIENT_ID,
                                                              client_secret=config.SPOTIFY_CLIENT_SECRET)
        self.__spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def check_if_artist_exists(self, artist: str) -> bool:
        artist = self.__spotify_client.search(q="artist:" + artist, type="artist")
        return True if artist['artists']['total'] > 0 else False
