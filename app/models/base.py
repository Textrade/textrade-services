from app import db

LAZY = 'dynamic'


class BaseModel:
    abstract = True

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def get_dict(self):
        pass

    @staticmethod
    def build_from_args(**kwargs):
        pass

    class ModelError(Exception):
        pass

    class NotFound(Exception):
        pass
