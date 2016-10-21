"""
The purpose of this program is to setup the local environment,
with default API User, User, UserRole, more will be added in the future.
"""
import sys
import os

from sqlalchemy.exc import IntegrityError

from app import db
import config
from app.models.api import ApiUser
from app.models.user import User, UserRole
from app.core.book import BookRentController
from app.models.book import (BookToRent, BookTradeHave, BookTradeWant,
                             BookStatus, Condition, BookRenting,
                             BookRentingRequest)

FILE_NAME = "users.txt"
USER_ROLES = [
    UserRole("customer"),
    UserRole("administrator"),
    UserRole("developer"),
]

DEFAULT_USER_PASSWORD = "test"

# Production: This user most be delete in production
API_USERS = [
    ApiUser("developers", "dev", "Default user to use for development"),
]

BOOK_CONDITIONS = [
    Condition("Like New", "New"),
    Condition("Very Good", "Minimal wear on cover, otherwise perfect"),
    Condition("Good", "Some wear on the cover, spine and pages"),
    Condition("Fair", "Noticeable wear on the cover, spine and pages"),
    Condition("Bad", "Clear evidence of heavy use")
]

BOOK_STATUS = [
    BookStatus("available"),
    BookStatus("no_available"),
    BookStatus("rented"),
    BookStatus("requested")
]

BOOKS_TO_RENT_ISBN = [
    "9780981467344",
    "9780399144462",
    "9780812981605",
    "9780062367549",
    "9780804139298",
    "9781601633088",
    "9781455582341",
    "9780399184123",
    "9781885167774",
    "9780984782802",
    "9780321923271",
    "9780321714114",
    "9780201314526",
    "9780133378719",
    "9781585424337",
    "9788449321948",
    "9780470903247",
    "9780321973610",
    "9780538497817",
    "9781250014450"
]


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


def create_users():
    import faker
    from app.core.user import UserController

    fake = faker.Factory.create()
    users = []
    fp = open(FILE_NAME, "w")
    fp.write("Development User Information\n\n")
    fp.write("Password for all users is: '{}'\n\n".format(DEFAULT_USER_PASSWORD))
    fp.write("Username\n=========\n")

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
            fp.write("{}\n".format(users[i]['username']))
            print("{} created".format(users[i]))
    fp.close()
    print("Users done")

    return users


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


def create_book_status(status=None):
    print("Creating Book Status")
    for s in status:
        try:
            s.create()
        except IntegrityError:
            print("{} is duplicate... Continuing".format(s))
        else:
            print("{} created".format(s))
    print("Book Status Done")


def create_book_condition(book_conditions):
    print("Creating Book Conditions")
    for condition in book_conditions:
        try:
            condition.create()
        except IntegrityError:
            print("{} is duplicate... Continuing".format(condition))
        else:
            print("{} created".format(condition))
    print("Book Conditions done")


def create_book_to_rent(users, books):
    print("Creating Book to Rent")
    if len(books) < 20:
        raise ValueError("Books array must be greater than 20")

    count = 0
    for user in users:
        b = BookRentController.create_renting_book(
            books[count], user_id=user['id'], condition=1,
            marks=False, condition_comment=""
        ).create()
        print("{} created by {}".format(b, user['username']))
        b = BookRentController.create_renting_book(
            books[count + 1], user_id=user['id'], condition=1,
            marks=False, condition_comment=""
        ).create()
        print("{} created by {}".format(b, user['username']))
        count += 2

    print("Book to Rent done")


def development():
    create_api_users(API_USERS)
    create_user_roles(USER_ROLES)
    USERS = create_users()
    create_book_condition(BOOK_CONDITIONS)
    create_book_status(BOOK_STATUS)
    create_book_to_rent(USERS, BOOKS_TO_RENT_ISBN)


def reset():
    os.remove('./%s' % config.DB_NAME)
    os.remove('./%s' % FILE_NAME)


def usage():
    print("\nusage: python setup.py [-d development] [-p production] [-rd reset and build development]\n")


def run(args):
    db.create_all()  # Create database and tables if doesn't exits

    if len(args) == 2:
        if args[1] == '-d':
            development()
            print("Development setup created successfully")
        elif args[1] == '-rd':
            reset()
            db.create_all()  # Create database and tables if doesn't exits
            development()
        elif args[1] == '-p':
            print("Production setup hasn't been implemented")
        else:
            usage()
    else:
        usage()

if __name__ == '__main__':
    run(sys.argv)
