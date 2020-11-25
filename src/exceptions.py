class BadParameter(Exception):
    pass


class NotAuthorized(Exception):
    pass


class UnexpectedError(Exception):
    pass


class NotFound(Exception):
    pass


class RepositoryError(Exception):
    pass


class ConfigClassNotFound(Exception):
    pass


class AlbumsNotFound(Exception):
    pass


class LyricsNotFound(Exception):
    pass


class ElasticSearchConnectionError(Exception):
    pass


class InvalidRepository(Exception):
    pass


class ArtistNotFound(Exception):
    pass
