from flask_bcrypt import generate_password_hash, check_password_hash

JSON_RESP_TYPE = 'application/json'
JSON_RESP_TEMPLATE = {
    'status': None,
    'msg': None,
    'content': None
}


def check_hash(p_hash, password):
    return check_password_hash(p_hash, password)


def hash_password(password):
    return generate_password_hash(password)
