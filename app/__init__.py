from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import config


app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
cross = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return redirect("https://github.com/dsantosp12/textrade-services/wiki")


# API Resources Import
from app.resources.api import api_user_api
from app.resources.user import user_api
from app.resources.search import search_api

# API Models Import
from app.models.api import *
from app.models.user import *
from app.models.book import *

# API App Registration
app.register_blueprint(api_user_api, url_prefix=config.API_PREFIX_URI)
app.register_blueprint(user_api, url_prefix=config.API_PREFIX_URI)
app.register_blueprint(search_api, url_prefix=config.API_PREFIX_URI)
