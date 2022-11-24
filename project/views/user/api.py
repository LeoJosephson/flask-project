from flask import Blueprint, jsonify, request
from models.user import User, UserSchema, UserSchemaView
from extensions import db
from marshmallow import ValidationError
from ..utils import createValidationErrorMessage
import bcrypt


users = Blueprint('users', __name__, url_prefix='/users')
user_schema = UserSchema()

@users.route('/', methods=['POST'])
def create_user():
    content = request.get_json()

    username = content.get("username")
    email = content.get("email")
    password = content.get('password')
    new_user = User(username=username, email=email, password=password )


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

@users.route('/', methods=['GET'])
def get_users():
    users = db.session.query(User).all()
    user_schema_m = UserSchemaView(many=True)

    return jsonify({"users":user_schema_m.dump(users)}),200

@users.route('/<id>', methods=['GET'])
def get_user(id):
    users = db.session.query(User).filter(User.id == id).first()
    user_schema_m = UserSchemaView()

    if users != None:
        return jsonify({"user":user_schema_m.dump(users)}),200
    else:
        return abort(404)

    
