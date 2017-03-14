from flask import Blueprint, Response
from flask_restful import Resource, Api, reqparse, fields, marshal

from app.auth.auth import client_auth
from app.core.user import UserController
from app.core.tools import ResponseTemplate


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

    @client_auth.login_required
    def post(self):
        args = self.parser.parse_args()
        is_verify = UserController.verify_user(
            args['username'], args['password'])
        return ResponseTemplate(status=200, content=is_verify).response()

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'username': fields.String,
    'email': fields.String,
    'joined': fields.DateTime,
    'role': fields.String
}


class UserRes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'first_name',
            type=str,
            required=True,
            help="First name wasn't provided"
        )
        self.parser.add_argument(
            'last_name',
            type=str,
            required=True,
            help="Last name wasn't provided"
        )
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
        self.parser.add_argument(
            'email',
            type=str,
            required=True,
            help="Email wasn't provided"
        )
        super().__init__()

    @client_auth.login_required
    def post(self):
        return "post"

    @client_auth.login_required
    def get(self, user_id):
        try:
            user = UserController.get_user_by_id(user_id)
        except UserController.UserNotFound:
            msg = "User with ID=%s doesn't exists" % user_id
            return ResponseTemplate(status=404, msg=msg).response()
        else:
            user_info = marshal(user.get_dict(), user_fields)
            return ResponseTemplate(
                status=200, content=user_info).response()

    @client_auth.login_required
    def put(self):
        return "put"

    @client_auth.login_required
    def delete(self):
        return "delete"


user_api = Blueprint('app.res.user', __name__)
api = Api(user_api)

api.add_resource(
    UserAuthRes,
    '/users/auth',
    endpoint='user_auth'
)

api.add_resource(
    UserRes,
    '/users',
    '/users/<int:user_id>',
    endpoint='user'
)
