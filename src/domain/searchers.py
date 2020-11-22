import spotipy
import requests

from typing import List
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials

from src import exceptions, configurations as config_module
from src.domain.entity import Lyrics

config = config_module.get_config()


class LyricsSearcher(object):

    def __init__(self, albums_searcher, track_searcher):
        self.albums_searcher = albums_searcher
        self.track_searcher = track_searcher
        self.__genius_search_url = 'https://api.genius.com/search'
        self.__genius_token = config.GENIUS_ACCESS_TOKEN

    def request_song_info(self, track_name, track_artist):
        return requests.get(url=self.__genius_search_url,
                            data={'q': track_name + ' ' + track_artist},
                            headers={'Authorization': 'Bearer ' + self.__genius_token})

    def check_hits(self, response, artist):
        json = response.json()
        remote_song_info = None
        for hit in json['response']['hits']:
            if artist.lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break
        return remote_song_info

    def scrape_lyrics(self, remote_song_info):
        page = requests.get(remote_song_info['result']['url'])
        html = BeautifulSoup(page.text, 'html.parser')
        lyrics = None

        lyrics_one = html.find("div", class_="lyrics")
        if lyrics_one:
            lyrics = lyrics_one.get_text()
            return lyrics

        lyrics_two = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
        if lyrics_two:
            lyrics = lyrics_two.get_text()
            return lyrics

        return lyrics

    def get_breno(self, artist, track):
        response = self.request_song_info(track, artist)
        remote_song_info = self.check_hits(response, artist)

        if remote_song_info:
            lyrics = self.scrape_lyrics(remote_song_info)
            return lyrics

        return None

    def get_lyrics(self, artist: str) -> List[Lyrics]:
        albums = self.albums_searcher.get_albums(artist)

        if not albums:
            raise exceptions.AlbumsNotFound

        albums = self.albums_searcher.remove_remaster_and_live_albums(albums)
        albums_to_tracks = {}
        track_lyrics = []
        for album in albums:
            try:
                if not albums_to_tracks.get(album):
                    albums_to_tracks[album] = []
                albums_to_tracks[album] = self.track_searcher.get_album_tracks(album)
            except Exception as ex:
                continue

        for album, tracks in albums_to_tracks.items():
            for track in tracks:
                try:
                    lyric = self.get_breno(artist, track)
                    if lyric:
                        track_lyrics.append(Lyrics(artist=artist, album=album, track=track, lyrics=lyric))
                except Exception as ex:
                    continue
        return track_lyrics


class TrackSearcher(object):

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIFY_CLIENT_ID,
                                                              client_secret=config.SPOTIFY_CLIENT_SECRET)
        self.__spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_album_tracks(self, album: str) -> List:
        album_tracks = []

        results = self.__spotify_client.search(q="album:" + album, type="album")

        if not results["albums"]["items"]:
            raise exceptions.AlbumsNotFound
        album_id = results["albums"]["items"][0]["uri"]

        tracks = self.__spotify_client.album_tracks(album_id)
        for track in tracks["items"]:
            album_tracks.append(track["name"])
        return album_tracks


class AlbumsSearcher(object):

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=config.SPOTIFY_CLIENT_ID,
                                                              client_secret=config.SPOTIFY_CLIENT_SECRET)
        self.__spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def remove_remaster_and_live_albums(self, albums: list) -> List:
        acceptable_albums = []
        unacceptable_albums = ['instrumental', 'international', 'live', 'version',
                               'limited', 'mtv', 'bonus', 'tour', 'anniversary', 'standard', 'track',
                               'exclusive', 'gold', 'edition', 'commentary', 'remaster', 'acoustic']
        for album in albums:
            this_album_album_is_acceptable = True
            album = album.replace('(', '')
            album = album.replace(')', '')

            album_title = album.split(sep=" ")

            for album_tittles in album_title:
                if album_tittles.lower() in unacceptable_albums:
                    this_album_album_is_acceptable = False
                    break

            if this_album_album_is_acceptable:
                acceptable_albums.append(album)

        return acceptable_albums

    def get_albums(self, artist: str) -> List:
        results = self.__spotify_client.search(q="artist:" + artist, type="artist")
        items = results["artists"]["items"]
        if not items:
            raise exceptions.AlbumsNotFound
        artist_item = items[0]

        albums = []
        albums_titles = []
        results = self.__spotify_client.artist_albums(artist_item["id"],
                                                      album_type="album")
        albums.extend(results["items"])
        while results["next"]:
            results = self.__spotify_client.next(results)
            albums.extend(results["items"])
        seen = set()
        albums.sort(key=lambda album: album["name"].lower())

        for album in albums:
            album_tittle = album["name"]
            if album_tittle not in seen:
                print(" " + album_tittle)
                seen.add(album_tittle)
                albums_titles.append(album_tittle)
        return albums_titles
