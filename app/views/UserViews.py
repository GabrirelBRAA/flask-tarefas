from database import db_session
from models.User import User, UserScheme
import bcrypt
from flask_jwt_extended import create_access_token
from flask import Blueprint, request, jsonify

from flask_cors import cross_origin

user_views = Blueprint('user_views', __name__, url_prefix='/user')

@user_views.post('/create')
@cross_origin()
def create_user():
    try:
        validated_user = UserScheme.model_validate(request.json)
        if User.exists(validated_user.name):
            raise ValueError('Name already exists')
    except ValueError as e:
        return repr(e), 400

    salt=bcrypt.gensalt()
    password = validated_user.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    user = User(
        name=validated_user.name,
        password_hash=hashed_password,
        password_salt=salt, #Field inútil
    )

    db_session.add(user)
    db_session.commit()
    return jsonify(validated_user.name), 201 #Validate this with pydantic

@user_views.post('/login')
@cross_origin()
def login():
    name = request.json['name']
    try:
        user = User.query.filter(User.name == name).first()
        if user is None:
            raise ValueError("Wrong name or password!")

        if bcrypt.checkpw(request.json['password'].encode('utf-8'), user.password_hash):
            additional_claims = {"name": name}
            return create_access_token(identity=user.id, additional_claims=additional_claims)
        else:
            raise ValueError("Wrong name or password!")
    except ValueError as e:
        return repr(e), 401