import json

from flask_bcrypt import generate_password_hash, check_password_hash

dumper = json.dumps


class JsonTemplate:
    JSON_RESP_TYPE = 'application/json'
    JSON_RESP_TEMPLATE = {
        'status': None,
        'msg': None,
        'content': None
    }
    JSON_NOT_FOUND_TEMPLATE = {
        'status': 404,
        'msg': None,
        'content': None
    }


def check_hash(p_hash, password):
    return check_password_hash(p_hash, password)


def hash_password(password):
    return generate_password_hash(password)
