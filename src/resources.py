# -*- coding: utf-8 -*-

import re

from functools import wraps
from flask import Response
from flask_restful import Resource

from src import configurations as config_module, exceptions

config = config_module.get_config()


def not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return Response('{"result": "Method Not Allowed"}', 405, content_type='application/json')
    return decorated_function


class ResourceBase(Resource):

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def snake_to_camel(name):
        result = []
        for index, part in enumerate(name.split('_')):
            if index == 0:
                result.append(part.lower())
            else:
                result.append(part.capitalize())
        return ''.join(result)

    def transform_key(self, data, method):
        if isinstance(data, dict):
            return {method(key): self.transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.transform_key(value, method) for key, value in item.items()}
        return data

    def response(self, data_dict):
        return self.transform_key(data_dict, self.snake_to_camel)

    def return_ok(self, **extra):
        response = {'result': 'OK'}
        if extra is not None:
            response.update(extra)
        return response

    def return_elastic_search_connection_error(self):
        return {'result': 'error', 'exception': "Maybe your elastic search isn't working"}, 502

    def return_no_lyrics_were_found(self):
        return {'result': 'error', 'exception': 'Sadly no lyrics were found'}, 404

    def return_no_artist_found(self):
        return {'result': 'error', 'exception': 'This artist seems invalid, perhaps you misspelled'}, 404

    def return_unexpected_error(self, exception=None):
        return {'result': 'error', 'error': 'General Error', 'exception': str(exception)}, 500

    def return_artist_not_send(self, exception=None):
        return {'result': 'error', 'error': 'Artist Not Received', 'exception': str(exception)}, 400

    def return_invalid_repository(self):
        return {'result': 'error', 'error': 'Invalid Repository, You should use elasticsearch or mongodb'}, 405


class ArtistResource(ResourceBase):

    def __init__(self, artist_service):
        self.artist_service = artist_service

    def get(self, artist):
        try:
            words_frequency = self.artist_service.count_frequency(artist)
            return self.response({'words_frequency': words_frequency})
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

    @not_allowed
    def delete(self):
        pass

    @not_allowed
    def put(self):
        pass
