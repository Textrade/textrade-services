from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

import config


app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return "<h3>For help, refer to the <a href='{}'>documentation</a>.".format(url_for('docs'))


@app.route('/api/v1/docs/')
def docs():
    return "<h3>Needs to be written</h3>"

# API Resources Import
from app.resources.api import api_user_api
from app.resources.user import user_api

# API Models Import
from app.models.api import ApiUser

# API App Registration
app.register_blueprint(api_user_api, url_prefix=config.API_PREFIX_URI)
app.register_blueprint(user_api, url_prefix=config.API_PREFIX_URI)
