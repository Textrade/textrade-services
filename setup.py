"""
The purpose of this program is to setup the local environment,
with default API User, User, UserRole, more will be added in the future.
"""
import sys

from sqlalchemy.exc import IntegrityError

from app import db
from app.models.api import ApiUser
from app.models.user import User, UserRole

USER_ROLES = [
    UserRole("customer"),
    UserRole("administrator"),
    UserRole("developer"),
]

# Production: This user most be delete in production
API_USERS = [
    ApiUser("developers", "dev", "Default user to use for development"),
]

DEFAULT_USER_PASSWORD = "test"


def create_user_roles(roles=None):
    print("Creating User Roles")
    for role in roles:
        try:
            pass
        except IntegrityError:
            print("{} is duplicate... Continuing".format(role))
        else:
            print("{} created".format(role))
    print("User Roles done")


def create_users(users=None):
    import faker
    from app.core.user import UserController

    fake = faker.Factory.create()
    users = []

    print("Creating Users")
    for i in range(0, 10):
        try:
            users.append(
                UserController(
                    fake.first_name_male(),
                    fake.last_name_male(),
                    fake.user_name(),
                    DEFAULT_USER_PASSWORD,
                    fake.email()
                ).create()
            )
            UserController.activate(users[i]['username'])
        except IntegrityError:
            print("{} is duplicate... Continuing".format(users[i]))
        else:
            print("{} created".format(users[i]))
    print("Users done")


def create_api_users(api_users=None):
    print("Creating API Users")
    for api_user in api_users:
            print("Creating: {}".format(api_user))
            try:
                api_user.create()
            except IntegrityError:
                print("{} is duplicate... Continuing".format(api_user))
            else:
                print("{} created".format(api_user))
    print("API Users done")


def development():
    create_api_users(API_USERS)
    create_user_roles(USER_ROLES)
    create_users()


def usage():
    print("\nusage: python setup.py [-d development] [-p production]\n")


def run(args):
    db.create_all()  # Create database and tables if doesn't exits

    if len(args) == 2:
        if args[1] == '-d':
            development()
            print("Development setup created successfully")
        elif args[1] == '-p':
            print("Production setup hasn't been implemented")
        else:
            usage()
    else:
        usage()

if __name__ == '__main__':
    run(sys.argv)
