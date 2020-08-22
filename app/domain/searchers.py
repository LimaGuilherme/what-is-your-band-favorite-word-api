import spotipy
import urllib
import requests
import lxml.html

from typing import List
from io import BytesIO
from spotipy.oauth2 import SpotifyClientCredentials


from app import exceptions
from app import config as config_module
from app.domain.entity import Lyrics

config = config_module.get_config()


class LyricsSearcher(object):

    def __init__(self, albums_searcher, track_searcher):
        self.albums_searcher = albums_searcher
        self.track_searcher = track_searcher

    def lyrics_transform_case(self, s: str) -> str:
        words = s.split()
        new_words = []
        for word in words:
            new_words.append(word[0].capitalize() + word[1:])
        s = "_".join(new_words)
        s = s.replace("<", "Less_Than")
        s = s.replace(">", "Greater_Than")
        s = s.replace("#", "Number_")
        s = s.replace("[", "(")
        s = s.replace("]", ")")
        s = s.replace("{", "(")
        s = s.replace("}", ")")
        try:
            # Python 3 version
            s = urllib.parse.urlencode([(0, s)])[2:]
        except AttributeError:
            # Python 2 version
            s = urllib
        return s

    def noname(self, artist: str, title: str) -> str:
        try:
            base_url = "https://lyrics.wikia.com/"
            page_name = '{}:{}'.format(self.lyrics_transform_case(artist), self.lyrics_transform_case(title))
            url = base_url + page_name
            response = requests.get(url)
            doc = lxml.html.parse(BytesIO(response.content), base_url=url)
        except IOError:
            raise
        try:
            lyric_box = doc.getroot().cssselect(".lyricbox")[0]
        except IndexError as ex:
            raise
        except Exception as ex:
            raise

        if len(doc.getroot().cssselect(".lyricbox a[title=\"Instrumental\"]")):
            return None

        _lyrics = []
        if lyric_box.text is not None:
            _lyrics.append(lyric_box.text)
        for node in lyric_box:
            if str(lyric_box.tag).lower() == "br":
                _lyrics.append("\n")
            if node.tail is not None:
                _lyrics.append(node.tail)
        return "".join(_lyrics).strip()

    def get_lyrics(self, artist: str) -> List[Lyrics]:
        albums = self.albums_searcher.get_albums(artist)
        if not albums:
            raise exceptions.AlbumsNotFound
        # albums = self.albums_searcher.remove_remaster_and_live_albums(albums)
        albums_to_tracks = {}
        track_lyrics = []

        for album in albums:
            try:
                if not albums_to_tracks.get(album):
                    albums_to_tracks[album] = []
                albums_to_tracks[album] = self.track_searcher.get_album_tracks(album)
            except:
                continue

        for album, tracks in albums_to_tracks.items():
            for track in tracks:
                try:
                    lyric = self.noname(artist, track)
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
        pass

    def get_albums(self, artist: str) -> List:
        results = self.__spotify_client.search(q="artist:" + artist, type="artist")
        items = results["artists"]["items"]
        if not items:
            raise exceptions.AlbumsNotFound
        artist_item = items[0]

        albums = []
        albums_titles = []
        results = self.__spotify_client.artist_albums(artist_item["id"], album_type="album")
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
