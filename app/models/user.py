import datetime

from app.models.base import db, BaseModel


class User(BaseModel, db.Model):
    """User model"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    joined = db.Column(db.DateTime, default=datetime.datetime.now)
    university_email = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)
    activated_on = db.Column(db.DateTime, nullable=True, default=None)
    role = db.Column(db.String(255), db.ForeignKey('user_role.role'))

    def __init__(self, first_name, last_name,
                 username, password, university_email, role):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.university_email = university_email
        self.role = role

    def __repr__(self):
        return "<User: %r>" % self.username

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(user_id):
        return User.query.filter_by(id=user_id).first()

    def get_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password,
            'joined': self.joined,
            'email': self.university_email,
            'active': self.active,
            'activated_on': self.activated_on,
            'role': self.role
        }

    def get_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def joined_to_string(self):
        return self.joined.strftime("%b. %Y")

    def is_admin(self):
        return not self.role == "costumer"

    def is_active(self):
        return self.active


class UserRole(BaseModel, db.Model):
    """UserRole table to store the different user categories and
    and control privileges for users.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(40), unique=True)

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        return "<Role: %r>" % self.role