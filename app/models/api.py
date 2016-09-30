import datetime

from .base import BaseModel, db


class Elmer(BaseModel, db.Model):
    __tablename__ = "elmer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    who = db.Column(db.String(255))

    def __init__(self, who):
        self.who = who
