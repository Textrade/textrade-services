from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from app.models.api import ApiUser

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')
client_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    client = ApiUser.get_user(username)
    if client is None:
        return False
    else:
        if client.verify_password(password):
            g.client = client
            return True
    return False


@token_auth.verify_token
def verify_token(token):
    client = ApiUser.verify_auth_token(token)
    if client is not None:
        g.client = client
        return True
    return False
