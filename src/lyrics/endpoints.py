# -*- coding: utf-8 -*-
from flask_restful import reqparse

from src.lyrics import exceptions
from src.lyrics.base.endpoints import ResourceBase
from src.web_app import get_api

api = get_api()


class LyricsResource(ResourceBase):

    def __init__(self, index_service):
        super(LyricsResource, self).__init__()
        self.index_service = index_service

    def post(self, artist):
        try:
            self.index_service.index(artist)
            return self.return_ok(), 200
        except exceptions.LyricsNotFound:
            return self.return_no_lyrics_were_found()
        except exceptions.ArtistNotFound:
            return self.return_no_artist_found()

    def get(self, artist):
        return self.return_method_not_allowed()

    def delete(self, artist):
        return self.return_method_not_allowed()

    def put(self, artist):
        return self.return_method_not_allowed()


class TopWordsResource(ResourceBase):

    def __init__(self, storage_word_service):
        super(TopWordsResource, self).__init__()
        self.storage_word_service = storage_word_service
        self.parser = reqparse.RequestParser()

    def get(self, artist):
        try:
            self.parser.add_argument('size', type=int, help='The number of top-words. Error: {error_msg} ', required=True)
            args = self.parser.parse_args()
            words_frequency = self.storage_word_service.count_frequency(artist, args['size'])
            return words_frequency, 200
        except exceptions.ElasticSearchConnectionError:
            return self.return_elastic_search_connection_error()
        except exceptions.ArtistNotFound:
            return self.return_no_artist_found()
        except exceptions.LyricsNotFound:
            return self.return_no_lyrics_were_found()

    def post(self, artist):
        return self.return_method_not_allowed()

    def delete(self, artist):
        return self.return_method_not_allowed()

    def put(self, artist):
        return self.return_method_not_allowed()


def register(storage_word_service, index_service) -> None:
    api.add_resource(TopWordsResource,
                     '/api/artists/<string:artist>/top-words',
                     resource_class_kwargs={
                         'storage_word_service': storage_word_service,
                     })

    api.add_resource(LyricsResource,
                     '/api/artists/<string:artist>/lyrics',
                     resource_class_kwargs={
                         'index_service': index_service,
                     })
