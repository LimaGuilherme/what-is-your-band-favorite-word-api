from typing import List

import spotipy
import urllib
import requests
import lxml.html

from spotipy.oauth2 import SpotifyClientCredentials
from io import StringIO, BytesIO


from app import exceptions


class Lyrics(object):
    
    def __init__(self, artist, album, track, lyrics, lyric_id=None):
        self.id = lyric_id
        self.artist = artist
        self.album = album
        self.track = track
        self.lyrics = lyrics


class ArtistService(object):

    def __init__(self, lyrics_searcher, statistic, repository):
        self.lyrics_searcher = lyrics_searcher
        self.statistic = statistic
        self.lyrics_repository = repository

    def count_frequency(self, artist):
        lyrics_list = self.lyrics_repository.get_by_artist(artist)
        return self.statistic.count_words_frequency(lyrics_list)

    def index(self, artist):
        lyrics_list = self.lyrics_searcher.get_lyrics(artist)
        for lyrics in lyrics_list:
            self.lyrics_repository.save(lyrics)


class LyricsSearcher(object):

    def __init__(self, albums_searcher, track_searcher):
        self.albums_searcher = albums_searcher
        self.track_searcher = track_searcher

    def lyricsTransformCase(self, s):
        words = s.split()
        new_words = []
        for word in words:
            new_words.append(word[0].capitalize() + word[1:])
        s = "_".join(new_words)
        s = s.replace("<", "Less_Than")
        s = s.replace(">", "Greater_Than")
        s = s.replace("#", "Number_")  # FIXME: "Sharp" is also an allowed substitution
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

    def noname(self, artist, title):
        try:
            base_url = "https://lyrics.wikia.com/"
            page_name = '{}:{}'.format(self.lyricsTransformCase(artist), self.lyricsTransformCase(title))
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
        client_credentials_manager = SpotifyClientCredentials(client_id='f048a48923d64486a1e4f4e76921e1c1',
                                                              client_secret='52a4fad0604c447fa4f6d07827ec5d62')
        self.__spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_album_tracks(self, album):
        album_tracks = []

        results = self.__spotify_client.search(q="album:" + album, type="album")

        if not results["albums"]["items"]:
            raise exceptions.AlbumNotFound
        album_id = results["albums"]["items"][0]["uri"]

        tracks = self.__spotify_client.album_tracks(album_id)
        for track in tracks["items"]:
            album_tracks.append(track["name"])
        return album_tracks


class AlbumsSearcher(object):

    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id='f048a48923d64486a1e4f4e76921e1c1',
                                                              client_secret='52a4fad0604c447fa4f6d07827ec5d62')
        self.__spotify_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def remove_remaster_and_live_albums(self, albums):
        pass

    def get_albums(self, artist):
        results = self.__spotify_client.search(q="artist:" + artist, type="artist")
        items = results["artists"]["items"]
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


if __name__ == '__main__':
    albums_searcher = AlbumsSearcher()

    track_searcher = TrackSearcher()

    lyrics_searcher = LyricsSearcher(albums_searcher, track_searcher)

    lyrics = lyrics_searcher.get_lyrics('Behemoth')
    # lyrics = [{'artist': 'artist', 'album': 'album', 'track': 'track', 'lyric': 'lyric'}]
    for lyric in lyrics:
        lyrics_what = Lyrics(*lyric)


