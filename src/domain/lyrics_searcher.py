import requests

from typing import List
from bs4 import BeautifulSoup

from src import configurations as config_module
from src.domain.entity import Lyrics

config = config_module.get_config()


class LyricsSearcher:

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

    def scrape_lyrics(self, remote_song_info: str):
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

    def get_breno(self, artist: str, track: str):
        response = self.request_song_info(track, artist)
        remote_song_info = self.check_hits(response, artist)

        if remote_song_info:
            lyrics = self.scrape_lyrics(remote_song_info)
            return lyrics

        return None

    def get_lyrics(self, artist: str) -> List[Lyrics]:
        albums = self.albums_searcher.get_albums(artist)

        albums = self.albums_searcher.remove_remaster_and_live_albums(albums)
        albums_to_tracks = {}
        track_lyrics = []

        for album in albums:
            try:
                if not albums_to_tracks.get(album):
                    albums_to_tracks[album] = []
                albums_to_tracks[album] = self.track_searcher.get_tracks(album)
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
