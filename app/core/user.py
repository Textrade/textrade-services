import datetime

import sqlalchemy as sql
from itsdangerous import URLSafeTimedSerializer

import config
from app.core.tools import hash_password, check_hash
from app.models.user import User, db


class UserController:
    SALT = "*lo!ki>,C}s%}651{343{"
    DEFAULT_DAYS = 86400 * 3  # Day in seconds times the number of days to activate account

    def __init__(self, first_name=None, last_name=None,
                 username=None, password=None, university_email=None,
                 role="customer", user=None):
        self.user = user  # This is the user object
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = UserController.__get_hash(password)
        self.university_email = university_email
        self.role = role

    @staticmethod
    def create_user(**kwargs):
        """"Create user controls."""
        user = User(
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'],
            username=kwargs['username'],
            password=hash_password(kwargs['password']),
            university_email=kwargs['email'],
            role="costumer"
        )
        db.session.add(user)
        db.session.commit()
        return user

    def create(self):
        """Create user if initialized with constructor."""
        user = User(self.first_name, self.last_name, self.username, self.password, self.university_email, self.role)
        db.session.add(user)
        db.session.commit()
        return user.get_dict()

    @staticmethod
    def activate(username):
        db.session.execute(
            sql.update(User).where(
                User.username == username
            ).values(
                active=True,
                activated_on=datetime.datetime.now()
            )
        )
        db.session.commit()

    @staticmethod
    def verify_user(username, password):
        try:
            user = UserController.get_user_by_username(username)
        except UserController.UserNotFound:
            return False
        else:
            return UserController.check_hash(user.password, password)

    def change_password(self, old_password, new_password):
        """Change the user passed in constructor."""
        if UserController.check_hash(self.password, old_password):
            db.session.execute(
                sql.update(self.user).where(
                    User.username == self.username
                ).values(
                    password=UserController.__get_hash(new_password)
                )
            )
            db.session.commit()
        else:
            raise ValueError("Old password is invalid.")

    @staticmethod
    def change_user_password(pk_id, old_password, new_password):
        """Edit a user. Old password is required."""
        user = User.query.filter_by(id=pk_id).first()

        if UserController.check_hash(user.password, old_password):
            db.session.execute(
                sql.update(User).where(
                    User.id == pk_id
                ).values(
                    password=UserController.__get_hash(new_password)
                )
            )
            db.session.commit()
        else:
            raise ValueError("Old password is invalid.")

    @staticmethod
    def delete_user(username, password):
        """Delete a user. The password must be provided."""
        user = User.get(User.username == username)
        if UserController.check_hash(
                user.password,  # Hash
                password
        ):
            user.delete_instance()
        else:
            raise PermissionError("You password is wrong.")

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise UserController.UserNotFound("%s is not a username." % user_id)
        else:
            return user

    @staticmethod
    def get_user_by_username(username=None):
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise UserController.UserNotFound("%s is not a username." % username)
        else:
            return user

    @staticmethod
    def get_user_by_university_email(university_email=None):
        user = User.query.filter_by(university_email=university_email).first()
        if user is None:
            raise UserController.UserNotFound("%s is not in our system." % university_email)
        else:
            return user

    @staticmethod
    def username_exists(username):
        try:
            UserController.get_user_by_username(username)
        except UserController.UserNotFound:
            return False
        else:
            return True

    @staticmethod
    def get_user_as_dict(university_email=None, username=None):
        if university_email:
            user = UserController.get_user_by_university_email(university_email)
        elif username:
            user = UserController.get_user_by_username(username)
        else:
            raise UserController.UserNotFound("No argument passed.")
        return user.get_dict()

    @staticmethod
    def __get_hash(password):
        return hash_password(password)

    @staticmethod
    def check_hash(p_hash, password):
        return check_hash(p_hash, password)

    def __generate_token(self):
        return URLSafeTimedSerializer(
            secret_key=config.SECRET_KEY,
            salt=UserController.SALT
        ).dumps(
            self.university_email,
        )

    @staticmethod
    def generate_token(email):
        return URLSafeTimedSerializer(
            secret_key=config.SECRET_KEY,
            salt=UserController.SALT
        ).dumps(
            email
        )

    @staticmethod
    def __confirm_token(token, expiration=None):
        serializer = URLSafeTimedSerializer(
            secret_key=config.SECRET_KEY,
            salt=UserController.SALT
        )
        if expiration:
            email = serializer.loads(
                token,
                max_age=expiration,
                salt=UserController.SALT
            )
        else:
            email = serializer.loads(
                token,
                max_age=UserController.DEFAULT_DAYS,  # Default 3 days to activate account
                salt=UserController.SALT
            )
        return email

    @staticmethod
    def activate_account(token):
        university_email = UserController.__confirm_token(token)
        db.session.execute(
            sql.update(User).where(
                User.university_email == university_email
            ).values(
                active=True,
                activated_on=datetime.datetime.now()
            )
        )
        db.session.commit()

    class UserNotFound(Exception):
        pass
