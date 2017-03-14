import json

from flask import Response
from flask_bcrypt import generate_password_hash, check_password_hash


class ResponseTemplate:
    def __init__(self, status=None, msg=None, content=None,
                 resp_type='application/json'):
        self.dumper = json.dumps
        self.status = status
        self.data = {
            'msg': msg,
            'content': content
        }
        self.resp_type = resp_type

    def add_arg(self, key, value):
        self.data[key] = value

    def response(self):
        return Response(
            self.__dump_data(),
            mimetype=self.resp_type,
            status=self.status
        )

    def __dump_data(self, indent=4):
        return self.dumper(self.data, indent=indent)

    @staticmethod
    def get_not_found(msg):
        return ResponseTemplate(404, msg).response()


def check_hash(p_hash, password):
    return check_password_hash(p_hash, password)


def hash_password(password):
    return generate_password_hash(password)
