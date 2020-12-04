from dataclasses import dataclass, asdict, fields as dataclasses_fields
from abc import ABC
import json
import os

from importlib import import_module
from typing import Tuple

from src.exceptions import ConfigError


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



@dataclass
class Config(ABC):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    GENIUS_ACCESS_TOKEN: str

    @property
    def as_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def get_variables_names(cls) -> Tuple[str]:
        return tuple([str(field.name) for field in dataclasses_fields(cls)])


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


class EnvFullConfigRepository:

    def get(self) -> FullConfig:

        missing_env_vars = self.__check_for_missing_vars()

        if len(missing_env_vars) > 0:
            raise ConfigError(f'Environment variables missing: {missing_env_vars}')

        config_dict = {}
        for env_var in FullConfig.get_variables_names():
            config_dict[env_var] = os.environ[env_var]

        return FullConfig(**config_dict)

    def __check_for_missing_vars(self):
        missing_env_vars = []
        for env_var in FullConfig.get_variables_names():
            try:
                os.environ[env_var]
            except KeyError:
                missing_env_vars.append(env_var)
        return missing_env_vars


class LocalStorageSimpleConfigRepository:

    def __init__(self):
        self.__filename = '.localstorage'

    def get(self) -> SimpleConfig:
        try:
            with open(self.__filename, 'r') as localstorage:
                data = json.load(localstorage)

                missing_vars = self.__check_for_missing_vars(data)

                if len(missing_vars) > 0:
                    raise ConfigError(f'Variables missing: {missing_vars}')

                return SimpleConfig(**data)

        except FileNotFoundError:
            raise ConfigError('Cant get config because config file was not found. Try to config variables again')

    def save(self, simple_config: SimpleConfig) -> None:
        try:
            os.remove(self.__filename)
        except OSError:
            pass

        with open(self.__filename, 'w') as localstorage:
            json.dump(simple_config.as_dict, localstorage)

    def __check_for_missing_vars(self, data):
        missing_vars = []

        for env_var in SimpleConfig.get_variables_names():
            if not data.get(env_var):
                missing_vars.append(env_var)

        return missing_vars


def create_config(config_type) -> Config:
    if config_type == 'simple':
        repository = LocalStorageSimpleConfigRepository()
        simple_config = repository.get()
        return simple_config

    if config_type == 'full':
        repository = EnvFullConfigRepository()
        full_config = repository.get()
        return full_config

    raise ConfigError(f'Cant create config because the config_type {config_type} '
                      f'is invalid. Valid options: simple, full.')
