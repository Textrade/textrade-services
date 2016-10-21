import datetime

from app.models.base import db, BaseModel


class User(BaseModel, db.Model):
    """
        User model store the information about the users.
    """
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
    rating = db.Column(db.Float, default=0.0, nullable=False)
    role = db.Column(db.String(40), db.ForeignKey('user_role.role'))

    def __init__(self, first_name, last_name,
                 username, password, university_email, role):
        """
        User Constructor
        :param first_name:
        :param last_name:
        :param username:
        :param password:
        :param university_email:
        :param role:
        :return:
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.university_email = university_email
        self.role = role

    def __repr__(self) -> str:
        """
        String representation of User
        :return: str
        """
        return "<User: %r>" % self.username

    def get_dict(self) -> str:
        """
        Return a dict representation of User
        :return:
        """
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

    def get_name(self) -> str:
        """
        This method returns the full name of the user.
        :return: str
        """
        return "%s %s" % (self.first_name, self.last_name)

    def joined_strf(self) -> str:
        """
        Returns the joined date formatted like Jan/2016
        :return: str
        """
        return self.joined.strftime("%b. %Y")

    def is_admin(self) -> bool:
        """
        Check if the user is an administrator and returns a bool
        :return: bool
        """
        return not self.role == "costumer"

    def is_developer(self) -> bool:
        """
        Check if the user is a developer and returns a bool
        :return: bool
        """
        return not self.role == "developer"

    def is_active(self) -> bool:
        """
        Check if the user is active and returns a bool
        :return: bool
        """
        return self.active


class UserRole(BaseModel, db.Model):
    """
        UserRole table to store the different user categories and
        and control privileges for users.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(40), unique=True)

    def __init__(self, role: str):
        """
        UserRole constructor
        :param role: str
        :return:
        """
        self.role = role

    def __repr__(self) -> str:
        """
        String representation of UserRole
        :return: str
        """
        return "<Role: %r>".format(self.role)
