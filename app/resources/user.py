from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse

from app.auth.auth import auth


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
        super().__init__()

    @auth.login_required
    def post(self):
        return "Testing!"


user_api = Blueprint('app.res.user', __name__)
api = Api(user_api)

api.add_resource(
    UserAuthRes,
    '/user/auth',
    endpoint='user_auth'
)
