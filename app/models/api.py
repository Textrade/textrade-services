import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

import config
from .base import BaseModel, db
from app.core.tools import check_hash, hash_password


class ApiUser(BaseModel, db.Model):
    __tablename__ = "api_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    joined = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, username, password, description):
        self.username = username
        self.password = hash_password(password)
        self.description = description

    def __repr__(self):
        return "<API User: {}>".format(self.username)

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (BadSignature, SignatureExpired):
            return None
        else:
            user = ApiUser.query.filter_by(id=data['id']).first()
            return user

    def verify_password(self, password):
        return check_hash(self.password, password)

    def generate_auth_token(self, expires=3.15576E+07):
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def get_user(username):
        return ApiUser.query.filter_by(username=username).first()

    @staticmethod
    def build_from_args(**kwargs):
        pass

    def get_dict(self):
        pass
