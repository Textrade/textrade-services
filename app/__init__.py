from flask import Flask, url_for


app = Flask(__name__)


@app.route('/')
def index():
    return "<h3>For help, refer to the <a href='{}'>documentation</a>.".format(url_for('docs'))


@app.route('/api/v1/docs/')
def docs():
    return "<h3>Needs to be written</h3>"
