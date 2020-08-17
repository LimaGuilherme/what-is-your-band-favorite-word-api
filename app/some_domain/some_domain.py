from app import exceptions


class Entity(object):
    repository = None

    def __init__(self, db_instance):
        self.db_instance = db_instance

    @classmethod
    def create_with_id(cls, item_id):
        db_instance = cls.repository.one_or_none(id=item_id)
        if db_instance is None:
            raise exceptions.NotFound('Could not find a entity with id {}'.format(item_id))
        return cls(db_instance=db_instance)

    @classmethod
    def create_with_instance(cls, db_instance):
        return cls(db_instance)

    @classmethod
    def _create_with_keys(cls, **keys):
        db_instance = cls.repository.one_or_none(**keys)
        if db_instance is None:
            raise exceptions.NotFound('Could not find a user with keys: {}'.format(keys))
        return cls(db_instance=db_instance)
