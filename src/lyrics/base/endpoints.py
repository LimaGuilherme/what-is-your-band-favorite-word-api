from flask_restful import Resource

from src.lyrics.base.serializer import CaseStyleConverter


class ResourceBase(Resource):

    def __init__(self, *args, **kwargs):
        super(ResourceBase, self).__init__(*args, **kwargs)
        self._converter = CaseStyleConverter()

    def _serialize_in(self, data_dict: dict) -> dict:
        return self._converter.camel_to_snake(data_dict)

    def return_ok(self, **extra):
        result = {'result': 'OK'}
        if extra is not None:
            result.update(extra)
        return result

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

    def return_method_not_allowed(self):
        return {'result': 'error', 'error': 'Method Not Allowed'}, 405
