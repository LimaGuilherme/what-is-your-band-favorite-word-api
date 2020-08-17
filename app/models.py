import datetime
import unicodedata

from app import database, exceptions

db = database.AppRepository.db


class AbstractModel(object):
    class AlreadyExist(Exception):
        pass

    class NotExist(Exception):
        pass

    class RepositoryError(Exception):
        pass

    @classmethod
    def add_in_batch(cls, instance):
        db.session.add(instance)

    @classmethod
    def close_session(cls):
        db.session.remove()

    @classmethod
    def commit_in_batch(cls):
        db.session.commit()
        db.session.flush()

    def commit_session(self):
        db.session.commit()

    @classmethod
    def create_from_json(cls, json_data):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.save_db()
            return instance
        except Exception as ex:
            raise cls.RepositoryError(str(ex))

    @classmethod
    def create_from_json_without_commit(cls, json_data):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.save_db(commit=False)
            return instance
        except Exception as ex:
            raise cls.RepositoryError(str(ex))

    def delete_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def get_list(cls, *args, **kwargs):
        return cls.query.filter_by()

    @classmethod
    def get_item(cls, item_id):
        item = cls.query.get(item_id)
        if not item:
            raise exceptions.NotFound
        else:
            return item

    @classmethod
    def get_all_ids_in(cls, items_id):
        return db.session.query(cls).filter(cls.id.in_(items_id)).all()

    @classmethod
    def roll_back_session(cls):
        db.session.rollback()

    @classmethod
    def one_or_none(cls, **kwargs):
        return cls.filter(**kwargs).one_or_none()

    @classmethod
    def slugify(cls, value):
        slug = unicodedata.normalize('NFKD', value)
        slug = slug.replace(' ', '-')
        slug = slug.encode('ascii', 'ignore').lower()
        return slug

    def save_db(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        else:
            db.session.flush()

    @classmethod
    def update_from_json(cls, item_id, json_data):
        try:
            instance = cls.get_item(item_id)
            instance.set_values(json_data)
            instance.save_db()
            return instance
        except db.IntegrityError as ex:
            raise exceptions.RepositoryError(str(ex))

    @classmethod
    def save_in_batch(cls, items):
        db.session.bulk_save_objects(items)
        db.session.commit()

    def set_values(self, json_data):
        for key, value in json_data.items():
            setattr(self, key, json_data.get(key, getattr(self, key)))


class SomeTable(db.Model, AbstractModel):
    __tablename__ = 'some_table'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String)
    date_of_creation = db.Column(db.Date, default=datetime.datetime.utcnow)
