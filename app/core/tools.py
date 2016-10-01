from flask_bcrypt import generate_password_hash, check_password_hash

JSON_RESP = 'application/json'


def check_hash(password, hash):
    return check_password_hash(hash, password)


def hash_password(password):
    return generate_password_hash(password)
