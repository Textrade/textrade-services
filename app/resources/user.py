import json

from flask import Blueprint, jsonify, Response
from flask_restful import Resource, Api, reqparse

from app.auth.auth import auth
from app.core.tools import JSON_RESP


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
        resp = None
        args = self.parser.parse_args()



        return ""


user_api = Blueprint('app.res.user', __name__)
api = Api(user_api)

api.add_resource(
    UserAuthRes,
    '/user/auth',
    endpoint='user_auth'
)
