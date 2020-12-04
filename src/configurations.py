import os

from importlib import import_module


class ConfigCLI:
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    ENVIRONMENT = None
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    GENIUS_ACCESS_TOKEN = os.environ['GENIUS_ACCESS_TOKEN']


class DevelopmentConfigCLI(ConfigCLI):
    pass


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    ENVIRONMENT = None
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    ELASTICSEARCH_HOST = os.environ['ELASTICSEARCH_HOST']
    ELASTICSEARCH_PORT = os.environ['ELASTICSEARCH_PORT']
    GENIUS_ACCESS_TOKEN = os.environ['GENIUS_ACCESS_TOKEN']
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = os.environ['MONGO_PORT']
    REPOSITORY = os.environ['REPOSITORY']
    ELASTICSEARCH_INDEX = os.environ['ELASTICSEARCH_INDEX']
    MONGO_COLLECTION = os.environ['MONGO_COLLECTION']


class DevelopmentConfig(Config):
    ENVIRONMENT = 'development'
    DEVELOPMENT = True
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
    return config_class()


from dataclasses import dataclass
from abc import ABC


@dataclass
class Config(ABC):
    DEBUG: bool
    ENVIRONMENT: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    GENIUS_ACCESS_TOKEN: str


@dataclass
class SimpleConfig(Config):
    pass


@dataclass
class FullConfig(Config):
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: str
    MONGO_HOST: str
    MONGO_PORT: str
    REPOSITORY: str
    ELASTICSEARCH_INDEX: str
    MONGO_COLLECTION: str
