# -*- coding: utf-8 -*-

from src.lyrics import exceptions
from src.lyrics.base.endpoints import ResourceBase
from src.web_app import get_api

api = get_api()


class WordsResource(ResourceBase):

    def __init__(self, storage_word_service, index_service):
        super(WordsResource, self).__init__()
        self.storage_word_service = storage_word_service
        self.index_service = index_service

    def get(self, artist):
        try:
            words_frequency = self.storage_word_service.count_frequency(artist, 10)
            return words_frequency, 200
        except exceptions.ElasticSearchConnectionError:
            return self.return_elastic_search_connection_error()
        except exceptions.ArtistNotFound:
            return self.return_no_artist_found()
        except exceptions.LyricsNotFound:
            return self.return_no_lyrics_were_found()

    def post(self, artist):
        try:
            self.index_service.index(artist)
            return self.return_ok(), 200
        except exceptions.LyricsNotFound:
            return self.return_no_lyrics_were_found()
        except exceptions.ArtistNotFound:
            return self.return_no_artist_found()

    def delete(self, artist):
        return self.return_method_not_allowed()

    def put(self, artist):
        return self.return_method_not_allowed()


def register(storage_word_service, index_service) -> None:
    api.add_resource(WordsResource,
                     '/api/artists/<string:artist>/lyrics',
                     resource_class_kwargs={
                         'storage_word_service': storage_word_service,
                         'index_service': index_service,
                     })
