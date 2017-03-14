from flask import Blueprint, g, Response, request
from flask_restful import Resource, Api

from app.auth.auth import client_auth
from app.core.tools import ResponseTemplate


class ApiUserRes(Resource):
    def __init__(self):
        super().__init__()

    @client_auth.login_required
    def get(self):
        token = g.client.generate_auth_token()
        content = {'token': token.decode('ascii')}
        return ResponseTemplate(status=200, content=content).response()

api_user_api = Blueprint('app.res.api_user', __name__)

api = Api(api_user_api)

api.add_resource(
    ApiUserRes,
    '/clients/auth',
    endpoint='api_user'
)
