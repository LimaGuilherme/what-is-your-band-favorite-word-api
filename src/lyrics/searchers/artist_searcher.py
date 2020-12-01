import spotipy

from spotipy.oauth2 import SpotifyClientCredentials


class ArtistSearcher:

    def __init__(self, config):
        client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIFY_CLIENT_ID,
                                                              client_secret=config.SPOTIFY_CLIENT_SECRET)
        self.__spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def is_this_artist_valid(self, artist: str) -> bool:
        artist = self.__spotify_client.search(q="artist:" + artist, type="artist")
        return True if artist['artists']['total'] > 0 else False
