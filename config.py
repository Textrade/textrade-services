import os

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Runtime Config
DOMAIN_NAME = "textrade.us"
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

# App Resources
SECRET_KEY = ';\xec:G\x91\xdf\xdf\x89\x81\x81\x13\xf0hv\xc5\x06\xa5\x9b\x84\x85\x98\xb3DC'

# Local DB Information
SQLALCHEMY_DATABASE_URI = "sqlite:///../dev-db.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Site Information
LOCAL_URL = "http://{HOST}:{PORT}/".format(HOST=HOST, PORT=PORT)
PUBLIC_URL = "http://{}/".format(DOMAIN_NAME)
URL = LOCAL_URL  # TODO: In production change to PUBLIC_URL

# API Information
API_VERSION = 1
API_PREFIX_URI = "api/v{}/".format(API_VERSION)
API_URL = URL + API_PREFIX_URI


def reset_system(db, reset=False):
    if reset:
        db.drop_all()
        db.create_all()
    else:
        db.create_all()
