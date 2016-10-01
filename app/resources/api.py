import json

from flask import Blueprint, g, Response
from flask_restful import Resource, Api

from app.auth.auth import auth
from app.core.tools import JSON_RESP_TYPE, JSON_RESP_TEMPLATE


class ApiUserRes(Resource):
    def __init__(self):
        super().__init__()

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        json_resp = JSON_RESP_TEMPLATE
        json_resp['status'] = 200
        json_resp['content'] = {'token': token.decode('ascii')}
        return Response(json.dumps(json_resp, indent=4), status=200, mimetype=JSON_RESP_TYPE)

api_user_api = Blueprint('app.res.api_user', __name__)

api = Api(api_user_api)

api.add_resource(
    ApiUserRes,
    '/client/auth',
    endpoint='api_user'
)
