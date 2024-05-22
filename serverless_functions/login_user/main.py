import functions_framework
import pytz
import os

from flask import jsonify
from sqlalchemy import and_

from library_serverless_core.persistence.database import open_session
from library_serverless_core.security.token_utils import generate_token
from library_serverless_core.shared_models.User import User

secret = os.environ.get('JWT_KEY')
tz = pytz.timezone('America/Bogota')


@functions_framework.http
def login_user(request):
    username = request.json['username']
    password = request.json['password']

    with open_session() as session:
        valid_user = session.query(User).filter(and_(
            User.username == username,
            User.password == password
        )).first()

        if valid_user:
            return jsonify({
                'success': True,
                'token': generate_token(valid_user)
            }), 200

        return jsonify({
            'message': 'Invalid credentials'
        }), 401
