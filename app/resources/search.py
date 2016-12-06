from flask import Blueprint, Response, request
from flask_restful import Resource, Api, reqparse, fields, marshal

from app.auth.auth import client_auth
from app.core.tools import dumper, JsonTemplate as JT
from app.core.search import SearchEngine

# TODO: Check is this matches the new Book models attributes
book_to_rent_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'description': fields.String,
    'isbn': fields.String
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
            rv = SearchEngine(query).search()
            if rv[0]:
                data_list = [marshal(data, book_to_rent_fields)
                             for data in rv[0]]
                json_resp['status'] = 200
                json_resp['msg'] = "Search successful"
                json_resp['totalItems'] = len(data_list)
                json_resp['content'] = data_list
                return Response(dumper(json_resp),
                                mimetype=JT.JSON_RESP_TYPE, status=200)
            else:  # No book found
                json_resp['content'] = None
                json_resp['status'] = 404
                json_resp['msg'] = "Book not found."
                json_resp['totalItem'] = 0
                return Response(dumper(json_resp),
                                mimetype=JT.JSON_RESP_TYPE, status=200)


search_api = Blueprint('app.res.search', __name__)
api = Api(search_api)

api.add_resource(
    SearchRes,
    '/search',
    endpoint='search'
)
