import spotipy
import urllib
import requests
import lxml.html

from typing import List
from io import BytesIO

from bs4 import BeautifulSoup
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

    def request_song_info(self, track_name, track_artist):
        self.track_name = track_name
        self.track_artist = track_artist
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + 'ntyBy8mQc2YoI_qIscfE3qCPRBrVAltVt-CN7zZlBNl6ybmedMoJECpDBWfHUAJx'}
        search_url = base_url + '/search'
        data = {'q': track_name + ' ' + track_artist}
        response = requests.get(search_url, data=data, headers=headers)
        self.response = response
        return self.response

    def check_hits(self):
        json = self.response.json()
        remote_song_info = None
        for hit in json['response']['hits']:
            if self.track_artist.lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break
        self.remote_song_info = remote_song_info
        return self.remote_song_info

    def get_url(self):
        song_url = self.remote_song_info['result']['url']
        self.song_url = song_url
        return self.song_url

    def scrape_lyrics(self):
        page = requests.get(self.song_url)
        html = BeautifulSoup(page.text, 'html.parser')
        lyrics1 = html.find("div", class_="lyrics")
        lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
        if lyrics1:
            lyrics = lyrics1.get_text()
        elif lyrics2:
            lyrics = lyrics2.get_text()
        elif lyrics1 == lyrics2 == None:
            lyrics = None
        return lyrics

    def get_breno(self, artist, track):
        response = self.request_song_info(track, artist)
        remote_song_info = self.check_hits()
        if remote_song_info == None:
            lyrics = None
        else:
            url = self.get_url()
            lyrics = self.scrape_lyrics()
        return lyrics

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
        albums = self.albums_searcher.remove_remaster_and_live_albums(albums)
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
                    lyric = self.get_breno(artist, track)
                    # lyric = self.noname(artist, track)
                    if lyric:
                        track_lyrics.append(Lyrics(artist=artist, album=album, track=track, lyrics=lyric))
                except Exception as ex:
                    continue
        print('track_lyrics')
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
                               'exclusive',  'gold', 'edition', 'commentary', 'remaster', 'acoustic']
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
