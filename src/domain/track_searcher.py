from typing import List

import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

from src import configurations as config_module

config = config_module.get_config()


class TrackSearcher:

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIFY_CLIENT_ID,
                                                              client_secret=config.SPOTIFY_CLIENT_SECRET)
        self.__spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_tracks(self, album: str) -> List[str]:

        results = self.__spotify_client.search(q="album:" + album, type="album")

        if not results["albums"]["items"]:
            return []

        album_id = results["albums"]["items"][0]["uri"]
        tracks = self.__spotify_client.album_tracks(album_id)

        return [track['name'] for track in tracks["items"]]
