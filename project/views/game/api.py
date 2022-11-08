from flask import Blueprint, jsonify, request, Response, abort
from marshmallow import ValidationError
from ..utils import createValidationErrorMessage
import logging
from models.game import Game, GameSchema
from extensions import db
from flasgger import swag_from
import os
games = Blueprint('games', __name__, url_prefix='/games')

logging_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

path = os.path.realpath(os.path.dirname(__file__))

@games.route('/', methods=['POST'])
@swag_from(os.path.join(path, 'docs', 'post_game.yml'))
def create_game():
    """ Create a new game """
    content = request.get_json()

    name = content.get("name")
    category_id = content.get("category_id")
    new_game = Game(name=name, category_id=category_id)

    game_schema = GameSchema()
    try:
        game_schema.load(new_game.to_json()) # Validates the input

        db.session.add(new_game)
        db.session.commit()

        return jsonify({
            "message": "new game inserted",
            "game": game_schema.dump(new_game)
            }, 200)
    except ValidationError as e:
        return jsonify(createValidationErrorMessage(e)), 400
    
@games.route('/', methods=['GET'])
@swag_from(os.path.join(path, 'docs', 'get_games.yml'))
def get_games():
    games = Game.query.all()

    game_schema = GameSchema(many=True)
    resp = game_schema.dump(games)

    return jsonify(
        {"games":resp}
        ), 200
    

@games.route('/<id>', methods=['GET'])
@swag_from(os.path.join(path, 'docs', 'get_game.yml'))
def get_game_by_id(id):
    """Returns a game that has the same input id of <id> in json format"""
    game = Game.query.get_or_404(id) 
    game_schema = GameSchema()
    return jsonify({"game": game_schema.dump(game)})

@games.route('/<id>', methods=['DELETE'])
@swag_from(os.path.join(path, 'docs', 'delete_game.yml'))
def delete_game_by_id(id):
    games = db.session.query(Game).filter(Game.id == id).delete()
    if (games == 1):
        db.session.commit()
        logging.info("Successful deletion")
        return jsonify({"message": "Successful deletion"})
    else: 
        logging.error("Game not found")
        return abort(404)
    
@games.route('/<id>', methods=['PUT'])
@swag_from(os.path.join(path, 'docs', 'update_game.yml'))
def game_update(id):

    game = Game.query.get_or_404(id)
    content = request.get_json()

    name = content.get("name", game.name)
    category_id = content.get("category_id", game.category_id)

    game_schema = GameSchema()
    try:
        result = game_schema.load(
            {"name": name,
            "category_id": category_id}
        )
        game.name = name
        game.category_id = category_id
        db.session.commit()

        return jsonify({"game": result})
    except ValidationError as e:
        return jsonify(createValidationErrorMessage(e)), 400


