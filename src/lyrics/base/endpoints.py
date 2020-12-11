from flask_restful import Resource


class ResourceBase(Resource):

    def __init__(self, *args, **kwargs):
        super(ResourceBase, self).__init__(*args, **kwargs)

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

    def return_method_not_allowed(self):
        return {'result': 'error', 'error': 'Method Not Allowed'}, 405
