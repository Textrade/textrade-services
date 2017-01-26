from flask import Blueprint, Response, request
from flask_restful import Resource, Api, reqparse, fields, marshal

from app.auth.auth import client_auth
from app.core.tools import ResponseTemplate
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
        try:
            query = request.args['q']
        except KeyError:
            msg = "Invalid or missing query string"
            return ResponseTemplate(400, msg).get_response()
        else:
            rv = SearchEngine(query).search()
            if rv[0]:
                data_list = [marshal(data, book_to_rent_fields)
                             for data in rv[0]]
                msg = "Search successful"
                response_template = ResponseTemplate(200, msg, data_list)
                response_template.add_arg('totalItems', len(data_list))
                return response_template.get_response()
            else:
                return ResponseTemplate.get_not_found("Any books found")


search_api = Blueprint('app.res.search', __name__)
api = Api(search_api)

api.add_resource(
    SearchRes,
    '/search',
    endpoint='search'
)
