# -*- coding: utf-8 -*-

from functools import wraps
import re

from flask import request, g, Response
from flask_restful import Resource

from app import  config as config_module

config = config_module.get_config()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = getattr(g, 'authenticated', False)
        if not authenticated:
            return Response('{"result": "Not Authorized"}', 401, content_type='application/json')
        return f(*args, **kwargs)
    return decorated_function


def not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return Response('{"result": "Method not allowed"}', 405, content_type='application/json')
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

    def payload(self):
        payload = {}
        try:
            if request.json:
                payload.update(self.transform_key(request.json, self.camel_to_snake))
        except Exception as Ex:
            pass
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        return payload

    def response(self, data_dict):
        return self.transform_key(data_dict, self.snake_to_camel)

    def return_ok(self, **extra):
        result = {'result': 'OK'}
        if extra is not None:
            result.update(extra)
        return result

    def return_deleted(self):
        return {'result': 'OK'}, 204

    def return_not_authorized(self):
        return {'result': 'Not Authorized'}, 401

    def return_forbidden(self):
        return {'result': 'Forbidden'}, 403

    def return_not_found(self, exception=None):
        return {'result': 'error', 'error': 'Not Found', 'exception': str(exception)}, 404

    def return_unexpected_error(self, exception=None):
        return {'result': 'error', 'error': 'General Error', 'exception': str(exception)}, 500

    def return_artist_not_send(self, exception=None):
        return {'result': 'error', 'error': 'Artist Not Received', 'exception': str(exception)}, 400

    def return_bad_request(self, exception=None):
        return {'result': 'error', 'error': 'Bad Request', 'exception': str(exception)}, 400

    def return_bad_parameters(self, exception=None):
        return {'result': 'error', 'error': 'Bad Parameters', 'exception': str(exception)}, 500


class ArtistResource(ResourceBase):

    def __init__(self, artist_service):
        self.artist_service = artist_service

    def get(self, artist):
        if artist:
            words_frequency = self.artist_service.count_frequency(artist)
            return self.response({'words_frequency': words_frequency})
        return self.return_artist_not_send()

    @not_allowed
    def delete(self, something_id):
        pass

    def post(self, artist):
        if artist:
            self.artist_service.index(artist)
            return self.return_ok()
        return self.return_artist_not_send()

    @not_allowed
    def put(self, something_id):
        pass


class HealthCheckResource(ResourceBase):

    def get(self):
        return self.response({'yes': 'i am ok'})

    @not_allowed
    def post(self):
        pass

    @not_allowed
    def put(self):
        pass

    @not_allowed
    def delete(self):
        pass
