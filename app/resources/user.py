import json

from flask import Blueprint, Response
from flask_restful import Resource, Api, reqparse

from app.auth.auth import auth
from app.core.user import UserController
from app.core.tools import JSON_RESP_TYPE, JSON_RESP_TEMPLATE


class UserAuthRes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'username',
            type=str,
            required=True,
            help="Username wasn't provided"
        )
        self.parser.add_argument(
            'password',
            type=str,
            required=True,
            help="Password wasn't provided"
        )

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        json_resp = JSON_RESP_TEMPLATE
        json_resp['status'] = 200
        json_resp['content'] = UserController.verify_user(args['username'], args['password'])
        return Response(json.dumps(json_resp, indent=4), status=200, mimetype=JSON_RESP_TYPE)


user_api = Blueprint('app.res.user', __name__)
api = Api(user_api)

api.add_resource(
    UserAuthRes,
    '/user/auth',
    endpoint='user_auth'
)
