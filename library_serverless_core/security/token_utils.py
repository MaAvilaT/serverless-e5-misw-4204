import datetime
import logging
import os
import jwt
import pytz

from ..shared_models.User import User

secret = os.environ.get('JWT_KEY')
tz = pytz.timezone('America/Bogota')

logger = logging.Logger(level=logging.INFO, name='access.log')


def generate_token(authenticated_user: User):
    payload = {
        'iat': datetime.datetime.now(tz=tz),
        'exp': datetime.datetime.now(tz=tz) + datetime.timedelta(minutes=120),
        'username': authenticated_user.username,
        'fullname': authenticated_user.fullname,
        'user_id': authenticated_user.id,
        'roles': [authenticated_user.role.role_name]
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def verify_token(headers):
    if 'Authorization' in headers.keys():
        authorization = headers['Authorization']
        encoded_token = authorization.split(" ")[1]

        if len(encoded_token) > 0:
            try:
                payload = jwt.decode(encoded_token, secret, algorithms=["HS256"])
                roles = list(payload['roles'])

                if 'PARTICIPANT' in roles:
                    return True

                return False
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False

        return False


def decode_token(headers):
    authorization = headers['Authorization']
    encoded_token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(encoded_token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.log(logging.ERROR, 'Expired token')
    except jwt.InvalidTokenError:
        logger.log(logging.ERROR, 'Invalid token')

    return None
