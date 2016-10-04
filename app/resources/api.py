import json

from flask import Blueprint, g, Response, request
from flask_restful import Resource, Api

from app.auth.auth import client_auth
from app.core.tools import JsonTemplate as JT, dumper


class ApiUserRes(Resource):
    def __init__(self):
        super().__init__()

    # @client_auth.login_required
    def get(self):
        token = g.client.generate_auth_token()
        json_resp = JT.JSON_RESP_TEMPLATE
        json_resp['status'] = 200
        json_resp['content'] = {'token': token.decode('ascii')}
        return Response(dumper(json_resp, indent=4),
                        status=200, mimetype=JT.JSON_RESP_TYPE)

api_user_api = Blueprint('app.res.api_user', __name__)

api = Api(api_user_api)

api.add_resource(
    ApiUserRes,
    '/clients/auth',
    endpoint='api_user'
)
