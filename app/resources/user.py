import json

from flask import Blueprint, Response
from flask_restful import Resource, Api, reqparse, fields, marshal

from app.auth.auth import client_auth
from app.core.user import UserController
from app.core.tools import JsonTemplate as JT, dumper


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

    # @client_auth.login_required
    def post(self):
        args = self.parser.parse_args()
        json_resp = JT.JSON_RESP_TEMPLATE
        json_resp['status'] = 200
        json_resp['content'] = UserController.verify_user(
            args['username'], args['password'])
        return Response(dumper(json_resp, indent=4),
                        status=200, mimetype=JT.JSON_RESP_TYPE)


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

    # @client_auth.login_required
    def post(self):
        return "post"

    # @client_auth.login_required
    def get(self, user_id):
        try:
            user = UserController.get_user_by_id(user_id)
        except UserController.UserNotFound:
            json_resp = JT.JSON_NOT_FOUND_TEMPLATE
            json_resp['msg'] = "User with ID=%s doesn't exists" % user_id
            return Response(dumper(JT.JSON_NOT_FOUND_TEMPLATE),
                            status=404, mimetype=JT.JSON_RESP_TYPE)
        else:
            json_resp = JT.JSON_RESP_TEMPLATE
            user_info = marshal(user.get_dict(), user_fields)
            json_resp['content'] = user_info
            json_resp['status'] = 200
            return Response(dumper(json_resp),
                            status=200, mimetype=JT.JSON_RESP_TYPE)

    # @client_auth.login_required
    def put(self):
        return "put"

    # @client_auth.login_required
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
