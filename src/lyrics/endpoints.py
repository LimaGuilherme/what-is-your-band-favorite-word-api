# -*- coding: utf-8 -*-

from src.lyrics import exceptions
from src.lyrics.base.endpoints import ResourceBase
from src.web_app import get_api

api = get_api()


class ArtistResource(ResourceBase):

    def __init__(self, artist_service):
        super(ArtistResource, self).__init__()
        self.artist_service = artist_service

    def get(self, artist):
        try:
            words_frequency = self.artist_service.count_frequency(artist)
            return self.response(words_frequency)
        except exceptions.ElasticSearchConnectionError:
            return self.return_elastic_search_connection_error()
        except exceptions.ArtistNotFound:
            return self.return_no_artist_found()
        except exceptions.LyricsNotFound:
            return self.return_no_lyrics_were_found()

    def post(self, artist):
        try:
            self.artist_service.index(artist)
            return self.return_ok()
        except exceptions.LyricsNotFound:
            return self.return_no_lyrics_were_found()
        except exceptions.ArtistNotFound:
            return self.return_no_artist_found()

    def delete(self):
        return self.return_method_not_allowed()

    def put(self):
        return self.return_method_not_allowed()


def register(artist_service) -> None:
    api.add_resource(ArtistResource,
                     '/api/artists/<string:artist>/lyrics',
                     resource_class_kwargs={'artist_service': artist_service})
