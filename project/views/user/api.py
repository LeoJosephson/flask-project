from flask import Blueprint, jsonify, request
from models.user import User, UserSchema
from extensions import db
from marshmallow import ValidationError
from ..utils import createValidationErrorMessage
import bcrypt


users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['POST'])
def create_user():
    content = request.get_json()

    username = content.get("username")
    email = content.get("email")
    password = content.get('password')
    new_user = User(username=username, email=email, password=password )

    user_schema = UserSchema()
    try:
        user_schema.load(new_user.to_json()) # Validates the input

        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user.password = password_hashed

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "new user created",
            })

    except ValidationError as e:
        msg = createValidationErrorMessage(e)
        return jsonify(msg), 400


