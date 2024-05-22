import functions_framework
from flask import jsonify

from library_serverless_core.persistence.database import open_session
from library_serverless_core.shared_models.Role import Role
from library_serverless_core.shared_models.User import User


@functions_framework.http
def create_user(request):
    role = request.json['role']
    email = request.json['email']

    with open_session() as session:
        role = session.query(Role).filter(Role.role_name == role).first()
        user = session.query(User).filter(User.email == email).first()

        if role and user is None:
            new_user = User(
                fullname=request.json['fullname'],
                username=request.json['username'],
                password=request.json['password'],
                email=email
            )
            new_user.role = role
            session.add(new_user)
            session.commit()
            return jsonify({
                'success': True,
            }), 201

        return jsonify(''), 505
