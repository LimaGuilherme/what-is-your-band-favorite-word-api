# -*- coding: utf-8 -*-

from flask_restful import Api
from app import resources


def create_api(app):
    api = Api(app)
    api.add_resource(resources.SomeResource,  '/api/something/<string:something_id>')
