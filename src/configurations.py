import json
import os

from dataclasses import dataclass, asdict, fields as dataclasses_fields
from abc import ABC

from typing import Tuple, Union

from src.exceptions import ConfigError

__all__ = [
    'create_simple_config',
    'get_config',
    'SimpleConfig',
    'FullConfig'
]

full_config = None
simple_config = None


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


def create_simple_config(spotify_client_id, spotify_client_secret, genius_access_token) -> None:
    config_repository = LocalStorageSimpleConfigRepository()
    simple_config = SimpleConfig(
        SPOTIFY_CLIENT_ID=spotify_client_id,
        SPOTIFY_CLIENT_SECRET=spotify_client_secret,
        GENIUS_ACCESS_TOKEN=genius_access_token,
    )
    config_repository.save(simple_config)


def get_config(config_type: str) -> Union[SimpleConfig, FullConfig]:
    global full_config
    global simple_config

    if config_type == 'simple':
        if simple_config:
            return simple_config

        repository = LocalStorageSimpleConfigRepository()
        simple_config = repository.get()
        return simple_config

    if config_type == 'full':
        if full_config:
            return full_config

        repository = EnvFullConfigRepository()
        full_config = repository.get()
        return full_config

    raise ConfigError(f'Cant create config because the config_type {config_type} '
                      f'is invalid. Valid options: simple, full.')
