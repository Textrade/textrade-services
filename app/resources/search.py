from flask import Blueprint, Response, request
from flask_restful import Resource, Api, reqparse, fields, marshal

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
    'user': fields.String
}

"""
No book => Show book -> [GoogleSearch] -> insert to Book -> "no available"
No available => Show book -> "no available"
Available ? book to rent => Show book -> "available"
"""


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
            if query.isdigit():
                rv = SearchEngine.book_by_isbn(query)
                data_list = [marshal(data, book_to_rent_fields) for data in rv]
                json_resp['status'] = 200
                json_resp['msg'] = "Search successful"
                json_resp['totalItems'] = len(data_list)
                json_resp['content'] = data_list
                return Response(dumper(json_resp),
                                mimetype=JT.JSON_RESP_TYPE, status=200)
            elif not query.isnumeric():
                rv = SearchEngine.book_by_title(query)
                data_list = [marshal(data, book_to_rent_fields) for data in rv]
                json_resp['status'] = 200
                json_resp['msg'] = "Search successful"
                json_resp['totalItems'] = len(data_list)
                json_resp['content'] = data_list
                return Response(dumper(json_resp),
                                mimetype=JT.JSON_RESP_TYPE, status=200)
            return query


search_api = Blueprint('app.res.search', __name__)
api = Api(search_api)

api.add_resource(
    SearchRes,
    '/search',
    endpoint='search'
)
