#  -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from importlib import import_module

from app import exceptions


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    ENVIRONMENT = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        if self.ENVIRONMENT is None:
            raise TypeError('You should use one of the specialized config class')
        self.SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        self.REDIS_URL = os.environ['REDIS_URL']


class ProductionConfig(Config):
    ENVIRONMENT = 'production'


class StagingConfig(Config):
    ENVIRONMENT = 'staging'
    DEBUG = True


class DevelopmentConfig(Config):
    ENVIRONMENT = 'development'
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True


class SandboxConfig(Config):
    ENVIRONMENT = 'sandbox'
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True


class TestingConfig(DevelopmentConfig):
    ENVIRONMENT = 'test'
    TESTING = True


def get_config():
    config_imports = os.environ['APP_SETTINGS'].split('.')
    config_class_name = config_imports[-1]
    config_module = import_module('.'.join(config_imports[:-1]))
    config_class = getattr(config_module, config_class_name, None)
    if not config_class:
        raise exceptions.ConfigClassNotFound('Unable to find a config class in {}'.format(os.environ['APP_SETTINGS']))
    return config_class()
