from flask import Blueprint, jsonify, g
from flask_restful import Resource, Api

from app.auth.auth import auth


class ApiUserRes(Resource):
    def __init__(self):
        super().__init__()

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        json_resp = jsonify({
            'status': 200,
            'msg': "",
            'content': {
                'token': token.decode('ascii')
            },
        })

api_user_api = Blueprint('app.res.api_user', __name__)

api = Api(api_user_api)

api.add_resource(
    ApiUserRes,
    '/client/verification',
    endpoint='api_user'
)
