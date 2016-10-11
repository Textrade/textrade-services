from flask import Blueprint, Response, request
from flask_restful import Resource, Api, reqparse, fields

from app.auth.auth import client_auth
from app.core.tools import dumper, JsonTemplate as JT
from app.core.search import SearchEngine

book_to_rent_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'author': fields.String,
    'description': fields.String,
    'isbn': fields.String,
    'condition': fields.String,
    'book_status': fields.String,
    'username': fields.String
}


class SearchRes(Resource):
    def __init__(self):
        super().__init__()

    @client_auth.login_required
    def get(self):
        json_resp = JT.JSON_RESP_TEMPLATE
        try:
            query = request.args['q']
        except KeyError:
            json_resp['status'] = 400
            json_resp['msg'] = "Invalid or missing query string"
            return Response(dumper(json_resp),
                            mimetype=JT.JSON_RESP_TYPE, status=400)
        else:

            return query


search_api = Blueprint('app.res.search', __name__)
api = Api(search_api)

api.add_resource(
    SearchRes,
    '/search',
    endpoint='search'
)
